"""
Hierarchical Entity Clustering Pipeline
========================================
Three independent L1 clusterings → co-association meta-clustering (L2).

Algorithm choices for structural and behavioral:
  "louvain"            NetworkX Louvain
  "leiden"             Leiden (RBConfiguration / CPM / Modularity)
  "hdbscan_diffusion"  Diffusion distance matrix → HDBSCAN  [recommended]
  "hdbscan_node2vec"   node2vec embeddings → HDBSCAN
  "mcl"                Markov Cluster Algorithm

Scoping
-------
  L1 Semantic  : runs on ALL measures in the semantic file (sem_df_full),
                 regardless of the pipeline's working set.
  L2 Meta      : runs only on the intersection of working_set and
                 sem_df_full (sem_ws), because every meta-graph node
                 needs a valid Business Capability embedding.
  Final output : covers ALL measures in working_set.  Measures outside
                 the semantic intersection receive meta_cluster = -1
                 via the signal_agreement_report fallback.
"""

import argparse
import numpy as np
import pandas as pd

from l1_structural  import run_structural_clustering
from l1_semantic    import run_semantic_clustering
from l1_behavioral  import run_behavioral_clustering
from l2_meta        import run_meta_clustering


# ─────────────────────────────────────────────────────────────────────────────
# Tunable parameters
# All keys for all algorithms live here.
# Each algorithm reads only the keys it needs — the rest are silently ignored.
# Switch algorithm by changing the "algorithm" key — nothing else required.
# ─────────────────────────────────────────────────────────────────────────────

STRUCTURAL_PARAMS = dict(

    # ── graph construction ─────────────────────────────────────────────────
    w_grain          = 0.8,   # weight of grain Jaccard similarity
    w_mg             = 0.2,   # weight of same MeasureGroup
    min_edge_weight  = 0.0,    # drop edges below this (0 = keep all)

    # ── algorithm selection ────────────────────────────────────────────────
    # "louvain" | "leiden" | "hdbscan_diffusion" | "hdbscan_node2vec" | "mcl"
    algorithm        = "hdbscan_diffusion",

    # ── louvain ───────────────────────────────────────────────────────────
    resolution       = 1.0,    # γ — higher → more clusters
    seed             = 42,

    # ── leiden ────────────────────────────────────────────────────────────
    leiden_partition      = "CPM",   # "RBConfiguration" | "CPM" | "Modularity"
    leiden_n_iterations   = 100,

    # ── hdbscan (both diffusion and node2vec) ─────────────────────────────
    min_cluster_size       = 5,    # no cluster smaller than this is formed
    min_samples            = 5,    # controls noise sensitivity
    hdbscan_selection_method = "eom",  # "eom" | "leaf"
    cluster_selection_epsilon=0.00625,     # once pairs are within this distance, merge them

    # ── hdbscan_diffusion ─────────────────────────────────────────────────
    diffusion_t      = 5,     # random walk steps (2–5); higher → smoother

    # ── hdbscan_node2vec ──────────────────────────────────────────────────
    # p=0.5, q=2 → BFS-biased (community detection; recommended)
    # p=1,   q=1 → neutral (DeepWalk)
    # p=2,   q=0.5 → DFS-biased (structural roles)
    n2v_dimensions   = 64,
    n2v_walk_length  = 10,
    n2v_num_walks    = 100,
    n2v_p            = 2.0,
    n2v_q            = 2.0,
    n2v_window       = 5,

    # ── mcl ───────────────────────────────────────────────────────────────
    # inflation: higher → smaller, more clusters  (try 1.5 – 4.0)
    # expansion: random walk length  (almost always 2)
    mcl_inflation         = 6.0,
    mcl_expansion         = 10,
    mcl_iterations        = 100,
    mcl_pruning_threshold = 0.0001,
)

SEMANTIC_PARAMS = dict(
    w_cap_desc               = 0.5,
    w_cap                    = 0.5,
    model_name               = "all-MiniLM-L6-v2",
    min_cluster_size         = 5,
    cluster_selection_method = "eom",
)

