import json
import time
import numpy as np
import pandas as pd
import hdbscan
from sklearn.metrics import adjusted_rand_score, silhouette_score


# ---------------------------------------------------------------------------
# HDBSCAN
# ---------------------------------------------------------------------------

def run_hdbscan(
    D_fused: np.ndarray,
    min_cluster_size: int = 3,
    min_samples:      int = 2,
) -> hdbscan.HDBSCAN:
    """
    Run HDBSCAN on the precomputed distance matrix.

    cluster_selection_method='eom' (Excess of Mass) is preferred over 'leaf'
    for uneven cluster sizes — typical in supply chain domain data.

    prediction_data=True enables soft cluster membership scores,
    which are essential for identifying hub measures.
    """
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="precomputed",
        cluster_selection_method="eom",
        
    )
    clusterer.fit(D_fused)
    return clusterer


def _compute_cross_cluster_affinity(
    labels: np.ndarray,
    D_fused: np.ndarray | None,
    threshold: float = 0.30,
) -> np.ndarray:
    """
    For each measure, compute its mean similarity to every cluster other than
    its own.  Returns a boolean array: True if the measure has strong affinity
    (≥ threshold) to at least one other cluster — i.e. it is cross-cutting.

    Works purely from the distance matrix so it is compatible with
    metric='precomputed'.
    """
    n = len(labels)
    cross = np.zeros(n, dtype=bool)

    if D_fused is None:
        return cross

    S = 1.0 - D_fused                           # back to similarity
    unique_clusters = sorted(set(labels) - {-1})

    for i in range(n):
        own = labels[i]
        if own == -1:
            continue
        for other in unique_clusters:
            if other == own:
                continue
            other_idxs = np.where(labels == other)[0]
            if len(other_idxs) == 0:
                continue
            mean_sim = S[i, other_idxs].mean()
            if mean_sim >= threshold:
                cross[i] = True
                break

    return cross


def build_cluster_df(
    df: pd.DataFrame,
    clusterer: hdbscan.HDBSCAN,
    D_fused:        np.ndarray | None = None,
    measure_col:    str = "MeasureName",
    confidence_col: str = "Confidence",
    cap_col:        str = "Business Capability",
    spread_col:     str = "spread_score",
) -> pd.DataFrame:
    """
    Attach cluster labels, probabilities, and hub flags to the measure DataFrame.

    hub_flag logic (any of):
      1. Noise label (−1)
      2. Cross-cluster affinity ≥ 0.30 to another cluster (from D_fused)
      3. spread_score > 0.70 from PageRank (if column present)
    """
    result = df.copy()
    result["cluster_id"]   = clusterer.labels_
    result["cluster_prob"] = clusterer.probabilities_

    labels = clusterer.labels_

    # Cross-cluster affinity hub detection (works with precomputed metric)
    cross_cutting = _compute_cross_cluster_affinity(labels, D_fused)

    def _is_hub(i, label):
        if label == -1:
            return True
        if cross_cutting[i]:
            return True
        if spread_col in result.columns and pd.notna(result.iloc[i].get(spread_col)):
            if float(result.iloc[i][spread_col]) > 0.70:
                return True
        return False

    result["hub_flag"]    = [_is_hub(i, lbl) for i, lbl in enumerate(labels)]
    result["conf_flag"]   = result[confidence_col].str.upper() == "MEDIUM"

    # Fraction of MEDIUM-confidence members per cluster (for cluster-level reliability)
    medium_frac = (
        result.groupby("cluster_id")["conf_flag"]
        .mean()
        .rename("cluster_medium_frac")
    )
    result = result.merge(medium_frac, on="cluster_id", how="left")
    result["cluster_low_reliability"] = result["cluster_medium_frac"] > 0.40

    return result


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(
    cluster_df: pd.DataFrame,
    D_fused: np.ndarray,
    meta_caps_df: pd.DataFrame,
    cap_col:      str = "Business Capability",
    cluster_col:  str = "cluster_id",
) -> dict:
    """
    ARI: compare measure clusters vs meta-capability labels propagated to measures.
    Silhouette: uses the fused distance matrix.
    Excludes noise points (-1) from both metrics.
    """
    merged = cluster_df.merge(meta_caps_df, on=cap_col, how="left")
    mask   = merged[cluster_col] != -1

    ari = adjusted_rand_score(
        merged.loc[mask, "meta_cap_label"].fillna(-1),
        merged.loc[mask, cluster_col],
    )

    # Silhouette needs at least 2 clusters and ≥2 non-noise points per cluster
    labels_nonoise = merged.loc[mask, cluster_col].values
    D_nonoise      = D_fused[np.ix_(mask.values, mask.values)]
    if len(set(labels_nonoise)) >= 2:
        sil = silhouette_score(D_nonoise, labels_nonoise, metric="precomputed")
    else:
        sil = float("nan")

    return {"ari_vs_meta_caps": round(ari, 4), "silhouette": round(sil, 4)}


