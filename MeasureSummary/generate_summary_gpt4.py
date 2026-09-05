"""
process_measures.py

Reads a measures text file, calls Azure OpenAI GPT-4 in batches of 50 rows
using the structured supply-chain prompt, and appends parsed results to a CSV file.

Requirements:
    pip install openai pandas

Usage:
    python process_measures.py --input measures.txt --output results.csv
"""

import argparse
import ast
import csv
import io
import json
import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
from openai import AzureOpenAI

# ---------------------------------------------------------------------------
# Azure OpenAI configuration
# ---------------------------------------------------------------------------
AZURE_API_VERSION  = "2024-05-01-preview"
AZURE_ENDPOINT     = "https://o9-oai-eastus2.openai.azure.com"
AZURE_API_KEY      = "de82e9c0f8fe450ea761c8301e56fe79"          # ← replace or set env var AZURE_OPENAI_API_KEY
DEPLOYMENT_NAME    = "o9-gpt-4"

# ---------------------------------------------------------------------------
# Prompt template (everything before the measures list)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an expert at extracting structured data from supply chain platform documentation."""

USER_PROMPT_TEMPLATE = """\
You are an expert at extracting structured data from supply chain platform documentation.

Your task is to identify MEASURES, BUSINESS Capabilities, MEASURE descriptions and the relationships between them.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
DOMAIN CONTEXT:
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Demand Planning;

Models: Collaborative Demand Planning, Basic ML/Stat Forecasting, NPI Forecasting, Spares Forecasting, Reverse Forecasting, Demand Sensing, Short term ML forecasting, Advanced ML Forecasting, Long Range Demand Forecasting
entities: Product/SKU Hierarchy, Locations/Network, Historical Data, Forecasted Data, Calendar/Time, Inventory Levels
drivers: Product Lifecycle Data, External Factors, Out-of-Stock Indicators, Customer Behavior/Market Intelligence, Seasonality/Trends, Price Changes, Promotions
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Supply Planning;

Models: SC Planning Data Foundation, SC Master Planning Foundation, SC Operational Planning Foundation, Order Promising & Order Scheduling, Production Scheduling & Sequencing, Transportation Scheduling, Spares Planning, Reverse Planning, Multi-Tier Supplier Relationship Management (SRM), Sourcing, Contract Management, Supplier Collaboration (Procure to Pay), Risk Management
entities: Customers, Suppliers/Vendors, Transportation, Inventory, Facilities
drivers: Cost Structures, Information Systems, Lead Times, Production Capacity, Demand Forecast
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Definitions:

- MEASURE: A quantitative data entity, which contains information of business values  (e.g., Forecast, forecast accuracy).
- ATTRIBUTE: A categorical attribute used to slice data (e.g., "Product Category"). Only extract if clearly associated with a measure.
- BUSINESS CAPABILITY: The well defined granular business capability or process area served. For each capability, provide a brief description (1-2 sentences) explaining what this capability represents in the context of the entity & the attached document. Capabilities are not Business functionalities but more granular (Ex: Demand Planning can have multiple capabilities within it like forecast management etc)
- MEASURE description: A detailed, measure-specific description of what the measure enables or represents within a business context (e.g., "Tracks deviation between ML-generated forecast and actuals to evaluate new product launch accuracy").
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Rules:

1. Only extract Measures that are explicitly mentioned in the input list. Never invent measures. Do not change the measure names.
2. Business Capabilities and measure description must be synthesised from the full domain context.
3. A measure can map to multiple business capabilities.
4. If an attribute is mentioned alongside a measure, include it as an attribute across that measure.
5. Include a brief reasoning excerpt (max 100 chars) as evidence for each extracted relationship.
6. If the section context implies a capability but is not named explicitly, mark capability_confidence as "MEDIUM", otherwise "HIGH".
7. Ensure similar measures map to consistent capabilities.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
OUTPUT FORMAT:
Return ONLY a JSON array. Each element must have exactly these keys:
  - measure_name         (string)
  - aliases              (comma-separated string, empty string if none)
  - business_capability  (string)
  - capability_description (string, 1-2 sentences)
  - capability_confidence  ("HIGH" or "MEDIUM")
  - measure_description  (string)
  - attributes           (comma-separated string, empty string if none)
  - evidence             (string, max 100 chars)

If a measure maps to multiple capabilities, emit one JSON object per capability.
Do NOT wrap the JSON in markdown code fences.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
measures to extract (MeasureName, [aliases]):
{measures_block}
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_input_file(path: str) -> list[tuple[str, list[str]]]:
    """Parse the measures text file into (name, aliases) tuples."""
    measures = []
    with open(path, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            # Split on the first tab (or multiple spaces acting as separator)
            parts = re.split(r"\t+|\s{2,}", line, maxsplit=1)
            if len(parts) < 2:
                # Try splitting on the last '[' to handle single-space delimited files
                idx = line.rfind("[")
                if idx == -1:
                    continue
                parts = [line[:idx].strip(), line[idx:].strip()]
            name = parts[0].strip()
            alias_raw = parts[1].strip()
            try:
                aliases = ast.literal_eval(alias_raw)
                if not isinstance(aliases, list):
                    aliases = []
            except Exception:
                aliases = []
            measures.append((name, aliases))
    return measures


def format_measures_block(batch: list[tuple[str, list[str]]]) -> str:
    """Format a batch of measures into the tuple-per-line style the prompt expects."""
    lines = []
    for name, aliases in batch:
        lines.append(f'("{name}",\t{aliases})')
    return "\n".join(lines)


def call_gpt4(client: AzureOpenAI, measures_block: str, retries: int = 3) -> str:
    """Call Azure OpenAI GPT-4 and return the raw text response."""
    prompt = USER_PROMPT_TEMPLATE.format(measures_block=measures_block)
    for attempt in range(1, retries + 1):
        try:
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,          # Azure uses deployment name here
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
            )
            return response.choices[0].message.content
        except Exception as exc:
            print(f"  [attempt {attempt}/{retries}] API error: {exc}")
            if attempt < retries:
                time.sleep(5 * attempt)
            else:
                raise


def parse_llm_response(raw: str) -> list[dict]:
    """Extract a JSON array from the LLM response, tolerating markdown fences."""
    # Strip markdown fences if present
    cleaned = re.sub(r"```(?:json)?", "", raw, flags=re.IGNORECASE).strip().rstrip("`").strip()
    # Find first '[' and last ']'
    start = cleaned.find("[")
    end = cleaned.rfind("]")
    if start == -1 or end == -1:
        print("  WARNING: Could not locate JSON array in response. Skipping batch.")
        print("  Raw response snippet:", raw[:300])
        return []
    json_str = cleaned[start : end + 1]
    try:
        data = json.loads(json_str)
        if not isinstance(data, list):
            return []
        return data
    except json.JSONDecodeError as exc:
        print(f"  WARNING: JSON parse error ({exc}). Attempting line-by-line recovery.")
        # Try to recover partial objects
        objects = []
        for match in re.finditer(r"\{[^{}]+\}", json_str, re.DOTALL):
            try:
                obj = json.loads(match.group())
                objects.append(obj)
            except Exception:
                pass
        return objects


EXPECTED_COLUMNS = [
    "measure_name",
    "aliases",
    "business_capability",
    "capability_description",
    "capability_confidence",
    "measure_description",
    "attributes",
    "evidence",
]


def append_to_csv(rows: list[dict], output_path: str, all_columns: set):
    """Append rows to CSV, dynamically handling extra/missing columns."""
    if not rows:
        return

    # Discover any new columns in this batch
    for row in rows:
        all_columns.update(row.keys())

    # Build ordered column list: expected first, then any extras alphabetically
    ordered_cols = EXPECTED_COLUMNS + sorted(all_columns - set(EXPECTED_COLUMNS))

    file_exists = Path(output_path).exists()

    if file_exists:
        # Re-read existing file, add missing columns, rewrite with full header
        existing_df = pd.read_csv(output_path, dtype=str).fillna("")
        new_df = pd.DataFrame(rows).fillna("")
        combined = pd.concat([existing_df, new_df], ignore_index=True)
        for col in ordered_cols:
            if col not in combined.columns:
                combined[col] = ""
        combined = combined[ordered_cols]
        combined.to_csv(output_path, index=False, encoding="utf-8")
    else:
        new_df = pd.DataFrame(rows).fillna("")
        for col in ordered_cols:
            if col not in new_df.columns:
                new_df[col] = ""
        new_df = new_df[ordered_cols]
        new_df.to_csv(output_path, index=False, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Process supply chain measures with Azure OpenAI GPT-4.")
    parser.add_argument("--input",      required=True,          help="Path to the measures text file")
    parser.add_argument("--output",     default="results.csv",  help="Output CSV file (default: results.csv)")
    parser.add_argument("--batch-size", type=int, default=50,   help="Rows per LLM call (default: 50)")
    args = parser.parse_args()

    # Allow API key override via environment variable
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", AZURE_API_KEY)

    client = AzureOpenAI(
        api_version    = AZURE_API_VERSION,
        azure_endpoint = AZURE_ENDPOINT,
        api_key        = api_key,
    )

    print(f"Reading measures from: {args.input}")
    measures = parse_input_file(args.input)
    print(f"  Found {len(measures)} measures.")

    if not measures:
        sys.exit("No measures found. Check your input file format.")

    all_columns: set = set()
    total_batches = (len(measures) + args.batch_size - 1) // args.batch_size

    for batch_idx in range(total_batches):
        start = batch_idx * args.batch_size
        end   = start + args.batch_size
        batch = measures[start:end]

        print(f"\nBatch {batch_idx + 1}/{total_batches} — measures {start + 1}–{min(end, len(measures))}")
        measures_block = format_measures_block(batch)

        print("  Calling Azure OpenAI GPT-4 ...")
        raw_response = call_gpt4(client, measures_block)

        print("  Parsing response ...")
        rows = parse_llm_response(raw_response)
        print(f"  Extracted {len(rows)} row(s).")

        if rows:
            append_to_csv(rows, args.output, all_columns)
            print(f"  Appended to {args.output}")
        else:
            print("  No rows to append for this batch.")

        # Polite pause between batches to avoid rate limits
        if batch_idx < total_batches - 1:
            time.sleep(2)

    print(f"\nDone. Results written to: {args.output}")


if __name__ == "__main__":
    main()