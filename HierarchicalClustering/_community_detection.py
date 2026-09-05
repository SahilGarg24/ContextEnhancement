"""
Community Detection — Unified Dispatcher
=========================================
Supports five algorithms on a weighted NetworkX graph:

  Algorithm key         Method
  ─────────────────     ──────────────────────────────────────────────────────
  "louvain"             NetworkX built-in Louvain (modularity optimisation)
  "leiden"              leidenalg — RBConfiguration / CPM / Modularity
  "hdbscan_diffusion"   Diffusion distance matrix → HDBSCAN (deterministic)
  "hdbscan_node2vec"    node2vec random-walk embeddings → HDBSCAN (stochastic)
  "mcl"                 Markov Cluster Algorithm (flow simulation)

All algorithms honour the same output contract:
  labels : dict { node_name → cluster_id }
  cluster_id == -1  means isolated / noise / not clustered

Isolated nodes (degree 0) are always assigned -1 and excluded from
algorithm computation — they carry no structural signal in any method.

Algorithm selection guidance
─────────────────────────────
  Dense structural graph (config)   → hdbscan_diffusion  (recommended)
                                      leiden/CPM          (good fallback)
                                      mcl                 (balanced sizes)
  Sparse behavioral graph (PMI)     → hdbscan_diffusion
                                      mcl
                                      louvain / leiden    (fast)
  Need strict balance (≈N per cluster) → mcl or hdbscan_* with min_cluster_size
  Need interpretable parameter      → mcl (inflation) or leiden/CPM (density)
  Large graph (>1 K nodes)          → hdbscan_node2vec or louvain (speed)
"""

import numpy as np
import networkx as nx
import hdbscan as _hdbscan
import igraph as ig
import leidenalg
import markov_clustering as mc
from sklearn.metrics import pairwise_distances


# ─────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────────────

def _split_isolated(G: nx.Graph) -> tuple[nx.Graph, set]:
    """Return (subgraph_without_isolated, set_of_isolated_nodes)."""
    isolated = {n for n in G.nodes() if G.degree(n) == 0}
    sub = G.copy()
    sub.remove_nodes_from(isolated)
    return sub, isolated


def _nx_to_igraph(G_nx: nx.Graph) -> tuple[ig.Graph, list]:
    """Convert NetworkX → igraph preserving edge weights. Returns (G_ig, ordered_nodes)."""
    nodes   = list(G_nx.nodes())
    mapping = {n: i for i, n in enumerate(nodes)}
    G_ig    = ig.Graph(n=len(nodes), directed=False)
    G_ig.vs["name"] = nodes
    edges   = [(mapping[u], mapping[v]) for u, v in G_nx.edges()]
    weights = [G_nx[u][v].get("weight", 1.0) for u, v in G_nx.edges()]
    G_ig.add_edges(edges)
    if edges:
        G_ig.es["weight"] = weights
    return G_ig, nodes


def _labels_from_communities(communities: list[set | list], all_nodes: list) -> dict:
    """Map community membership lists back to {node: cid} dict."""
    labels = {}
    for cid, members in enumerate(communities):
        for m in members:
            labels[m] = cid
    return labels


# ─────────────────────────────────────────────────────────────────────────────
# Algorithm 1 — Louvain
# ─────────────────────────────────────────────────────────────────────────────

def _run_louvain(G: nx.Graph, resolution: float, seed: int, **_) -> dict:
    sub, isolated = _split_isolated(G)
    labels = {n: -1 for n in isolated}
    if sub.number_of_nodes() > 0:
        comms = nx.community.louvain_communities(
            sub, weight="weight", resolution=resolution, seed=seed
        )
        labels.update(_labels_from_communities(comms, list(sub.nodes())))
    return labels


# ─────────────────────────────────────────────────────────────────────────────
# Algorithm 2 — Leiden
# ─────────────────────────────────────────────────────────────────────────────

_LEIDEN_PARTITIONS = {
    "RBConfiguration": leidenalg.RBConfigurationVertexPartition,
    "CPM":             leidenalg.CPMVertexPartition,
    "Modularity":      leidenalg.ModularityVertexPartition,
}


