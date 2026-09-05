import numpy as np
import pandas as pd
import ast


def parse_measure_list(measure_str):
    """
    Convert string like:
    "['A', 'B', 'C']" → ['A','B','C']
    """
    try:
        return list(set(ast.literal_eval(measure_str)))
    except:
        return []


def build_cooccurrence(df: pd.DataFrame, measure_col: str = "Measures"):
    """
    Build:
    1) co-occurrence matrix
    2) measure index mapping
    """
    # --- Parse all queries ---
    queries = df[measure_col].dropna().apply(parse_measure_list)

    # --- Build global measure list ---
    all_measures = sorted(set(m for q in queries for m in q))
    n = len(all_measures)
    name_to_idx = {m: i for i, m in enumerate(all_measures)}

    # --- Co-occurrence matrix ---
    co = np.zeros((n, n), dtype=np.float64)

    for q in queries:
        idxs = [name_to_idx[m] for m in q if m in name_to_idx]

        if len(idxs) < 2:
            continue

        for i in range(len(idxs)):
            for j in range(i + 1, len(idxs)):
                a, b = idxs[i], idxs[j]
                co[a, b] += 1
                co[b, a] += 1

    return co, all_measures


def build_behavioral_matrix(df: pd.DataFrame, measure_col: str = "Measures"):
    """
    Build behavioral similarity using PMI:

    1) co-occurrence
    2) P(i,j)
    3) P(i)
    4) PMI
    """

    co, measure_list = build_cooccurrence(df, measure_col)
    n = len(measure_list)

    total_pairs = co.sum()

    if total_pairs == 0:
        print("WARNING: No co-occurrence found")
        S = np.zeros((n, n), dtype=np.float32)
        np.fill_diagonal(S, 1.0)
        return S, measure_list

    # --- Probabilities ---
    P_ij = co / total_pairs                      # joint
    freq = co.sum(axis=1)                        # marginal counts
    P_i  = freq / total_pairs                    # marginal probability

    # --- Correct PMI ---
    denom = np.outer(P_i, P_i) + 1e-12           # P(i)*P(j)
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log(P_ij / denom)

    # --- Positive PMI only ---
    ppmi = np.clip(pmi, 0.0, None)

    # --- Normalize to [0,1] ---
    if ppmi.max() > 0:
        ppmi = ppmi / ppmi.max()

    np.fill_diagonal(ppmi, 1.0)

    # Return both matrix AND measure_list so main.py can align to the working set
    return ppmi.astype(np.float32), measure_list