"""
APEX Key Entities Ranking — offline utility
============================================
Reads all configuration from config.txt in the same folder.
End users only edit config.txt — no command-line args, no batch syntax.
"""

import os
import csv
import pandas as pd

from data_utils import data_extraction_utils
from ranking_utils import entity_ranking


# ---------------------------------------------------------------------------
# Config reader
# ---------------------------------------------------------------------------

def _read_config(config_path="config.txt") -> dict:
    """
    Parse a simple KEY=VALUE text file.
    Lines starting with # (after stripping) are treated as comments.
    Values are stripped of surrounding whitespace.
    Missing keys default to empty string (treated as "skip" for optional paths).
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"config.txt not found at '{os.path.abspath(config_path)}'.\n"
            "Please place config.txt in the same folder as main.py."
        )

    cfg = {}
    with open(config_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            cfg[key.strip()] = value.strip()

    required = ["CLIENT", "CONFIG", "TENANT"]
    for key in required:
        if not cfg.get(key):
            raise ValueError(
                f"'{key}' is missing or blank in config.txt — it is mandatory."
            )

    # Optional keys default to empty string
    cfg.setdefault("ADOPTION", "")
    cfg.setdefault("PSR", "")

    return cfg


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cfg = _read_config()

    client   = cfg["CLIENT"]
    config   = cfg["CONFIG"]
    tenant   = cfg["TENANT"]
    adoption = cfg["ADOPTION"]
    psr      = cfg["PSR"]

    deu = data_extraction_utils()
    er  = entity_ranking()

    print(f"Running for: {client}")

    # -- Config data ---------------------------------------------------------
    print("Loading config data...")
    df_vwml = deu.get_widgetmeasureslist_from_config(config)
    df_md   = deu.get_measuredescriptions_from_config(config)
    df_da   = df_md   # Measure <-> DimAttr structural input via Grain column

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
    df_tenant_raw = pd.read_csv(tenant)
    df_tenant_stats, df_dimattr_stats = deu.get_measure_and_dim_attrs_stats_from_tenantlogs(df_tenant_raw)

    measure_scores = er.generate_measure_ranks_from_logs_data(df_tenant_stats)
    dimattr_scores = er.generate_dimattr_ranks_from_logs_data(df_dimattr_stats)

    # -- Adoption log stats (optional) ---------------------------------------
    print("Computing view interaction scores from adoption logs...")
    try:
        if not adoption:
            raise ValueError("No adoption file path set in config.txt")
        df_adoption_stats = deu.get_view_stats_from_adoptionlogs(pd.read_csv(adoption))
        view_scores       = er.generate_view_ranks_from_adoption_data(df_adoption_stats)
    except Exception as e:
        print(f"  WARNING: Adoption data unavailable - view scores will be zero. Reason: {e}")
        view_scores = pd.DataFrame(columns=["View", "interaction_score"])

    # -- PSR / ELK log stats (optional) --------------------------------------
    print("Computing widget interaction scores from PSR logs...")
    try:
        if not psr:
            raise ValueError("No PSR file path set in config.txt")
        df_psr_stats  = deu.get_widget_stats_from_psrlogs(pd.read_csv(psr, sep=","))
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