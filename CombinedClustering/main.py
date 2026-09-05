"""
Entity Clustering Pipeline
==========================
Inputs
------
semantic_file  : CSV/Excel  — LLM output  (MeasureName, Measure Description,
                              Business Capability, Attribute, Confidence)
tenant_file    : CSV        — measures_in_query_per_userid.csv
                              must have a 'Measures' column with list strings
config_md_file : CSV        — df_md.csv from data_utils
                              must have Measure, MeasureGroup, Grain columns
pagerank_file  : CSV        — measure_ranks_{CLIENT}.csv (optional)
                              columns: Measure, pagerank_score, spread_score

Outputs
-------
measure_clusters.csv  — one row per measure
cluster_names.csv     — one row per cluster
"""

import argparse
import numpy as np
import pandas as pd

from step1_structural     import build_structural_matrix
from step2_semantic       import build_semantic_matrix
from step3_behavioral     import build_behavioral_matrix
from step4_fusion         import fuse
from step5_cluster_naming import run_hdbscan, build_cluster_df, name_clusters_with_llm


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

WEIGHTS        = dict(w_struct=0.30, w_semantic=0.45, w_behavioral=0.25)
HDBSCAN_PARAMS = dict(min_cluster_size=3, min_samples=2)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ---------------------------------------------------------------------------
# Alignment helper
# ---------------------------------------------------------------------------

def align_behavioral_to_working_set(
    S_beh_full:   np.ndarray,
    beh_measures: list,
    working_set:  list,
) -> np.ndarray:
    """
    S_behavioral is N_log × N_log (only measures that appear in logs).
    working_set  is M measures (top-X from PageRank / semantic file).

    This function returns an M × M matrix where:
      - pairs both present in logs  → their PMI score
      - pairs where one/both absent → 0.0  (no behavioral signal, not penalised)
    """
    m = len(working_set)
    S_aligned = np.zeros((m, m), dtype=np.float32)
    np.fill_diagonal(S_aligned, 1.0)

    beh_idx = {name: i for i, name in enumerate(beh_measures)}

    for i, mi in enumerate(working_set):
        for j, mj in enumerate(working_set):
            if i == j:
                continue
            bi = beh_idx.get(mi)
            bj = beh_idx.get(mj)
            if bi is not None and bj is not None:
                S_aligned[i, j] = S_beh_full[bi, bj]
            # else: stays 0.0

    return S_aligned