def _run_leiden(
    G: nx.Graph,
    resolution: float,
    leiden_partition: str,
    leiden_n_iterations: int,
    seed: int,
    **_,
) -> dict:
    if leiden_partition not in _LEIDEN_PARTITIONS:
        raise ValueError(
            f"Unknown leiden_partition '{leiden_partition}'. "
            f"Choose from: {list(_LEIDEN_PARTITIONS.keys())}"
        )
    PartClass = _LEIDEN_PARTITIONS[leiden_partition]
    sub, isolated = _split_isolated(G)
    labels = {n: -1 for n in isolated}
    if sub.number_of_nodes() > 0:
        G_ig, ig_nodes = _nx_to_igraph(sub)
        kw = dict(
            weights="weight" if G_ig.ecount() > 0 else None,
            n_iterations=leiden_n_iterations,
            seed=seed,
        )
        if leiden_partition != "Modularity":
            kw["resolution_parameter"] = resolution
        partition = leidenalg.find_partition(G_ig, PartClass, **kw)
        for cid, members in enumerate(partition):
            for vid in members:
                labels[ig_nodes[vid]] = cid
    return labels


# ─────────────────────────────────────────────────────────────────────────────
# Algorithm 3 — HDBSCAN + Diffusion Distance
# ─────────────────────────────────────────────────────────────────────────────

def _diffusion_distance(G: nx.Graph, t: int) -> tuple[np.ndarray, list]:
    """
    Compute N×N normalised diffusion distance matrix.

    D[i,j] = || T^t[i,:] - T^t[j,:] ||_2  /  max

    T = D^{-1/2} A D^{-1/2}  (symmetric normalised adjacency)
    t = number of diffusion steps  (2–5 recommended)

    Isolated nodes (all-zero rows in A) get a sentinel row of 1.0
    so HDBSCAN places them in noise. Caller strips them afterwards.
    """
    nodes = list(G.nodes())
    n     = len(nodes)
    A     = nx.to_numpy_array(G, nodelist=nodes, weight="weight")

    deg   = A.sum(axis=1)
    # Isolated nodes: degree 0 → sentinel so they land far from everything
    isolated_mask = deg == 0
    deg_safe = np.where(isolated_mask, 1.0, deg)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(deg_safe))

    T   = D_inv_sqrt @ A @ D_inv_sqrt          # symmetric transition matrix
    T   = np.clip(T, 0.0, 1.0)                 # numerical safety
    T_t = np.linalg.matrix_power(T, t)

    # Sentinel rows for isolated nodes
    T_t[isolated_mask] = 1.0

    D = pairwise_distances(T_t, metric="euclidean").astype(np.float64)
    max_d = D[~isolated_mask][:, ~isolated_mask].max()
    if max_d > 0:
        D /= max_d
    D = np.clip(D, 0.0, 1.0)
    np.fill_diagonal(D, 0.0)
    return D, nodes


def _run_hdbscan_diffusion(
    G: nx.Graph,
    diffusion_t: int,
    min_cluster_size: int,
    min_samples: int,
    hdbscan_selection_method: str,
    cluster_selection_epsilon: int,
    **_,
) -> dict:
    _, isolated = _split_isolated(G)
    nodes = list(G.nodes())

    D, ordered_nodes = _diffusion_distance(G, t=diffusion_t)

    raw = _hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="precomputed",
        cluster_selection_method=hdbscan_selection_method,
        cluster_selection_epsilon=cluster_selection_epsilon
    ).fit_predict(D)

    labels = {}
    for node, lbl in zip(ordered_nodes, raw):
        labels[node] = -1 if node in isolated else int(lbl)

    return labels


# ─────────────────────────────────────────────────────────────────────────────
# Algorithm 4 — HDBSCAN + node2vec
# ─────────────────────────────────────────────────────────────────────────────

