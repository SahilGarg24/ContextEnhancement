"""
APEX Key Entities Ranking — offline utility
============================================
Invoked by run.bat.  All paths are passed as command-line arguments so
the script itself never needs to be edited by the end user.

Usage (handled by run.bat):
    python main.py <CLIENT> <CONFIG_ZIP> <TENANT_CSV> <ADOPTION_CSV> <PSR_CSV>
"""

import sys
import csv
import argparse
import pandas as pd

from data_utils import data_extraction_utils
from ranking_utils import entity_ranking


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args():
    parser = argparse.ArgumentParser(
        description="APEX Key Entities Ranking — offline utility"
    )
    parser.add_argument("client",   help="Client / project name (informational only)")
    parser.add_argument("config",   help="Path to config backup ZIP file")
    parser.add_argument("tenant",   help="Path to TenantLogs CSV file")
    parser.add_argument("adoption", help="Path to AdoptionData CSV file (pass empty string to skip)")
    parser.add_argument("psr",      help="Path to ELK PSR CSV file (pass empty string to skip)")
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = _parse_args()

    deu = data_extraction_utils()
    er  = entity_ranking()

    print(f"Running for: {args.client}")

    # -- Config data ---------------------------------------------------------
    print("Loading config data...")
    df_vwml = deu.get_widgetmeasureslist_from_config(args.config)
    df_md   = deu.get_measuredescriptions_from_config(args.config)

    # df_md contains [Measure, Grain] — reused directly as Measure<->DimAttr
    # structural input; no separate config read needed.
    df_da = df_md

    wml   = df_vwml[["Widget", "Measure"]].drop_duplicates()
    wmmdl = (
        wml.merge(df_md, how="left", on="Measure")
        .groupby("Widget")
        .agg(
            measure_list=("Measure", list),
            measure_descriptions=("Description", list),
        )
        .reset_index()
    )

    # -- Tenant log stats (mandatory) ----------------------------------------
    print("Computing measure & dimension.attribute interaction scores from tenant logs...")
    df_tenant_raw = pd.read_csv(args.tenant)
    df_tenant_stats, df_dimattr_stats = deu.get_measure_and_dim_attrs_stats_from_tenantlogs(df_tenant_raw)

    measure_scores = er.generate_measure_ranks_from_logs_data(df_tenant_stats)
    dimattr_scores = er.generate_dimattr_ranks_from_logs_data(df_dimattr_stats)

    # -- Adoption log stats (optional) ---------------------------------------
    print("Computing view interaction scores from adoption logs...")
    try:
        if not args.adoption:
            raise ValueError("No adoption file path provided")
        df_adoption_raw   = pd.read_csv(args.adoption)
        df_adoption_stats = deu.get_view_stats_from_adoptionlogs(df_adoption_raw)
        view_scores       = er.generate_view_ranks_from_adoption_data(df_adoption_stats)
    except Exception as e:
        print(f"  WARNING: Adoption data unavailable - view scores will be zero. Reason: {e}")
        view_scores = pd.DataFrame(columns=["View", "interaction_score"])

    # -- PSR / ELK log stats (optional) --------------------------------------
    print("Computing widget interaction scores from PSR logs...")
    try:
        if not args.psr:
            raise ValueError("No PSR file path provided")
        df_psr_raw    = pd.read_csv(args.psr, sep=",")        # delimiter: comma
        df_psr_stats  = deu.get_widget_stats_from_psrlogs(df_psr_raw)
        widget_scores = er.generate_widget_ranks_from_psr_data(df_psr_stats)
    except Exception as e:
        print(f"  WARNING: PSR data unavailable - widget scores will be zero. Reason: {e}")
        widget_scores = pd.DataFrame(columns=["Widget", "interaction_score"])

    # -- PageRank ------------------------------------------------------------
    print("Running PageRank...")
    measure_final, widget_final, dimattr_final = er.generate_ranks(
        config_data    = df_vwml,
        md_data        = df_da,
        view_scores    = view_scores,
        widget_scores  = widget_scores,
        measure_scores = measure_scores,
        dimattr_scores = dimattr_scores,
    )

    # -- Output 1: measure_ranks.csv -----------------------------------------
    # Columns: Measure, Aliases — ranked by pagerank_score descending.
    # Aliases come from the Translation column in df_md.
    measure_out = (
        measure_final[["Measure", "pagerank_score"]]
        .merge(df_md[["Measure", "Translation"]].drop_duplicates(), on="Measure", how="left")
        .rename(columns={"Translation": "Aliases"})
        .sort_values("pagerank_score", ascending=False)
        [["Measure", "Aliases"]]
    )
    measure_out.to_csv("measure_ranks.csv", index=False, quoting=csv.QUOTE_ALL)
    print(f"  Saved measure_ranks.csv  ({len(measure_out)} measures)")

    # -- Output 2: dimattr_ranks.csv -----------------------------------------
    # Column: DimAttr — ranked by pagerank_score descending.
    dimattr_out = (
        dimattr_final[["DimAttr", "pagerank_score"]]
        .sort_values("pagerank_score", ascending=False)
        [["DimAttr"]]
    )
    dimattr_out.to_csv("dimattr_ranks.csv", index=False, quoting=csv.QUOTE_ALL)
    print(f"  Saved dimattr_ranks.csv  ({len(dimattr_out)} attributes)")

    print("Completed.")


if __name__ == "__main__":
    main()