BEHAVIORAL_PARAMS = dict(

    # ── graph construction ─────────────────────────────────────────────────
    min_pmi          = 0.00,   # drop PMI edges below this

    # ── algorithm selection ────────────────────────────────────────────────
    algorithm        = "hdbscan_diffusion",

    # ── louvain ───────────────────────────────────────────────────────────
    resolution       = 1.0,
    seed             = 42,

    # ── leiden ────────────────────────────────────────────────────────────
    leiden_partition      = "RBConfiguration",
    leiden_n_iterations   = 100,

    # ── hdbscan (both variants) ───────────────────────────────────────────
    min_cluster_size       = 5,    # lower than structural — behavioral graph sparser
    min_samples            = 5,
    hdbscan_selection_method = "eom",
    cluster_selection_epsilon=0.0,

    # ── hdbscan_diffusion ─────────────────────────────────────────────────
    diffusion_t      = 5,

    # ── hdbscan_node2vec ──────────────────────────────────────────────────
    n2v_dimensions   = 64,
    n2v_walk_length  = 10,
    n2v_num_walks    = 100,
    n2v_p            = 0.5,
    n2v_q            = 2.0,
    n2v_window       = 5,

    # ── mcl ───────────────────────────────────────────────────────────────
    mcl_inflation         = 1.2,
    mcl_expansion         = 3,
    mcl_iterations        = 100,
    mcl_pruning_threshold = 0.001,
)

META_PARAMS = dict(
    # ── graph construction ─────────────────────────────────────────────────
    w_grain          = 0.40,   # weight of grain Jaccard similarity
    w_mg             = 0.10,   # weight of same MeasureGroup
    w_cap            = 0.50,   # weight of the combined semantic cosine channel
    # w_cap_desc: within the cap channel, description vs capability-name cosine.
    # 0.0 = capability name only  |  0.5 = equal blend (recommended)  |  1.0 = description only
    # Higher values help separate ST/MT variants of the same measure type whose
    # capability names are near-identical but whose descriptions diverge.
    w_cap_desc       = 0.50,
    min_edge_weight  = 0.0,    # drop edges below this (0 = keep all)

    # ── algorithm selection ────────────────────────────────────────────────
    # "louvain" | "leiden" | "hdbscan_diffusion" | "hdbscan_node2vec" | "mcl"
    algorithm="hdbscan_diffusion",

    # ── louvain ───────────────────────────────────────────────────────────
    resolution=1.0,  # γ — higher → more clusters
    seed=42,

    # ── leiden ────────────────────────────────────────────────────────────
    leiden_partition="CPM",  # "RBConfiguration" | "CPM" | "Modularity"
    leiden_n_iterations=100,

    # ── hdbscan (both diffusion and node2vec) ─────────────────────────────
    min_cluster_size=5,  # no cluster smaller than this is formed
    min_samples=5,  # controls noise sensitivity
    hdbscan_selection_method="leaf",  # "eom" | "leaf"
    cluster_selection_epsilon=0.00225,

    # ── hdbscan_diffusion ─────────────────────────────────────────────────
    diffusion_t=3,  # random walk steps (2–5); higher → smoother

    # ── hdbscan_node2vec ──────────────────────────────────────────────────
    # p=0.5, q=2 → BFS-biased (community detection; recommended)
    # p=1,   q=1 → neutral (DeepWalk)
    # p=2,   q=0.5 → DFS-biased (structural roles)
    n2v_dimensions=64,
    n2v_walk_length=10,
    n2v_num_walks=100,
    n2v_p=2.0,
    n2v_q=2.0,
    n2v_window=5,

    # ── mcl ───────────────────────────────────────────────────────────────
    # inflation: higher → smaller, more clusters  (try 1.5 – 4.0)
    # expansion: random walk length  (almost always 2)
    mcl_inflation=6.0,
    mcl_expansion=10,
    mcl_iterations=100,
    mcl_pruning_threshold=0.0001,
)

PAGERANK_TOP_X = 300


# ─────────────────────────────────────────────────────────────────────────────
# Loaders
# ─────────────────────────────────────────────────────────────────────────────

def _load_semantic(path: str) -> pd.DataFrame:
    df = pd.read_excel(path) if path.endswith(".xlsx") else pd.read_csv(path)
    required = ["MeasureName", "Measure Description", "Business Capability"]
    missing  = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Semantic file missing columns: {missing}")
    return df.drop_duplicates("MeasureName").reset_index(drop=True)


def _working_set_from_pagerank(pagerank_path: str | None, top_x: int) -> list | None:
    if pagerank_path is None:
        return None
    pr = pd.read_csv(pagerank_path).sort_values("pagerank_score", ascending=False).head(top_x)
    return pr["Measure"].str.strip().tolist()


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline
# ─────────────────────────────────────────────────────────────────────────────