# ---------------------------------------------------------------------------
# LLM naming via Anthropic API
# ---------------------------------------------------------------------------

NAMING_SYSTEM = """You are a supply chain domain expert specializing in 
Demand Planning and Supply Planning platforms. 
You will receive a list of platform measures, their descriptions, and business capabilities. 
Your task: identify the bounded context (business sub-domain) these measures collectively represent.
Respond ONLY with valid JSON — no markdown fences, no preamble."""

NAMING_USER_TEMPLATE = """Measures in this cluster:
{measures_block}

Name this business domain. Respond with exactly the following JSON structure:
{{
  "domain_name": "<3-5 word bounded context name>",
  "description": "<2 sentences: what business process this cluster represents>",
  "planning_domain": "<one of: Demand Planning | Supply Planning | Both>",
  "confidence": "<High | Medium | Low based on how cohesive the cluster is>"
}}"""


def _build_measures_block(cluster_rows: pd.DataFrame,
                           measure_col:  str = "MeasureName",
                           desc_col:     str = "Measure Description",
                           cap_col:      str = "Business Capability") -> str:
    lines = []
    for _, row in cluster_rows.iterrows():
        lines.append(
            f"- {row[measure_col]}: {row.get(desc_col, '')} "
            f"[Capability: {row.get(cap_col, '')}]"
        )
    return "\n".join(lines)


def name_clusters_with_llm(
    cluster_df: pd.DataFrame,
    measure_col: str = "MeasureName",
    desc_col:    str = "Measure Description",
    cap_col:     str = "Business Capability",
    model:       str = "claude-sonnet-4-20250514",
    max_tokens:  int = 512,
    retry_delay: int = 5,
) -> pd.DataFrame:
    """
    For each non-noise cluster, send measures to Claude and parse the JSON response.
    Returns a DataFrame with one row per cluster.
    """
    import anthropic

    client   = anthropic.Anthropic()
    clusters = sorted(c for c in cluster_df["cluster_id"].unique() if c != -1)
    results  = []

    for cid in clusters:
        rows = cluster_df[cluster_df["cluster_id"] == cid]
        measures_block = _build_measures_block(rows, measure_col, desc_col, cap_col)

        prompt = NAMING_USER_TEMPLATE.format(measures_block=measures_block)

        for attempt in range(3):
            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    system=NAMING_SYSTEM,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw  = response.content[0].text.strip()
                data = json.loads(raw)
                data["cluster_id"]    = cid
                data["member_count"]  = len(rows)
                data["hub_count"]     = int(rows["hub_flag"].sum())
                data["low_reliability"] = bool(rows["cluster_low_reliability"].iloc[0])
                results.append(data)
                break
            except (json.JSONDecodeError, Exception) as e:
                if attempt == 2:
                    print(f"  WARNING: LLM naming failed for cluster {cid}: {e}")
                    results.append({
                        "cluster_id":      cid,
                        "domain_name":     f"Cluster_{cid}",
                        "description":     "LLM naming failed",
                        "planning_domain": "Unknown",
                        "confidence":      "Low",
                        "member_count":    len(rows),
                        "hub_count":       int(rows["hub_flag"].sum()),
                        "low_reliability": bool(rows["cluster_low_reliability"].iloc[0]),
                    })
                else:
                    time.sleep(retry_delay)

    # Add hub cluster entry
    hub_rows = cluster_df[cluster_df["cluster_id"] == -1]
    if len(hub_rows) > 0:
        results.append({
            "cluster_id":      -1,
            "domain_name":     "Shared / Cross-cutting",
            "description":     "Hub measures spanning multiple domains. "
                               "Review for duplication or dedicated shared-infrastructure cluster.",
            "planning_domain": "Both",
            "confidence":      "N/A",
            "member_count":    len(hub_rows),
            "hub_count":       len(hub_rows),
            "low_reliability": False,
        })

    return pd.DataFrame(results)
