import pandas as pd
import numpy as np
import networkx as nx
from visualization_utils import visualise_models


SAFETY_FACTOR = 1e-6
PRIOR_BEHAVIOURAL_WEIGHT = 0.7
PRIOR_SPREAD_WEIGHT = 0.3
# personalization type weight
type_budget = {
        "view":    0.25,
        "widget":  0.45,
        "measure": 0.30,
    }

PAGERANK_DAMPING = 0.9
PAGERANK_MAX_ITER = 200
PAGERANK_TOL = 1e-6
FORWARD_EDGE_DAMPING = 0.7
REVERSE_EDGE_DAMPING = 0.9


class entity_ranking:
    def __init__(self):
        pass

    # Pre Ranking ------------------------------------------------------------------------------------------------------

    def _minmax_normalize(self, series: pd.Series) -> pd.Series:
        # min-max normalization to aid the blend with spread score
        min_val = series.min()
        max_val = series.max()
        return (series - min_val) / (max_val - min_val + SAFETY_FACTOR)



    def _compute_behavioural_score(self, df: pd.DataFrame, terms: list, user_freq_col: str = "User_Freq", penalty_factor: float = 3,) -> pd.Series:

        # log is used for compression to level the domination
        score = sum(
            weight * np.log1p(df[col])
            for weight, col in terms
        )
        # this penalise the cases where only one user shows dominance (maybe useful but may introduce bias)
        spread_penalty = df[user_freq_col] / (df[user_freq_col] + penalty_factor)
        score = score * spread_penalty
        return self._minmax_normalize(score)


    def generate_measure_ranks_from_logs_data(self, logs_data: pd.DataFrame) -> pd.DataFrame:

        data = logs_data.copy()
        for col in ["User_Freq", "Global_Freq"]:
            data[col] = pd.to_numeric(data[col], errors="coerce").clip(lower=0).fillna(0)

        data["interaction_score"] = self._compute_behavioural_score(
            data,
            terms=[(0.6, "User_Freq"), (0.4, "Global_Freq")],
        )
        return data[["Measure", "interaction_score"]]


    def generate_widget_ranks_from_psr_data(self, psr_data: pd.DataFrame) -> pd.DataFrame:

        data = psr_data.copy()
        for col in ["User_Freq", "Global_Freq"]:
            data[col] = pd.to_numeric(data[col], errors="coerce").clip(lower=0).fillna(0)

        # this intensity rewards the good performers (high global freq and moderate user freq)
        data["intensity"] = data["Global_Freq"] / (data["User_Freq"] + SAFETY_FACTOR)

        data["interaction_score"] = self._compute_behavioural_score(
            data,
            terms=[(0.6, "User_Freq"), (0.3, "Global_Freq"), (0.1, "intensity")],
        )
        return data[["Widget", "interaction_score"]]


    def generate_view_ranks_from_adoption_data(self, adoption_data: pd.DataFrame) -> pd.DataFrame:

        data = adoption_data.copy()
        for col in ["User_Freq", "Global_Freq", "Usage"]:
            data[col] = pd.to_numeric(data[col], errors="coerce").clip(lower=0).fillna(0)

        # this intensity rewards high usage per user
        data["intensity"] = np.sqrt(data["Usage"]) / (data["User_Freq"] + SAFETY_FACTOR)

        data["interaction_presence_score"] = self._compute_behavioural_score(
            data,
            terms=[
                (0.40, "User_Freq"),
                (0.25, "Global_Freq")
            ],
        )
        data["interaction_usage_score"] = self._compute_behavioural_score(
            data,
            terms=[
                (0.3, "Usage"),
                (0.05, "intensity")
            ],
        )
        data["interaction_score"] = (
            0.6 * data["interaction_presence_score"] +
            0.4 * data["interaction_usage_score"]
        )

        return data[["View", "interaction_score"]]


    def _compute_spread_scores(self, config_data: pd.DataFrame) -> tuple:

        vw_data = config_data[["View", "Widget"]].drop_duplicates()
        wm_data = config_data[["Widget", "Measure"]].drop_duplicates()

        widget_spread = (
            vw_data.groupby("Widget")["View"]
            .nunique()
            .reset_index(name="View_Count")
        )

        measure_spread = (
            wm_data.groupby("Measure")["Widget"]
            .nunique()
            .reset_index(name="Widget_Count")
        )

        # min-max normalization to aid the blend with behavioural scores

        widget_spread["spread_score"] = self._minmax_normalize(
            np.log1p(widget_spread["View_Count"])
        )

        measure_spread["spread_score"] = self._minmax_normalize(
            np.log1p(measure_spread["Widget_Count"])
        )

        return (
            widget_spread[["Widget", "spread_score"]],
            measure_spread[["Measure", "spread_score"]],
        )

    # Graph ------------------------------------------------------------------------------------------------------------

    def _build_node_priors(
        self,
        view_scores: pd.DataFrame,
        widget_scores: pd.DataFrame,
        measure_scores: pd.DataFrame,
        widget_spread: pd.DataFrame,
        measure_spread: pd.DataFrame,
    ) -> dict:

        priors = {}

        for _, row in view_scores.iterrows():
            priors[("view", row["View"])] = float(row["interaction_score"])

        # Widgets — merge behavioural and spread
        w_merged = widget_scores.merge(widget_spread, on="Widget", how="outer").fillna(0)
        for _, row in w_merged.iterrows():
            prior = (
                PRIOR_BEHAVIOURAL_WEIGHT * row["interaction_score"] +
                PRIOR_SPREAD_WEIGHT * row["spread_score"]
            )
            priors[("widget", row["Widget"])] = float(prior)

        # Measures — merge behavioural and spread
        m_merged = measure_scores.merge(measure_spread, on="Measure", how="outer").fillna(0)
        for _, row in m_merged.iterrows():
            prior = (
                PRIOR_BEHAVIOURAL_WEIGHT * row["interaction_score"] +
                PRIOR_SPREAD_WEIGHT * row["spread_score"]
            )
            priors[("measure", row["Measure"])] = float(prior)

        return priors


    def build_graph(
        self,
        config_data: pd.DataFrame,
        view_scores: pd.DataFrame,
        widget_scores: pd.DataFrame,
        measure_scores: pd.DataFrame,
        widget_spread: pd.DataFrame,
        measure_spread: pd.DataFrame,
    ) -> nx.DiGraph:

        G = nx.DiGraph()

        priors = self._build_node_priors(
            view_scores, widget_scores, measure_scores,
            widget_spread, measure_spread,
        )

        # Add all nodes
        for node, prior in priors.items():
            G.add_node(node, prior=prior)

        view_score_map = view_scores.set_index("View")["interaction_score"].to_dict()
        widget_score_map = widget_scores.set_index("Widget")["interaction_score"].to_dict()
        measure_score_map = measure_scores.set_index("Measure")["interaction_score"].to_dict()

        # --- Page -> Widget edges ---
        vw_data = config_data[["View", "Widget"]].drop_duplicates()
        widget_count_per_view = vw_data.groupby("View")["Widget"].nunique()
        view_count_per_widget = vw_data.groupby("Widget")["View"].nunique()

        for _, row in vw_data.iterrows():
            view = row["View"]
            widget = row["Widget"]
            view_score = view_score_map.get(view, 0.0)
            widget_score = widget_score_map.get(widget, 0.0)
            w_count = widget_count_per_view.get(view, 0)
            v_count = view_count_per_widget.get(widget, 0)

            # Ensure nodes exist even if absent from logs
            if ("view", view) not in G:
                G.add_node(("view", view), prior=0.0)
            if ("widget", widget) not in G:
                G.add_node(("widget", widget), prior=0.0)

            # forward edge from view to widget
            forward_weight = (view_score * FORWARD_EDGE_DAMPING) / w_count if w_count > 0 else 0.0
            if forward_weight > 0:
                G.add_edge(("view", view), ("widget", widget), weight=forward_weight)

            # reverse edge from widget to view
            reverse_weight = (widget_score * REVERSE_EDGE_DAMPING) / v_count if v_count > 0 else 0.0
            if reverse_weight > 0:
                G.add_edge(("widget", widget), ("view", view), weight=reverse_weight)

        # --- Widget -> Measure edges ---
        wm_data = config_data[["Widget", "Measure"]].drop_duplicates()
        measure_count_per_widget = wm_data.groupby("Widget")["Measure"].nunique()
        widget_count_per_measure = wm_data.groupby("Measure")["Widget"].nunique()

        for _, row in wm_data.iterrows():
            widget = row["Widget"]
            measure = row["Measure"]
            widget_score = widget_score_map.get(widget, 0.0)
            measure_score = measure_score_map.get(measure, 0.0)
            m_count = measure_count_per_widget.get(widget, 0)
            w_count = widget_count_per_measure.get(measure, 0)

            # Ensure nodes exist even if absent from logs
            if ("widget", widget) not in G:
                G.add_node(("widget", widget), prior=0.0)
            if ("measure", measure) not in G:
                G.add_node(("measure", measure), prior=0.0)

            # forward edge from widget to measure
            forward_weight = (widget_score * FORWARD_EDGE_DAMPING) / m_count if m_count > 0 else 0.0
            if forward_weight > 0:
                G.add_edge(("widget", widget), ("measure", measure), weight=forward_weight)

            # reverse edge from measure to widget
            reverse_weight = (measure_score * REVERSE_EDGE_DAMPING) / w_count if w_count > 0 else 0.0
            if reverse_weight > 0:
                G.add_edge(("measure", measure), ("widget", widget), weight=reverse_weight)

        return G

    # PageRank

    def _normalize_priors(self, priors: dict) -> dict:
        node_by_type = {"view": {}, "widget": {}, "measure": {}}
        for (ntype, name), val in priors.items():
            node_by_type[ntype][(ntype, name)] = val

        # Step 3 — within each type, distribute budget proportional to prior
        normalized = {}
        for ntype, nodes in node_by_type.items():
            if not nodes:
                continue
            type_total = sum(nodes.values()) or 1.0
            budget = type_budget[ntype]
            for node, val in nodes.items():
                normalized[node] = budget * (val / type_total)

        # Result already sums to 1.0 since budgets sum to 1.0 and within-type shares sum to 1.0
        return normalized


    def run_pagerank(self, G: nx.DiGraph) -> dict:

        priors = nx.get_node_attributes(G, "prior")
        # at each ranking step, all the node rank does not propagates. Instead, a portion of the node rank teleports
        # towards other nodes based on their value in the personaliation vector
        personalization = self._normalize_priors(priors)

        ranks = nx.pagerank(
            G,
            alpha=PAGERANK_DAMPING,
            personalization=personalization,
            weight="weight",
            max_iter=PAGERANK_MAX_ITER,
            tol=PAGERANK_TOL,
        )
        return ranks

    # Importance scores

    def compute_final_importance(
        self,
        ranks: dict,
        widget_scores: pd.DataFrame,
        measure_scores: pd.DataFrame,
    ) -> tuple:

        widget_pr = {
            node[1]: score
            for node, score in ranks.items()
            if node[0] == "widget"
        }
        measure_pr = {
            node[1]: score
            for node, score in ranks.items()
            if node[0] == "measure"
        }

        widget_pr_df = pd.DataFrame(widget_pr.items(), columns=["Widget", "pagerank_score"])
        measure_pr_df = pd.DataFrame(measure_pr.items(), columns=["Measure", "pagerank_score"])

        # Merge with behavioral scores
        widget_final = widget_pr_df.merge(widget_scores, on="Widget", how="outer").fillna(0)
        measure_final = measure_pr_df.merge(measure_scores, on="Measure", how="outer").fillna(0)

        return (
            measure_final[["Measure", "pagerank_score", "interaction_score"]].sort_values("pagerank_score", ascending=False),
            widget_final[["Widget", "pagerank_score", "interaction_score"]].sort_values("pagerank_score", ascending=False),
        )

    # Main entry

    def generate_ranks(
        self,
        config_data: pd.DataFrame,
        view_scores: pd.DataFrame,
        widget_scores: pd.DataFrame,
        measure_scores: pd.DataFrame,
    ) -> tuple:

        widget_spread, measure_spread = self._compute_spread_scores(config_data)

        G = self.build_graph(
            config_data,
            view_scores,
            widget_scores,
            measure_scores,
            widget_spread,
            measure_spread,
        )

        ranks = self.run_pagerank(G)
        measure_final, widget_final = self.compute_final_importance(ranks, widget_scores, measure_scores)

        # v_models = visualise_models()
        # v_models.visualize_graph(G, measure_final, widget_final, output_path="graph.html")

        return measure_final, widget_final