def align_structural_to_working_set(
    config_md_df: pd.DataFrame,
    working_set:  list,
    mg_col:       str = "MeasureGroup",
    grain_col:    str = "Grain",
) -> np.ndarray:
    """
    df_md has one row per measure (config ground truth).
    working_set is the filtered M measures.

    Returns an M × M structural matrix indexed by working_set order.
    Measures absent from config get empty grain sets and unknown MG.
    """
    # Deduplicate config to one row per measure name
    config_deduped = (
        config_md_df
        .drop_duplicates(subset="Measure")
        .set_index("Measure")
    )

    # Build a sub-dataframe in working_set order
    rows = []
    for m in working_set:
        if m in config_deduped.index:
            row = config_deduped.loc[m]
            rows.append({
                "Measure":      m,
                mg_col:         row.get(mg_col, "__UNKNOWN__"),
                grain_col:      row.get(grain_col, ""),
            })
        else:
            rows.append({"Measure": m, mg_col: "__UNKNOWN__", grain_col: ""})

    aligned_df = pd.DataFrame(rows)
    return build_structural_matrix(aligned_df, mg_col=mg_col, grain_col=grain_col)


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_semantic(path: str) -> pd.DataFrame:
    df = pd.read_excel(path) if path.endswith(".xlsx") else pd.read_csv(path)
    required = ["MeasureName", "Measure Description",
                "Business Capability", "Attribute", "Confidence"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Semantic file missing columns: {missing}")
    return df.drop_duplicates(subset="MeasureName").reset_index(drop=True)


def reduce_to_top_x(df: pd.DataFrame, pagerank_path: str | None, top_x: int) -> pd.DataFrame:
    if pagerank_path is None:
        print(f"  No PageRank file — using all {len(df)} measures from semantic file.")
        return df

    pr = pd.read_csv(pagerank_path).sort_values("pagerank_score", ascending=False).head(top_x)
    top_measures = set(pr["Measure"].tolist())
    filtered = df[df["MeasureName"].isin(top_measures)].copy()

    if "spread_score" in pr.columns:
        pr_map = pr.set_index("Measure")["spread_score"].to_dict()
        filtered["spread_score"] = filtered["MeasureName"].map(pr_map)

    print(f"  Working set: {len(filtered)} / {len(df)} measures (top-{top_x} PageRank)")
    return filtered.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(
    semantic_file:   str,
    tenant_file:     str,
    config_md_file:  str,
    pagerank_file:   str | None = None,
    top_x:           int        = 80,
    output_dir:      str        = ".",
):
    # ── Step 0: working set ──────────────────────────────────────────────────
    print("\n=== Step 0 — Load & reduce working set ===")
    df           = load_semantic(semantic_file)
    df           = reduce_to_top_x(df, pagerank_file, top_x)
    working_set  = df["MeasureName"].tolist()
    n            = len(working_set)
    config_md_df = pd.read_csv(config_md_file)
    print(f"  N = {n} measures")

    # ── Step 1: Structural (aligned to working set) ──────────────────────────
    print("\n=== Step 1 — Structural matrix ===")
    S_struct = align_structural_to_working_set(config_md_df, working_set)
    assert S_struct.shape == (n, n), f"Structural shape mismatch: {S_struct.shape}"
    print(f"  S_struct  shape={S_struct.shape}  "
          f"mean_off_diag={np.mean(S_struct[~np.eye(n, dtype=bool)]):.3f}")

    # ── Step 2: Semantic ────────────────────────────────────────────────────
    print("\n=== Step 2 — Semantic matrix ===")
    S_semantic = build_semantic_matrix(df, model_name=EMBEDDING_MODEL)
    assert S_semantic.shape == (n, n), f"Semantic shape mismatch: {S_semantic.shape}"
    print(f"  S_semantic shape={S_semantic.shape}  "
          f"mean_off_diag={np.mean(S_semantic[~np.eye(n, dtype=bool)]):.3f}")

    # ── Step 3: Behavioral (aligned to working set) ──────────────────────────
    print("\n=== Step 3 — Behavioral matrix ===")
    tenant_df = pd.read_csv(tenant_file)
    S_beh_full, beh_measures = build_behavioral_matrix(tenant_df)
    S_behavioral = align_behavioral_to_working_set(S_beh_full, beh_measures, working_set)
    assert S_behavioral.shape == (n, n), f"Behavioral shape mismatch: {S_behavioral.shape}"
    nonzero = int(np.sum(S_behavioral[~np.eye(n, dtype=bool)] > 0))
    print(f"  S_behavioral shape={S_behavioral.shape}  non-zero pairs={nonzero}")
    if nonzero == 0:
        print("  WARNING: No behavioral overlap between working set and log measures.")
        print("  Behavioral signal will contribute nothing — consider adjusting top_x")

    # ── Step 4: Fusion ───────────────────────────────────────────────────────
    print("\n=== Step 4 — Fusion ===")
    S_fused, D_fused = fuse(S_struct, S_semantic, S_behavioral, **WEIGHTS)
    print(f"  S_fused shape={S_fused.shape}  "
          f"mean_off_diag={np.mean(S_fused[~np.eye(n, dtype=bool)]):.3f}")

    # ── Step 5a: HDBSCAN ─────────────────────────────────────────────────────
    print("\n=== Step 5a — HDBSCAN ===")
    clusterer  = run_hdbscan(D_fused, **HDBSCAN_PARAMS)
    labels     = clusterer.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise    = int(np.sum(labels == -1))
    print(f"  Clusters found: {n_clusters}  |  Noise (hub candidates): {n_noise}")
    print(f"  Label distribution: {dict(zip(*np.unique(labels, return_counts=True)))}")

    cluster_df = build_cluster_df(df, clusterer, D_fused=D_fused)



    # ── Outputs ──────────────────────────────────────────────────────────────
    final_measures = cluster_df

    measure_out = f"{output_dir}/measure_clusters.csv"
    names_out   = f"{output_dir}/cluster_names.csv"
    final_measures.to_csv(measure_out, index=False)
    print(f"\n  Saved: {measure_out}")
    print(f"  Saved: {names_out}")

    return final_measures


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Entity Clustering Pipeline")
    parser.add_argument("--semantic",    required=True)
    parser.add_argument("--tenant",      required=True,  help="measures_in_query_per_userid.csv")
    parser.add_argument("--config_md",   required=True,  help="df_md.csv from data_utils")
    parser.add_argument("--pagerank",    default=None)
    parser.add_argument("--top_x",       default=300,     type=int)
    parser.add_argument("--output_dir",  default=".")
    args = parser.parse_args()

    run_pipeline(
        semantic_file  = args.semantic,
        tenant_file    = args.tenant,
        config_md_file = args.config_md,
        pagerank_file  = args.pagerank,
        top_x          = args.top_x,
        output_dir     = args.output_dir
    )