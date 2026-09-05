import numpy as np


def minmax_normalize(matrix: np.ndarray) -> np.ndarray:
    """
    Per-matrix min-max normalization → [0, 1].
    Diagonal (self-similarity = 1.0) is excluded from normalization
    and reset to 1.0 after scaling.
    """
    m = matrix.copy().astype(np.float32)
    np.fill_diagonal(m, np.nan)               # exclude diagonal

    lo  = np.nanmin(m)
    hi  = np.nanmax(m)
    rng = hi - lo

    if rng < 1e-9:
        m = np.where(np.isnan(m), 0.0, 0.0)  # degenerate: all off-diag identical
    else:
        m = (m - lo) / rng
        m = np.where(np.isnan(m), 0.0, m)

    np.fill_diagonal(m, 1.0)
    return m


def fuse(
    S_struct:    np.ndarray,
    S_semantic:  np.ndarray,
    S_behavioral: np.ndarray,
    w_struct:    float = 0.30,
    w_semantic:  float = 0.45,
    w_behavioral: float = 0.25,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Normalize each matrix then compute weighted sum.

    Returns
    -------
    S_fused : similarity matrix  [0, 1]
    D_fused : distance  matrix   [0, 1]  (= 1 - S_fused, diagonal = 0)
    """
    assert abs(w_struct + w_semantic + w_behavioral - 1.0) < 1e-6, \
        "Weights must sum to 1.0"

    S1 = minmax_normalize(S_struct)
    S2 = minmax_normalize(S_semantic)
    S3 = minmax_normalize(S_behavioral)

    S_fused = w_struct * S1 + w_semantic * S2 + w_behavioral * S3
    np.fill_diagonal(S_fused, 1.0)

    D_fused = np.clip(1.0 - S_fused, 0.0, 1.0).astype(np.float64)
    np.fill_diagonal(D_fused, 0.0)

    return S_fused, D_fused
