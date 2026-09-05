"""
L1 Semantic Clustering
======================
Embeds measure descriptions and business capability names,
builds a combined cosine distance matrix, and runs HDBSCAN.

HDBSCAN is correct here because:
  - Data lives in continuous vector space, not a graph
  - Noise label (−1) naturally identifies hub / cross-cutting measures
  - No K to specify — cluster count emerges from embedding density

Two embedding channels:
  - Measure description  (w=0.70): what the measure actually computes
  - Business capability  (w=0.30): which process area it serves
    Same-capability pairs score cos=1.0 automatically — no explicit
    name boost needed on top of this.
"""

import numpy as np
import pandas as pd
import hdbscan
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


def run_semantic_clustering(
    df:               pd.DataFrame,
    measure_col:      str   = "MeasureName",
    cap_desc_col: str   = "Capability Description",
    cap_col:          str   = "Business Capability",
    w_cap_desc:         float = 0.50,
    w_cap:            float = 0.50,
    model_name:       str   = "all-MiniLM-L6-v2",
    min_cluster_size: int   = 3,
    min_samples:      int   = 2,
    cluster_selection_method: str = "eom",
) -> tuple[dict, np.ndarray]:
    """
    Parameters
    ----------
    df              : semantic output DataFrame (one row per measure)
    measure_col     : column with measure name
    measure_desc_col: column with measure description text
    cap_col         : column with business capability name
    w_*             : embedding channel weights (must sum to 1.0)
    model_name      : sentence-transformers model
    min_cluster_size: HDBSCAN param — minimum members to form a cluster
    min_samples     : HDBSCAN param — controls noise sensitivity

    Returns
    -------
    labels : dict {measure_name: cluster_id}  (−1 = noise / hub)
    D      : N×N distance matrix used (for inspection)
    """
    assert abs(w_cap_desc + w_cap - 1.0) < 1e-6, "Embedding weights must sum to 1.0"
    model = _get_model(model_name)

    print("  Embedding measure descriptions...")
    emb_md  = model.encode(
        df[cap_desc_col].fillna("").tolist(),
        show_progress_bar=False, convert_to_numpy=True
    )

    print("  Embedding capability names...")
    emb_cap = model.encode(
        df[cap_col].fillna("").tolist(),
        show_progress_bar=False, convert_to_numpy=True
    )

    S = w_cap_desc * _cosine_matrix(emb_md) + w_cap * _cosine_matrix(emb_cap)
    np.fill_diagonal(S, 1.0)
    S = np.clip(S, 0.0, 1.0)

    D = np.clip(1.0 - S, 0.0, 1.0).astype(np.float64)
    np.fill_diagonal(D, 0.0)

    clusterer  = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="precomputed",
        cluster_selection_method=cluster_selection_method,
    )
    raw_labels = clusterer.fit_predict(D)

    measures   = df[measure_col].tolist()
    labels     = dict(zip(measures, raw_labels.tolist()))

    n_clusters = len({v for v in labels.values() if v != -1})
    n_noise    = sum(1 for v in labels.values() if v == -1)
    print(f"  Semantic  : {n_clusters} clusters  |  {n_noise} noise (hub/cross-cutting)")

    return labels, D