def run_pipeline(
    semantic_file:   str,
    beh_file:        str,
    config_md_file:  str,
    config_wml_file: str,
    pagerank_file:   str | None = None,
    top_x:           int        = PAGERANK_TOP_X,
    output_dir:      str        = ".",
):
    print(f"Structural: "
          f"ms-{STRUCTURAL_PARAMS.get('min_samples')} ; "
          f"t-{STRUCTURAL_PARAMS.get('diffusion_t')} ; "
          f"cse - {STRUCTURAL_PARAMS.get('cluster_selection_epsilon')}")

    print(f"Behavioral: "
          f"ms-{BEHAVIORAL_PARAMS.get('min_samples')} ; "
          f"t-{BEHAVIORAL_PARAMS.get('diffusion_t')} ; "
          f"cse - {BEHAVIORAL_PARAMS.get('cluster_selection_epsilon')}")

    print(f"Meta: "
          f"ms-{META_PARAMS.get('min_samples')} ; "
          f"t-{META_PARAMS.get('diffusion_t')} ; "
          f"cse - {META_PARAMS.get('cluster_selection_epsilon')}")

    # ── Step 0: working set ──────────────────────────────────────────────────
    print("\n=== Step 0 — Load & reduce working set ===")
    sem_df_full = _load_semantic(semantic_file)
    sem_names_check = set(sem_df_full["MeasureName"].str.strip().str.lower().tolist())

    pagerank_ws = _working_set_from_pagerank(pagerank_file, top_x)
    if pagerank_ws is not None:
        working_set = pagerank_ws
        print(f"  Working set : {len(working_set)} measures (top-{top_x} PageRank)")
    else:
        working_set = sem_df_full["MeasureName"].str.strip().tolist()
        print(f"  No PageRank — using all {len(working_set)} semantic measures.")

    # sem_ws    : intersection of working_set and semantic file
    #             → meta's working set (every node needs a capability embedding)
    # no_sem    : in working_set but no semantic row → sem/meta = -1 in output
    # sem_only  : in semantic file but NOT in working_set → struct/beh/meta = -1
    # outer_set : union (working_set first, sem_only appended) → all output rows
    ws_set    = set(working_set)
    sem_ws    = [m for m in working_set if m.lower() in sem_names_check]
    no_sem    = [m for m in working_set if m.lower() not in sem_names_check]
    sem_only  = [m for m in sem_df_full["MeasureName"].str.strip().tolist()
                 if m not in ws_set]
    outer_set = working_set + sem_only

    # sem_df  : semantic rows for the intersection (used by meta)
    sem_df = sem_df_full[
        sem_df_full["MeasureName"].str.strip().isin(set(sem_ws))
    ].copy().reset_index(drop=True)

    print(f"  Semantic coverage : {len(sem_ws)} / {len(working_set)} in working set")
    print(f"  Semantic-only     : {len(sem_only)} (sem_cluster only, rest = -1)")
    print(f"  Outer set total   : {len(outer_set)}")
    if no_sem:
        print(f"  No semantic       : {no_sem}")

    n       = len(working_set)
    df_md   = pd.read_csv(config_md_file)
    df_vwml = pd.read_csv(config_wml_file)
    beh_df  = pd.read_csv(beh_file)
    print(f"  N (working set) = {n}  |  N (meta intersection) = {len(sem_ws)}  |  N (outer set) = {len(outer_set)}")

    # ── L1a: Structural ──────────────────────────────────────────────────────
    algo_s = STRUCTURAL_PARAMS["algorithm"]
    print(f"\n=== L1a — Structural  [{algo_s}] ===")
    struct_labels, struct_G = run_structural_clustering(
        df_md, working_set, **STRUCTURAL_PARAMS
    )

    # ── L1b: Semantic ─────────────────────────────────────────────────────────
    # Runs on ALL measures in the semantic file (sem_df_full), not just those
    # in the pipeline's working set.  This gives the richest possible embedding
    # space for the semantic signal.
    print("\n=== L1b — Semantic  [HDBSCAN on embedding — ALL semantic measures] ===")
    sem_labels, sem_D_partial = run_semantic_clustering(sem_df_full, **SEMANTIC_PARAMS)

    # Expand partial (N_sem × N_sem) → full (N × N) for downstream visualisation.
    # Pairs with no semantic data stay at 1.0 (= maximum distance).
    # BUG FIX: enumerate(sem_df_full) iterates column names, not measure names.
    #          Use the actual MeasureName series instead.
    sem_full_names = sem_df_full["MeasureName"].str.strip().tolist()
    sem_idx        = {m: i for i, m in enumerate(sem_full_names)}
    sem_D          = np.ones((n, n), dtype=np.float64)
    np.fill_diagonal(sem_D, 0.0)
    for i, mi in enumerate(working_set):
        for j, mj in enumerate(working_set):
            if mi in sem_idx and mj in sem_idx:
                sem_D[i, j] = sem_D_partial[sem_idx[mi], sem_idx[mj]]

    # ── L1c: Behavioral ──────────────────────────────────────────────────────
    algo_b = BEHAVIORAL_PARAMS["algorithm"]
    print(f"\n=== L1c — Behavioral  [{algo_b}] ===")
    beh_labels, beh_G = run_behavioral_clustering(
        beh_df, df_vwml, working_set, **BEHAVIORAL_PARAMS
    )

    # ── L1 summary ───────────────────────────────────────────────────────────
    print("\n=== L1 summary ===")
    for name, lab in [("Structural", struct_labels),
                      ("Semantic",   sem_labels),
                      ("Behavioral", beh_labels)]:
        cids   = [v for v in lab.values() if v != -1]
        n_c    = len(set(cids))
        n_noise= sum(1 for v in lab.values() if v == -1)
        if cids:
            from collections import Counter
            sizes = sorted(Counter(cids).values(), reverse=True)
            print(f"  {name:12s}: {n_c} clusters  sizes={sizes}  noise={n_noise}")
        else:
            print(f"  {name:12s}: 0 clusters  noise={n_noise}")

    # ── L2: Meta-clustering ──────────────────────────────────────────────────
    # Meta runs on sem_ws (the intersection), NOT the full working_set,
    # because every meta-graph node needs a valid Business Capability embedding.
    # Measures in working_set but outside sem_ws appear in the final output
    # with meta_cluster = -1 via dict.get(m, -1) below.
    print(f"\n=== L2 — Meta-clustering [unified graph + community detection] ===")
    print(f"  Running on intersection: {len(sem_ws)} of {n} measures")
    meta_labels, meta_G = run_meta_clustering(
        df_md, sem_df, sem_ws, **META_PARAMS   # ← sem_ws, not working_set
    )

    # Build output — outer_set: all measures from working_set UNION sem_df_full.
    # Measures only in sem_df_full get struct/beh/meta = -1.
    # Measures only in working_set (no_sem) get sem/meta = -1.
    report_df = pd.DataFrame([
        {
            "measure":        m,
            "meta_cluster":   meta_labels.get(m, None),
            "struct_cluster": struct_labels.get(m, None),
            "sem_cluster":    sem_labels.get(m, None),
            "beh_cluster":    beh_labels.get(m, None),
        }
        for m in outer_set
    ])

    cids    = [v for v in meta_labels.values() if v != -1]
    n_meta  = len(set(cids))
    n_cross = sum(1 for v in meta_labels.values() if v == -1)
    if cids:
        from collections import Counter
        sizes = sorted(Counter(cids).values(), reverse=True)
        print(f"  Meta: {n_meta} clusters  sizes={sizes}")
    else:
        print(f"  Meta: 0 clusters  noise={n_cross}")
    print(f"  Meta-clusters : {n_meta}")
    print(f"  Cross-cutting : {n_cross}")
    print(f"  Outside meta  : {len(no_sem)} (no semantic data → meta_cluster=-1 in output)")

    # ── Write output ──────────────────────────────────────────────────────────
    out = f"{output_dir}/measure_clusters.csv"
    report_df.to_csv(out, index=False)
    print(f"\n  Saved: {out}  ({len(report_df)} rows = full outer set)")

    return report_df, meta_G, struct_G, beh_G, sem_D


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--semantic",    required=True)
    parser.add_argument("--beh",         required=True)
    parser.add_argument("--config_md",   required=True)
    parser.add_argument("--config_wml",  required=True)
    parser.add_argument("--pagerank",    default=None)
    parser.add_argument("--top_x",       default=PAGERANK_TOP_X, type=int)
    parser.add_argument("--output_dir",  default=".")
    parser.add_argument("--visualise",   action="store_true")
    args = parser.parse_args()

    final, meta_G, struct_G, beh_G, sem_D = run_pipeline(
        semantic_file    = args.semantic,
        beh_file         = args.beh,
        config_md_file   = args.config_md,
        config_wml_file  = args.config_wml,
        pagerank_file    = args.pagerank,
        top_x            = args.top_x,
        output_dir       = args.output_dir,
    )

    if args.visualise:
        from visualise import build_visualisation
        working_set   = final["measure"].tolist()
        struct_labels = dict(zip(final["measure"], final["struct_cluster"]))
        sem_labels    = dict(zip(final["measure"], final["sem_cluster"]))
        beh_labels    = dict(zip(final["measure"], final["beh_cluster"]))

        build_visualisation(
            struct_G      = struct_G,
            struct_labels = struct_labels,
            sem_S         = 1 - sem_D,
            sem_measures  = working_set,
            sem_labels    = sem_labels,
            beh_G         = beh_G,
            beh_labels    = beh_labels,
            df_vwml       = pd.read_csv(args.config_wml),
            df_md         = pd.read_csv(args.config_md),
            beh_df        = pd.read_csv(args.beh),
            working_set   = working_set,
            struct_params = STRUCTURAL_PARAMS,
            beh_params    = BEHAVIORAL_PARAMS,
            output_path   = f"{args.output_dir}/clustering_vis.html",
        )