"""
L1 Behavioral Clustering
========================
Builds a sparse weighted graph from PMI-normalised measure
co-occurrence in tenant query logs, then runs community detection.

Why graph-based (not HDBSCAN directly) here:
  - The data is fundamentally a graph: measures are nodes,
    co-occurrence is the edge. No natural vector space exists.
  - PMI matrices are sparse — most pairs have PMI=0 (never co-occurred).
    HDBSCAN on a precomputed distance matrix full of 1.0s would
    collapse most measures to noise.
  - Isolated nodes (measures absent from logs) simply have no edges
    and get label -1.
  - Thresholding PMI > min_pmi gives explicit control over
    what counts as a behavioural signal vs noise.

Input
-----
df          : DataFrame with a 'Measures' column containing
              list-strings of measure names per query,
              e.g. "['Adjusted Forecast', 'LY Sales']"
              (the measures_in_query_per_userid.csv format)
working_set : ordered list of measures to cluster
              Only co-occurrences within this set are counted.
"""

import ast
import numpy as np
import pandas as pd
import networkx as nx
from _community_detection import run_community_detection


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _parse_measure_list(s) -> list:
    try:
        return list(ast.literal_eval(s))
    except Exception:
        return []


# ---------------------------------------------------------------------------
# PMI graph
# ---------------------------------------------------------------------------

def penalize_w_non_cooc(w_co: dict, m1: str, m2: str) -> float:
    """
    Returns 0.5 if the measure pair (m1, m2) never appeared
    together on any widget, penalising query co-occurrence that
    has no design intent behind it.

    Parameters
    ----------
    w_co : dict {(measure_a, measure_b): count}  — widget co-occurrence counts
           Keys are sorted tuples of measure NAME strings.
    m1, m2 : measure name strings  ← must be names, NOT integer indices
    """
    key   = tuple(sorted([m1, m2]))
    c_val = w_co.get(key, 0)          # BUG FIX 3: was w_co[key] → KeyError
                                       # if pair never shared a widget
    return 1.0 if c_val > 0 else 0.5


def build_behavioral_graph(
    df:           pd.DataFrame,
    df_vwml:      pd.DataFrame,
    working_set:  list,
    measure_col:  str   = "Measures",
    min_pmi:      float = 0.10,
) -> nx.Graph:
    """
    Build sparse PMI co-occurrence graph restricted to working_set.

    Edge weight = normalised positive PMI (PPMI), clipped at min_pmi.
    Measures absent from logs or below the PMI threshold become
    isolated nodes (degree = 0).
    """
    # BUG FIX 4: use working_set (ordered list) as the single source of truth
    # for node ordering throughout — never convert to set for indexing.
    # set(working_set) loses insertion order, which caused ws_idx indices
    # to disagree with working_set[i] lookups in the final edge loop.
    n      = len(working_set)
    ws_idx = {m: i for i, m in enumerate(working_set)}   # name → row/col index
    ws_set = set(working_set)                              # only used for O(1) membership tests
    co     = np.zeros((n, n), dtype=np.float64)

    # --- Widget co-occurrence (used to penalise PMI of non-co-designed pairs) ---
    widget_co: dict[tuple, int] = {}
    wm = df_vwml[df_vwml["Measure"].isin(ws_set)]
    for _, grp in wm.groupby("Widget")["Measure"]:
        uniq = list(set(grp))
        for a in range(len(uniq)):
            for b in range(a + 1, len(uniq)):
                key = tuple(sorted([uniq[a], uniq[b]]))
                widget_co[key] = widget_co.get(key, 0) + 1

    # --- Query co-occurrence counts ---
    queries = df[measure_col].dropna().apply(_parse_measure_list)
    for q in queries:
        idxs = list({ws_idx[m] for m in q if m in ws_idx})
        if len(idxs) < 2:
            continue
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                i, j = idxs[a], idxs[b]
                co[i, j] += 1
                co[j, i] += 1

    G = nx.Graph()
    G.add_nodes_from(working_set)                          # BUG FIX 4: was ws_set (unordered)

    total = co.sum()
    if total == 0:
        print("  WARNING: no co-occurrence found within working set")
        return G

    # P(i,j) — joint probability of measures i and j appearing together
    P_joint = co / total

    # --- Widget-penalise P_joint ---
    # BUG FIX 1+2: was `for a in range(len(ws_set))` with `ws_idx[a]`
    #   ws_idx maps measure_name → int, NOT int → int, so ws_idx[0] raises KeyError.
    #   Also, penalize_w_non_cooc needs measure NAME strings, not integer indices.
    #   Fix: iterate over working_set directly to get names, then look up indices.
    for a in range(n):
        ma = working_set[a]
        for b in range(a + 1, n):
            mb = working_set[b]
            penalty = penalize_w_non_cooc(widget_co, ma, mb)   # pass names ✅
            P_joint[a, b] *= penalty
            P_joint[b, a] *= penalty                           # maintain symmetry

    # P_marginal[k] = marginal probability of measure k appearing in any pair.
    # Because co is symmetric, co.sum(axis=1) == co.sum(axis=0), so one
    # vector covers both dimensions.
    #
    # np.outer(P_marginal, P_marginal)[i,j]
    #   = P_marginal[i] * P_marginal[j]
    #   = P(measure_i) * P(measure_j)          ← correct PMI denominator
    #
    # This is NOT P_marginal² — the outer product of a vector with itself
    # gives element [i,j] = v[i]*v[j], which is P(i)*P(j) for i ≠ j.
    # PMI is symmetric: PMI[i,j] == PMI[j,i] because both P_joint and
    # the denominator are symmetric.
    P_marginal = co.sum(axis=1) / total
    denom      = np.outer(P_marginal, P_marginal) + 1e-12  # P(i) * P(j)

    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log(P_joint / denom)

    ppmi = np.clip(pmi, 0.0, None)
    if ppmi.max() > 0:
        ppmi = ppmi / ppmi.max()      # normalise to [0,1]

    # BUG FIX 4 (continued): working_set[i] now correctly aligns with
    # ppmi[i, j] because both use the same working_set ordering.
    for i in range(n):
        for j in range(i + 1, n):
            if ppmi[i, j] > min_pmi:
                G.add_edge(working_set[i], working_set[j], weight=float(ppmi[i, j]))

    return G


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_behavioral_clustering(
    df:           pd.DataFrame,
    df_wml:       pd.DataFrame,
    working_set:  list,
    measure_col:  str   = "Measures",
    min_pmi:      float = 0.10,
    algorithm:    str   = "hdbscan_diffusion",
    **kwargs,
) -> tuple[dict, nx.Graph]:
    """
    Full behavioral pipeline.

    Same algorithm choices and **kwargs forwarding as l1_structural.
    min_cluster_size defaults lower than structural (sparser graph).

    Returns
    -------
    labels : dict {measure_name: cluster_id}  (−1 = absent from logs / noise)
    G      : constructed PMI graph (for inspection)
    """
    G      = build_behavioral_graph(df, df_wml, working_set, measure_col, min_pmi)
    labels = run_community_detection(G, algorithm=algorithm, **kwargs)

    n_clusters = len({v for v in labels.values() if v != -1})
    n_absent   = sum(1 for v in labels.values() if v == -1)
    coverage   = 100 * (len(working_set) - n_absent) / len(working_set)
    print(f"  Graph     : {G.number_of_nodes()} nodes  {G.number_of_edges()} edges")
    print(f"  Behavioral [{algorithm}]: {n_clusters} clusters  |  "
          f"{n_absent} noise/absent  ({coverage:.0f}% coverage)")

    return labels, G