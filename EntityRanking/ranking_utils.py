import re
import pandas as pd
import numpy as np
import networkx as nx
# from visualization_utils import visualise_models


SAFETY_FACTOR = 1e-6
PRIOR_BEHAVIOURAL_WEIGHT = 0.7
PRIOR_SPREAD_WEIGHT = 0.3

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
        # this penalises the cases where only one user shows dominance (maybe useful but may introduce bias)
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

        if psr_data.empty:
            print("WARNING: No PSR data — widget interaction scores will be zero.")
            return pd.DataFrame(columns=["Widget", "interaction_score"])

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

        if adoption_data.empty:
            print("WARNING: No adoption data — view interaction scores will be zero.")
            return pd.DataFrame(columns=["View", "interaction_score"])

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


    def generate_dimattr_ranks_from_logs_data(self, logs_data: pd.DataFrame) -> pd.DataFrame:
        """
        Compute a behavioural interaction score for each dimension attribute.
        Uses the same weighted log-compressed scoring as measures:
          - User_Freq (0.6) — breadth of adoption across distinct users
          - Global_Freq (0.4) — overall query volume

        :param logs_data: DataFrame with columns [DimAttr, Global_Freq, User_Freq]
        :return: DataFrame with columns [DimAttr, interaction_score]
        """
        data = logs_data.copy()
        for col in ["User_Freq", "Global_Freq"]:
            data[col] = pd.to_numeric(data[col], errors="coerce").clip(lower=0).fillna(0)

        data["interaction_score"] = self._compute_behavioural_score(
            data,
            terms=[(0.6, "User_Freq"), (0.4, "Global_Freq")],
        )
        return data[["DimAttr", "interaction_score"]]


    # Config-derived structural helpers -------------------------------------------------------------------------------

    def _get_measure_dimattr_edges(self, md_data: pd.DataFrame) -> pd.DataFrame:
        """
        Parse the Grain column from the measure-description config DataFrame to
        produce a flat Measure <-> DimAttr mapping.

        The Grain column contains a comma-separated string of [DimName].[AttrName]
        entries that define the grain (key attributes) for the measure group to
        which each measure belongs.  This method expands those strings into one
        row per (Measure, DimAttr) pair.

        :param md_data: DataFrame with at minimum columns [Measure, Grain],
                        as returned by get_dimensionattributes_from_config /
                        get_measuredescriptions_from_config.
        :return: Deduplicated DataFrame with columns [Measure, DimAttr].
        """
        rows = []
        subset = md_data[["Measure", "Grain"]].dropna(subset=["Measure", "Grain"]).copy()
        subset = subset[subset["Grain"].str.strip() != ""]

        # Extract all [DimName].[AttrName] tokens from each Grain string as a list
        subset["DimAttr"] = subset["Grain"].apply(
            lambda g: [
                f"[{d.strip()}].[{a.strip()}]"
                for d, a in re.findall(r"\[([^\]]+)\]\.\[([^\]]+)\]", g)
            ]
        )

        result = (
            subset[["Measure", "DimAttr"]]
            .explode("DimAttr")
            .dropna(subset=["DimAttr"])
            .drop_duplicates()
            .reset_index(drop=True)
        )

        return result if not result.empty else pd.DataFrame(columns=["Measure", "DimAttr"])

    def _compute_spread_scores(self, config_data: pd.DataFrame, md_data: pd.DataFrame) -> tuple:
        """
        Compute a structural spread score for widgets, measures, and dim.attrs.

        - Widget spread  : number of distinct Views that contain the widget
        - Measure spread : number of distinct Widgets that contain the measure
        - DimAttr spread : number of distinct Measures whose grain includes the dim.attr

        All spread scores are log-compressed and min-max normalised.

        :param config_data: View-Widget-Measure mapping from config zip
        :param md_data:     Measure-Grain mapping from config zip
        :return: Three DataFrames (widget_spread, measure_spread, dimattr_spread),
                 each with a [entity_col, spread_score] schema.
        """
        vw_data = config_data[["View", "Widget"]].drop_duplicates()
        wm_data = config_data[["Widget", "Measure"]].drop_duplicates()

        # --- Widget spread ---
        widget_spread = (
            vw_data.groupby("Widget")["View"]
            .nunique()
            .reset_index(name="View_Count")
        )

        # --- Measure spread ---
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
        dimattr_scores: pd.DataFrame,
        widget_spread: pd.DataFrame,
        measure_spread: pd.DataFrame,
    ) -> dict:
        """
        Combine behavioural interaction scores with structural spread scores into
        a single prior value per node.

        Views use only their behavioural score (no spread concept applies at that
        layer since views are the top of the hierarchy).
        Widgets, Measures, and DimAttrs use the weighted blend:
            prior = 0.7 * behavioural_score + 0.3 * spread_score
        """
        priors = {}

        # Views — behavioural only (top of hierarchy, no spread metric)
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

        # DimAttrs — behavioral only (absent in the 3-layer measure-ranking pass)
        if dimattr_scores is not None and not dimattr_scores.empty:
            for _, row in dimattr_scores.iterrows():
                priors[("dimattr", row["DimAttr"])] = float(row["interaction_score"])

        return priors


    def build_graph(
        self,
        config_data: pd.DataFrame,
        md_data: pd.DataFrame,
        view_scores: pd.DataFrame,
        widget_scores: pd.DataFrame,
        measure_scores: pd.DataFrame,
        dimattr_scores: pd.DataFrame,
        widget_spread: pd.DataFrame,
        measure_spread: pd.DataFrame,
    ) -> nx.DiGraph:
        """
        Construct the directed weighted graph used for PageRank.

        Node types  : view, widget, measure, dimattr
        Edge layers :
            View    <-> Widget   (from config_data View-Widget mapping)
            Widget  <-> Measure  (from config_data Widget-Measure mapping)
            Measure <-> DimAttr  (from md_data Grain column)

        Forward edges carry influence downward (parent -> child) proportional
        to the parent's score divided by its out-degree at that layer.
        Reverse edges carry influence upward (child -> parent) proportional
        to the child's score divided by its in-degree at that layer.
        Zero-weight edges are omitted to keep the graph sparse.
        """
        G = nx.DiGraph()

        priors = self._build_node_priors(
            view_scores, widget_scores, measure_scores, dimattr_scores,
            widget_spread, measure_spread,
        )

        # Add all nodes with their prior values
        for node, prior in priors.items():
            G.add_node(node, prior=prior)

        view_score_map    = view_scores.set_index("View")["interaction_score"].to_dict()
        widget_score_map  = widget_scores.set_index("Widget")["interaction_score"].to_dict()
        measure_score_map = measure_scores.set_index("Measure")["interaction_score"].to_dict()
        # dimattr_scores is None in the 3-layer (measure-ranking) pass
        dimattr_score_map = (
            dimattr_scores.set_index("DimAttr")["interaction_score"].to_dict()
            if dimattr_scores is not None and not dimattr_scores.empty
            else {}
        )

        # --- View <-> Widget edges ---
        vw_data = config_data[["View", "Widget"]].drop_duplicates()
        widget_count_per_view  = vw_data.groupby("View")["Widget"].nunique()
        view_count_per_widget  = vw_data.groupby("Widget")["View"].nunique()

        for _, row in vw_data.iterrows():
            view   = row["View"]
            widget = row["Widget"]
            view_score   = view_score_map.get(view, 0.0)
            widget_score = widget_score_map.get(widget, 0.0)
            w_count = widget_count_per_view.get(view, 0)
            v_count = view_count_per_widget.get(widget, 0)

            # Ensure nodes exist even if absent from logs
            if ("view", view) not in G:
                G.add_node(("view", view), prior=0.0)
            if ("widget", widget) not in G:
                G.add_node(("widget", widget), prior=0.0)

            # forward edge: view -> widget
            forward_weight = (view_score * FORWARD_EDGE_DAMPING) / w_count if w_count > 0 else 0.0
            if forward_weight > 0:
                G.add_edge(("view", view), ("widget", widget), weight=forward_weight)

            # reverse edge: widget -> view
            reverse_weight = (widget_score * REVERSE_EDGE_DAMPING) / v_count if v_count > 0 else 0.0
            if reverse_weight > 0:
                G.add_edge(("widget", widget), ("view", view), weight=reverse_weight)

        # --- Widget <-> Measure edges ---
        wm_data = config_data[["Widget", "Measure"]].drop_duplicates()
        measure_count_per_widget = wm_data.groupby("Widget")["Measure"].nunique()
        widget_count_per_measure = wm_data.groupby("Measure")["Widget"].nunique()

        for _, row in wm_data.iterrows():
            widget  = row["Widget"]
            measure = row["Measure"]
            widget_score  = widget_score_map.get(widget, 0.0)
            measure_score = measure_score_map.get(measure, 0.0)
            m_count = measure_count_per_widget.get(widget, 0)
            w_count = widget_count_per_measure.get(measure, 0)

            # Ensure nodes exist even if absent from logs
            if ("widget", widget) not in G:
                G.add_node(("widget", widget), prior=0.0)
            if ("measure", measure) not in G:
                G.add_node(("measure", measure), prior=0.0)

            # forward edge: widget -> measure
            forward_weight = (widget_score * FORWARD_EDGE_DAMPING) / m_count if m_count > 0 else 0.0
            if forward_weight > 0:
                G.add_edge(("widget", widget), ("measure", measure), weight=forward_weight)

            # reverse edge: measure -> widget
            reverse_weight = (measure_score * REVERSE_EDGE_DAMPING) / w_count if w_count > 0 else 0.0
            if reverse_weight > 0:
                G.add_edge(("measure", measure), ("widget", widget), weight=reverse_weight)

        # --- Measure <-> DimAttr edges ---
        # Only built in the full 4-layer pass (dimattr_scores is not None).
        # Skipped entirely in the 3-layer measure-ranking pass to prevent
        # dim-attr behavioral scores from bleeding back into measure ranks.
        mda_data = self._get_measure_dimattr_edges(md_data)
        if dimattr_scores is not None and not mda_data.empty:
            dimattr_count_per_measure = mda_data.groupby("Measure")["DimAttr"].nunique()
            measure_count_per_dimattr = mda_data.groupby("DimAttr")["Measure"].nunique()

            for _, row in mda_data.iterrows():
                measure = row["Measure"]
                dimattr = row["DimAttr"]
                measure_score = measure_score_map.get(measure, 0.0)
                dimattr_score = dimattr_score_map.get(dimattr, 0.0)
                da_count = dimattr_count_per_measure.get(measure, 0)
                m_count  = measure_count_per_dimattr.get(dimattr, 0)

                # Ensure nodes exist even if absent from logs
                if ("measure", measure) not in G:
                    G.add_node(("measure", measure), prior=0.0)
                if ("dimattr", dimattr) not in G:
                    G.add_node(("dimattr", dimattr), prior=0.0)

                # forward edge: measure -> dimattr
                forward_weight = (measure_score * FORWARD_EDGE_DAMPING) / da_count if da_count > 0 else 0.0
                if forward_weight > 0:
                    G.add_edge(("measure", measure), ("dimattr", dimattr), weight=forward_weight)

                # reverse edge: dimattr -> measure
                reverse_weight = (dimattr_score * REVERSE_EDGE_DAMPING) / m_count if m_count > 0 else 0.0
                if reverse_weight > 0:
                    G.add_edge(("dimattr", dimattr), ("measure", measure), weight=reverse_weight)

        return G

    # PageRank ---------------------------------------------------------------------------------------------------------

    def run_pagerank(self, G: nx.DiGraph) -> dict:
        nodes = list(G.nodes())
        N = len(nodes)
        # index of each node in the graph
        node_idx = {node: i for i, node in enumerate(nodes)}

        # initialize the personalization matrix (nodes x nodes)
        P = np.zeros((N, N))
        # get the starting scores of all nodes (complete node information)
        priors = nx.get_node_attributes(G, "prior")
        # following dict will have only one element per node type
        type_distributions = {}

        for ntype in ["view", "widget", "measure", "dimattr"]:
            same_type_nodes = [(j, node) for j, node in enumerate(nodes) if node[0] == ntype]
            type_total = sum(priors[node] for _, node in same_type_nodes) or 1.0
            dist = {j: priors[node] / type_total for j, node in same_type_nodes}
            type_distributions[ntype] = dist

        # populate the personalization matrix: only same-type index pairs carry weight
        for i, src_node in enumerate(nodes):
            src_type = src_node[0]
            for j, weight in type_distributions[src_type].items():
                P[i][j] = weight

        # Build weighted propagation matrix from graph edges
        T = np.zeros((N, N))
        for src, dst, data in G.edges(data=True):
            T[node_idx[src]][node_idx[dst]] = data.get("weight", 0.0)

        # Normalise edge weights row-wise (each row = outgoing edges from node i)
        row_sums = T.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        T = T / row_sums

        # PageRank iteration
        alpha = PAGERANK_DAMPING
        # initialise starting ranks from priors
        prior_values = np.array([priors.get(node, 0.0) for node in nodes])
        prior_sum = prior_values.sum() or 1.0
        ranks = prior_values / prior_sum

        for _ in range(PAGERANK_MAX_ITER):
            new_ranks = alpha * (ranks @ T) + (1 - alpha) * (ranks @ P)
            if np.abs(new_ranks - ranks).sum() < PAGERANK_TOL:
                break
            ranks = new_ranks

        return {node: float(ranks[node_idx[node]]) for node in nodes}

    # Importance scores ------------------------------------------------------------------------------------------------

    def compute_final_importance(
        self,
        ranks: dict,
        widget_scores: pd.DataFrame,
        measure_scores: pd.DataFrame,
        dimattr_scores: pd.DataFrame,
    ) -> tuple:
        """
        Extract per-entity PageRank scores from the rank dict and merge them
        with the original behavioural interaction scores.

        :return: Three DataFrames sorted descending by pagerank_score:
                 (measure_final, widget_final, dimattr_final)
        """
        widget_pr  = {node[1]: score for node, score in ranks.items() if node[0] == "widget"}
        measure_pr = {node[1]: score for node, score in ranks.items() if node[0] == "measure"}
        dimattr_pr = {node[1]: score for node, score in ranks.items() if node[0] == "dimattr"}

        widget_pr_df  = pd.DataFrame(widget_pr.items(),  columns=["Widget",  "pagerank_score"])
        measure_pr_df = pd.DataFrame(measure_pr.items(), columns=["Measure", "pagerank_score"])
        dimattr_pr_df = pd.DataFrame(dimattr_pr.items(), columns=["DimAttr", "pagerank_score"])

        # Merge with behavioural scores
        widget_final  = widget_pr_df.merge(widget_scores,  on="Widget",  how="outer").fillna(0)
        measure_final = measure_pr_df.merge(measure_scores, on="Measure", how="outer").fillna(0)
        dimattr_final = dimattr_pr_df.merge(dimattr_scores, on="DimAttr", how="outer").fillna(0)

        return (
            measure_final[["Measure", "pagerank_score", "interaction_score"]].sort_values("pagerank_score", ascending=False),
            widget_final[["Widget",  "pagerank_score", "interaction_score"]].sort_values("pagerank_score", ascending=False),
            dimattr_final[["DimAttr", "pagerank_score", "interaction_score"]].sort_values("pagerank_score", ascending=False),
        )

    # Main entry -------------------------------------------------------------------------------------------------------

    def generate_ranks(
        self,
        config_data: pd.DataFrame,
        md_data: pd.DataFrame,
        view_scores: pd.DataFrame,
        widget_scores: pd.DataFrame,
        measure_scores: pd.DataFrame,
        dimattr_scores: pd.DataFrame,
    ) -> tuple:
        """
        Full ranking pipeline entry point.

        :param config_data:   View-Widget-Measure mapping from config zip
        :param md_data:       Measure-Grain mapping from config zip
                              (used to build Measure <-> DimAttr edges)
        :param view_scores:   Behavioural scores for views
        :param widget_scores: Behavioural scores for widgets
        :param measure_scores:Behavioural scores for measures
        :param dimattr_scores:Behavioural scores for dimension attributes
        :return: (measure_final, widget_final, dimattr_final) DataFrames
                 sorted by pagerank_score descending
        """
        widget_spread, measure_spread = self._compute_spread_scores(
            config_data, md_data
        )

        G_measures = self.build_graph(
            config_data,
            md_data,
            view_scores,
            widget_scores,
            measure_scores,
            None,
            widget_spread,
            measure_spread,
        )
        ranks_measures = self.run_pagerank(G_measures)

        G_full = self.build_graph(
            config_data,
            md_data,
            view_scores,
            widget_scores,
            measure_scores,
            dimattr_scores,
            widget_spread,
            measure_spread,
        )
        ranks_full = self.run_pagerank(G_full)

        # measure_final, widget_final, dimattr_final = self.compute_final_importance(
        #     ranks, widget_scores, measure_scores, dimattr_scores
        # )
        measure_final, widget_final, _ = self.compute_final_importance(ranks_measures, widget_scores, measure_scores,
                                                                       dimattr_scores)
        _, _, dimattr_final = self.compute_final_importance(ranks_full, widget_scores, measure_scores, dimattr_scores)

        return measure_final, widget_final, dimattr_final

        # v_models = visualise_models()
        # v_models.visualize_graph(G, measure_final, widget_final, output_path="graph.html")