def _run_hdbscan_node2vec(
    G: nx.Graph,
    n2v_dimensions: int,
    n2v_walk_length: int,
    n2v_num_walks: int,
    n2v_p: float,
    n2v_q: float,
    n2v_window: int,
    min_cluster_size: int,
    min_samples: int,
    hdbscan_selection_method: str,
    seed: int,
    **_,
) -> dict:
    from node2vec import Node2Vec

    sub, isolated = _split_isolated(G)
    labels = {n: -1 for n in isolated}

    if sub.number_of_nodes() < 2:
        return labels

    n2v = Node2Vec(
        sub,
        dimensions=n2v_dimensions,
        walk_length=n2v_walk_length,
        num_walks=n2v_num_walks,
        p=n2v_p,
        q=n2v_q,
        weight_key="weight",
        workers=1,
        quiet=True,
        seed=seed,
    )
    model = n2v.fit(window=n2v_window, min_count=1, sg=1, seed=seed)

    sub_nodes = list(sub.nodes())
    emb       = np.array([model.wv[str(nd)] for nd in sub_nodes])

    raw = _hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        cluster_selection_method=hdbscan_selection_method,
    ).fit_predict(emb)

    for node, lbl in zip(sub_nodes, raw):
        labels[node] = int(lbl)

    return labels


# ─────────────────────────────────────────────────────────────────────────────
# Algorithm 5 — MCL (Markov Cluster Algorithm)
# ─────────────────────────────────────────────────────────────────────────────

def _run_mcl(
    G: nx.Graph,
    mcl_inflation: float,
    mcl_expansion: int,
    mcl_iterations: int,
    mcl_pruning_threshold: float,
    **_,
) -> dict:
    """
    MCL directly on the weighted adjacency matrix.

    inflation   : higher → more / smaller clusters  (try 1.5 – 4.0)
    expansion   : random walk length  (almost always 2)
    pruning_threshold : entries below this are zeroed for sparsity
    """
    nodes = list(G.nodes())
    _, isolated = _split_isolated(G)

    A = nx.to_numpy_array(G, nodelist=nodes, weight="weight")

    result   = mc.run_mcl(
        A,
        inflation=mcl_inflation,
        expansion=mcl_expansion,
        iterations=mcl_iterations,
        pruning_threshold=mcl_pruning_threshold,
    )
    clusters = mc.get_clusters(result)   # list of tuples of integer indices

    labels = {n: -1 for n in nodes}     # default -1 (covers isolated)
    for cid, members in enumerate(clusters):
        for idx in members:
            node = nodes[idx]
            if node not in isolated:
                labels[node] = cid

    # MCL can return singleton clusters — re-label them -1 for consistency
    # with HDBSCAN noise semantics
    from collections import Counter
    size_map = Counter(v for v in labels.values() if v != -1)
    for node, cid in labels.items():
        if cid != -1 and size_map[cid] == 1:
            labels[node] = -1

    return labels


# ─────────────────────────────────────────────────────────────────────────────
# Public dispatcher
# ─────────────────────────────────────────────────────────────────────────────

_ALGORITHMS = {
    "louvain":             _run_louvain,
    "leiden":              _run_leiden,
    "hdbscan_diffusion":   _run_hdbscan_diffusion,
    "hdbscan_node2vec":    _run_hdbscan_node2vec,
    "mcl":                 _run_mcl,
}


def run_community_detection(G: nx.Graph, algorithm: str, **params) -> dict:
    """
    Unified entry point.

    Parameters
    ----------
    G         : weighted NetworkX undirected graph
    algorithm : one of 'louvain' | 'leiden' | 'hdbscan_diffusion' |
                        'hdbscan_node2vec' | 'mcl'
    **params  : all algorithm parameters (unused keys are silently ignored)

    Returns
    -------
    labels : dict { node_name → cluster_id }   (-1 = noise / isolated)
    """
    if algorithm not in _ALGORITHMS:
        raise ValueError(
            f"Unknown algorithm '{algorithm}'. "
            f"Choose from: {list(_ALGORITHMS.keys())}"
        )

    if G.number_of_nodes() == 0:
        return {}

    return _ALGORITHMS[algorithm](G, **params)