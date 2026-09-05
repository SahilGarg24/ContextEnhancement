"""
L1 Structural Clustering
========================
Builds a weighted measure-to-measure graph from config data using
two structural signals, then runs community detection.

Signals (all normalised to [0,1] before combining):
  1. Shared grain   — IDF-weighted Jaccard similarity (penalises non-exact matches)
  2. Same MeasureGroup — same logical family

Widget signal has been moved to l1_behavioral (design intent lives there).
Graph is native to this data; no vector projection needed.
"""

import re
import numpy as np
import pandas as pd
import networkx as nx
from _community_detection import run_community_detection


# ---------------------------------------------------------------------------
# Grain parsing
# ---------------------------------------------------------------------------

def _parse_grain(grain_str: str) -> set:
    """
    '[Version].[Version Name], [Location].[Location]'
    → {'[version].[version name]', '[location].[location]'}
    """
    if pd.isna(grain_str) or not str(grain_str).strip():
        return set()
    matches = re.findall(r"\[(.*?)\]\.\[(.*?)\]", grain_str)
    return {f"[{d.strip().lower()}].[{a.strip().lower()}]" for d, a in matches}


def _grain_jaccard(s1: set, s2: set) -> float:
    """
    Penalised Jaccard:
      exact match  → 1.0   (full credit)
      partial match → 0.5 * jaccard   (halved — penalises partial overlap)
      no overlap   → 0.0
      empty grain  → 0.0   (no signal)

    Rationale: two MGs that differ by even one meaningful grain
    (e.g. time.week vs time.month for ST vs MT models) should NOT
    get the same score as an exact match.  Halving the partial score
    lets widget + MG signals dominate when grain is ambiguous.
    """
    if not s1 or not s2:
        return 0.0
    ovl = len(s1 & s2) / len(s1 | s2)
    return ovl if ovl == 1.0 else 0.5 * ovl


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_structural_graph(
    df_md:           pd.DataFrame,
    working_set:     list,
    w_grain:         float = 0.60,
    w_mg:            float = 0.40,
    min_edge_weight: float = 0.0,
) -> nx.Graph:
    """
    Parameters
    ----------
    df_md           : Measure metadata
                      required columns: 'Measure', 'MeasureGroup', 'Grain'
    working_set     : ordered list of measure names to cluster
    w_grain         : weight for IDF-penalised grain Jaccard  (default 0.60)
    w_mg            : weight for same-MeasureGroup indicator  (default 0.40)
                      w_grain + w_mg must equal 1.0
    min_edge_weight : edges below this threshold are dropped

    Returns
    -------
    G : nx.Graph with nodes = working_set, edge attr 'weight'
    """
    # BUG FIX 1: assert now matches the TWO weights that are actually used.
    # Previously run_structural_clustering passed w_grain + w_mg (summing to 0.50
    # with old defaults) but build_structural_graph asserted they sum to 1.0 →
    # AssertionError on every call with default parameters.
    assert abs(w_grain + w_mg - 1.0) < 1e-6, \
        f"w_grain + w_mg must equal 1.0, got {w_grain + w_mg:.4f}"

    # --- Measure metadata lookup ---
    md_idx    = df_md.drop_duplicates("Measure").set_index("Measure")
    grain_map = {
        m: _parse_grain(md_idx.loc[m, "Grain"])
        if m in md_idx.index else set()
        for m in working_set
    }
    mg_map    = {
        m: str(md_idx.loc[m, "MeasureGroup"])
        if m in md_idx.index and "MeasureGroup" in md_idx.columns else "__UNKNOWN__"
        for m in working_set
    }

    # --- Build graph ---
    G = nx.Graph()
    G.add_nodes_from(working_set)

    n = len(working_set)
    for i in range(n):
        mi = working_set[i]
        for j in range(i + 1, n):
            mj = working_set[j]

            w_g = _grain_jaccard(grain_map[mi], grain_map[mj])
            w_m = 1.0 if (mg_map[mi] == mg_map[mj]
                          and mg_map[mi] != "__UNKNOWN__") else 0.0

            weight = w_grain * w_g + w_mg * w_m
            if weight > min_edge_weight:
                G.add_edge(mi, mj, weight=weight)

    return G


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_structural_clustering(
    df_md:           pd.DataFrame,
    working_set:     list,
    w_grain:         float = 0.60,   # BUG FIX 1: updated default so w_grain + w_mg = 1.0
    w_mg:            float = 0.40,   # (was 0.30 + 0.20 = 0.50, always failed the assert)
    min_edge_weight: float = 0.0,
    algorithm:       str   = "hdbscan_diffusion",
    **kwargs,
) -> tuple[dict, nx.Graph]:
    """
    Full structural pipeline.

    NOTE: w_widget has been removed from this module.
    Widget co-occurrence is now a signal in l1_behavioral only,
    where it penalises query co-occurrence pairs that have no
    widget design intent behind them.

    algorithm choices
    -----------------
    "louvain"           NetworkX Louvain
    "leiden"            leidenalg — set leiden_partition and leiden_n_iterations in kwargs
    "hdbscan_diffusion" Diffusion distance → HDBSCAN  (recommended for dense graphs)
    "hdbscan_node2vec"  node2vec embeddings → HDBSCAN
    "mcl"               Markov Cluster Algorithm

    All algorithm-specific parameters (resolution, min_cluster_size,
    diffusion_t, n2v_*, mcl_*, etc.) are passed through **kwargs
    directly to the dispatcher.
    """
    G = build_structural_graph(
        df_md, working_set,
        w_grain=w_grain, w_mg=w_mg,
        min_edge_weight=min_edge_weight,
    )

    labels = run_community_detection(G, algorithm=algorithm, **kwargs)

    n_clusters = len({v for v in labels.values() if v != -1})
    n_isolated = sum(1 for v in labels.values() if v == -1)
    print(f"  Graph     : {G.number_of_nodes()} nodes  {G.number_of_edges()} edges")
    print(f"  Structural [{algorithm}]: {n_clusters} clusters  |  {n_isolated} noise/isolated")

    return labels, G