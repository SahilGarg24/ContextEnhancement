import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


_MODEL_CACHE: dict = {}


def _get_model(model_name: str) -> SentenceTransformer:
    if model_name not in _MODEL_CACHE:
        print(f"  Loading embedding model: {model_name}")
        _MODEL_CACHE[model_name] = SentenceTransformer(model_name)
    return _MODEL_CACHE[model_name]


def _cosine_matrix(embeddings: np.ndarray) -> np.ndarray:
    """Compute full cosine similarity matrix from L2-normalised embeddings."""
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normed = embeddings / np.maximum(norms, 1e-9)
    return np.clip(normed @ normed.T, -1.0, 1.0).astype(np.float32)


def build_semantic_matrix(
    df: pd.DataFrame,
    measure_desc_col: str  = "Measure Description",
    cap_col:     str  = "Business Capability",
    confidence_col:   str  = "Confidence",
    w_cap_desc:       float = 0.30,
    model_name:       str  = "all-MiniLM-L6-v2",
) -> np.ndarray:
    """
    S_semantic[i,j] = conf_matrix[i,j] * cos(MD_i, MD_j)
                    + w_cap_desc       * cos(CD_i, CD_j)

    conf_matrix[i,j] = conf[i] * conf[j]   where HIGH=1.0, MEDIUM=0.5

    Measure description cosine captures *what the measure does*.
    Capability description cosine captures *which business area it serves*.

    For same-capability pairs, cos(CD_i, CD_j) == 1.0 automatically
    — no separate name-boost needed.
    """
    model = _get_model(model_name)
    n     = len(df)

    # --- Confidence weights ---
    # conf_map  = {"HIGH": 1.0, "MEDIUM": 0.5}
    # conf_vals = np.array(
    #     [conf_map.get(str(v).strip().upper(), 0.5) for v in df[confidence_col]],
    #     dtype=np.float32,
    # )
    # conf_matrix = np.outer(conf_vals, conf_vals)   # shape N×N

    # --- Embed measure descriptions ---
    print("  Embedding measure descriptions...")
    md_texts  = df[measure_desc_col].fillna("").tolist()
    emb_md    = model.encode(md_texts, show_progress_bar=False, convert_to_numpy=True)
    cos_md    = _cosine_matrix(emb_md)

    # --- Embed capability descriptions ---
    print("  Embedding business capabilities ...")
    bc_texts  = df[cap_col].fillna("").tolist()
    emb_bc    = model.encode(bc_texts, show_progress_bar=False, convert_to_numpy=True)
    cos_bc    = _cosine_matrix(emb_bc)

    S = 0.5 * cos_md + 0.5 * cos_bc
    np.fill_diagonal(S, 1.0)
    return np.clip(S, 0.0, 1.0)
