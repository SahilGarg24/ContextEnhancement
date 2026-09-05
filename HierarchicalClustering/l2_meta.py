"""
L2 Meta-Clustering
==================
Builds a combined graph from structural + semantic signals and runs
community detection to produce final meta-clusters.

Graph signals
-------------
  w_grain : IDF-penalised grain Jaccard (same as structural)
  w_mg    : same MeasureGroup indicator
  w_cap   : cosine similarity on Business Capability embeddings
            (consistent with l1_semantic — purely vector-space,
             no count-based component)
            w_grain + w_mg + w_cap must equal 1.0

Scope
-----
  build_meta_graph / run_meta_clustering operate on whatever
  working_set is passed in.  The caller (main_hierarchical) is
  responsible for restricting that to the semantic-intersection set
  so that every measure has a valid capability embedding.  Measures
  outside the intersection are not passed here; they receive label -1
  via the signal_agreement_report's dict.get(m, -1) fallback.

HDBSCAN on diffusion distance:
  - Measures that consistently land in different clusters across
    all signals → HDBSCAN noise (−1) = confirmed hub/cross-cutting
  - min_cluster_size controls how many measures must agree to form
    a stable domain
"""

import numpy as np
import pandas as pd
import re
import networkx as nx
from _community_detection import run_community_detection
from sentence_transformers import SentenceTransformer


_MODEL_CACHE: dict = {}


def _get_model(name: str) -> SentenceTransformer:
    if name not in _MODEL_CACHE:
        print(f"  Loading embedding model: {name}")
        _MODEL_CACHE[name] = SentenceTransformer(name)
    return _MODEL_CACHE[name]


