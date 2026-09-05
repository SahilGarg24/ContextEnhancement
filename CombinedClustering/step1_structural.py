import numpy as np
import pandas as pd
import re


def parse_grain(grain_str: str) -> set:
    """
    Parse grain string like:
    "[Version].[Version Name], [Location].[Location]"

    → returns set:
    {"version.version name", "location.location"}
    """
    if pd.isna(grain_str) or not str(grain_str).strip():
        return set()

    # Extract [X].[Y] patterns
    matches = re.findall(r"\[(.*?)\]\.\[(.*?)\]", grain_str)

    # Normalize
    return {f"{dim.strip().lower()}.{attr.strip().lower()}" for dim, attr in matches}


def attr_jaccard(set_a: set, set_b: set) -> float:
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def build_structural_matrix(
    df: pd.DataFrame,
    mg_col: str = "MeasureGroup",
    grain_col: str = "Grain",
    w_mg: float = 0.5,
    w_attr: float = 0.5,
) -> np.ndarray:
    """
    Builds structural similarity matrix:

    S_struct[i,j] = w_mg * same_MG + w_attr * attribute_jaccard
    """

    n = len(df)

    # --- Parse attributes from Grain ---
    attr_sets = [parse_grain(g) for g in df[grain_col]]

    # --- Measure Groups ---
    mgs = df[mg_col].fillna("__UNKNOWN__").tolist()

    # --- Initialize matrix ---
    S = np.zeros((n, n), dtype=np.float32)

    for i in range(n):
        for j in range(i, n):
            if i == j:
                S[i, j] = 1.0
                continue

            # --- Measure Group similarity ---
            same_MG = 1.0 if mgs[i] == mgs[j] else 0.0

            # --- Attribute Jaccard ---
            attr_score = attr_jaccard(attr_sets[i], attr_sets[j])

            # --- Final score ---
            score = w_mg * same_MG + w_attr * attr_score

            S[i, j] = score
            S[j, i] = score

    return S