def _cosine_matrix(emb: np.ndarray) -> np.ndarray:
    norms  = np.linalg.norm(emb, axis=1, keepdims=True)
    normed = emb / np.maximum(norms, 1e-9)
    return np.clip(normed @ normed.T, -1.0, 1.0).astype(np.float32)


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
    Penalised Jaccard — exact match scores 1.0, partial scores 0.5×jaccard.
    See l1_structural for full rationale.
    """
    if not s1 or not s2:
        return 0.0
    ovl = len(s1 & s2) / len(s1 | s2)
    return ovl if ovl == 1.0 else 0.5 * ovl


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_meta_graph(
    df_md:           pd.DataFrame,
    sem_df:          pd.DataFrame,
    working_set:     list,
    model_name:      str   = "all-MiniLM-L6-v2",
    w_grain:         float = 0.40,
    w_mg:            float = 0.10,
    w_cap:           float = 0.50,
    w_cap_desc:      float = 0.50,
    min_edge_weight: float = 0.0,
) -> nx.Graph:
    """
    Parameters
    ----------
    df_md           : Measure metadata
                      required columns: 'Measure', 'MeasureGroup', 'Grain'
    sem_df          : Semantic data with Business Capability labels
                      required columns: 'MeasureName', 'Measure Description',
                                        'Business Capability'
    working_set     : ordered list of measure names to cluster
                      Caller must ensure every measure here has a row in sem_df
                      so the capability embedding is defined.
    w_grain         : weight for grain Jaccard signal
    w_mg            : weight for same-MeasureGroup signal
    w_cap           : weight for the combined semantic cosine channel
                      w_grain + w_mg + w_cap must equal 1.0
    w_cap_desc      : within the cap channel, weight given to measure-description
                      cosine vs capability-name cosine.  Must be in [0, 1].
                        0.0 → capability name only  (original behaviour)
                        0.5 → equal blend           (recommended default)
                        1.0 → description only
                      Blending description catches near-identical capability names
                      that should be separated (e.g. ST vs MT variants of the
                      same forecast type): their descriptions diverge even when
                      their capability name is identical.
    min_edge_weight : edges below this threshold are dropped

    Returns
    -------
    G : nx.Graph with nodes = working_set, edge attr 'weight'
    """
    assert abs(w_grain + w_mg + w_cap - 1.0) < 1e-6, \
        f"w_grain + w_mg + w_cap must equal 1.0, got {w_grain + w_mg + w_cap:.4f}"
    assert 0.0 <= w_cap_desc <= 1.0, \
        f"w_cap_desc must be in [0, 1], got {w_cap_desc}"

    sem_idx = sem_df.set_index("MeasureName")

    # --- Capability-name cosine ---
    cap_list = [sem_idx.loc[m, "Business Capability"]
                if m in sem_idx.index else ""
                for m in working_set]

    # --- Description cosine ---
    desc_col = "Measure Description"
    desc_list = [sem_idx.loc[m, desc_col]
                 if m in sem_idx.index else ""
                 for m in working_set]

    model = _get_model(model_name)
    emb_caps = model.encode(cap_list,  show_progress_bar=False, convert_to_numpy=True)
    emb_desc = model.encode(desc_list, show_progress_bar=False, convert_to_numpy=True)

    cos_cap_name = np.clip(_cosine_matrix(emb_caps), 0.0, 1.0)
    cos_cap_desc = np.clip(_cosine_matrix(emb_desc), 0.0, 1.0)

    # Blend: description pulls apart ST/MT variants that share a capability name
    cos_combined = (w_cap_desc * cos_cap_desc
                    + (1.0 - w_cap_desc) * cos_cap_name)

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
            w_c = float(cos_combined[i, j])

            weight = w_grain * w_g + w_mg * w_m + w_cap * w_c
            if weight > min_edge_weight:
                G.add_edge(mi, mj, weight=weight)

    return G


# ---------------------------------------------------------------------------
# Meta clustering entry point
# ---------------------------------------------------------------------------

def run_meta_clustering(
    df_md:           pd.DataFrame,
    sem_df:          pd.DataFrame,
    working_set:     list,
    w_grain:         float = 0.40,
    w_mg:            float = 0.10,
    w_cap:           float = 0.50,
    w_cap_desc:      float = 0.50,
    min_edge_weight: float = 0.0,
    algorithm:       str   = "hdbscan_diffusion",
    **kwargs,
) -> tuple[dict, nx.Graph]:
    """
    Full meta-clustering pipeline.

    The capability signal is now pure cosine similarity on Business
    Capability embeddings — no count-based component.  w_grain + w_mg
    + w_cap must equal 1.0.

    working_set should be the intersection of the pipeline's working
    set and the semantic file's measures.  The caller (main_hierarchical)
    handles this scoping; measures outside the intersection are not
    present in the returned labels dict and get label -1 via a
    dict.get(m, -1) fallback in the caller.

    Parameters
    ----------
    df_md           : Measure metadata
    sem_df          : Semantic data with Business Capability labels
    working_set     : ordered list of measures to cluster (intersection)
    w_*             : graph signal weights (must sum to 1.0)
    min_edge_weight : edges below this are dropped
    algorithm       : community detection algorithm key
    **kwargs        : passed through to run_community_detection

    Returns
    -------
    labels : dict {measure_name: cluster_id}  (−1 = cross-cutting / noise)
    G      : the meta graph (for inspection)
    """
    G = build_meta_graph(
        df_md, sem_df, working_set,
        w_grain=w_grain, w_mg=w_mg, w_cap=w_cap, w_cap_desc=w_cap_desc,
        min_edge_weight=min_edge_weight,
    )

    labels = run_community_detection(G, algorithm=algorithm, **kwargs)

    n_clusters = len({v for v in labels.values() if v != -1})
    n_isolated = sum(1 for v in labels.values() if v == -1)
    print(f"  Graph     : {G.number_of_nodes()} nodes  {G.number_of_edges()} edges")
    print(f"  Meta [{algorithm}]: {n_clusters} clusters  |  {n_isolated} noise/isolated")

    return labels, G