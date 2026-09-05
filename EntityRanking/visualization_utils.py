from pyvis.network import Network
import networkx as nx
import pandas as pd

class visualise_models():
    def __init__(self):
        pass

    def visualize_graph(
            self,
            G: nx.DiGraph,
            measure_ranks: pd.DataFrame,
            widget_ranks: pd.DataFrame,
            output_path: str = "graph.html",
            top_k: int = 50,
    ) -> None:

        measure_importance = measure_ranks.set_index("Measure")["pagerank_score"].to_dict()
        widget_importance = widget_ranks.set_index("Widget")["pagerank_score"].to_dict()

        # --- Determine which nodes to show ---
        top_measures = set(measure_ranks.head(100)["Measure"].tolist())
        top_widgets = set(widget_ranks.head(50)["Widget"].tolist())
        # top_measures = set(measure_ranks["Measure"].tolist())
        # top_widgets = set(widget_ranks["Widget"].tolist())

        def should_include(node):
            ntype, name = node
            if ntype == "view":
                return True
            if ntype == "widget":
                return name in top_widgets
            if ntype == "measure":
                return name in top_measures
            return False

        visible_nodes = {n for n in G.nodes() if should_include(n)}

        TYPE_COLOR = {
            "view": "#4C9BE8",  # blue
            "widget": "#F4A261",  # orange
            "measure": "#2A9D8F",  # teal
        }
        BASE_SIZE = 10
        MAX_SIZE = 50

        def get_size(node):
            ntype, name = node
            if ntype == "view":
                return BASE_SIZE
            score = (
                widget_importance.get(name, 0.0)
                if ntype == "widget"
                else measure_importance.get(name, 0.0)
            )
            return BASE_SIZE + score * (MAX_SIZE - BASE_SIZE)

        net = Network(
            height="900px",
            width="100%",
            directed=True,
            bgcolor="#1a1a2e",
            font_color="white",
        )
        net.barnes_hut(
            gravity=-8000,
            central_gravity=0.3,
            spring_length=150,
            spring_strength=0.05,
            damping=0.09,
        )

        for node in visible_nodes:
            ntype, name = node
            net.add_node(
                str(node),
                label=name,
                color=TYPE_COLOR[ntype],
                size=get_size(node),
                title=(
                    f"Type: {ntype}\n"
                    f"Name: {name}\n"
                    f"PageRank: {float(measure_importance.get(name, widget_importance.get(name, '0.00'))):.4f}"
                ),
                shape="dot",
            )

        all_weights = [
            d.get("weight", 0.0)
            for u, v, d in G.edges(data=True)
            if u in visible_nodes and v in visible_nodes
        ]
        max_weight = max(all_weights) if all_weights else 1.0

        for u, v, data in G.edges(data=True):
            if u not in visible_nodes or v not in visible_nodes:
                continue
            weight = data.get("weight", 0.0)
            normalized_weight = weight / (max_weight)
            net.add_edge(
                str(u),
                str(v),
                value=normalized_weight,
                color=f"rgba(255,255,255,{max(0.1, normalized_weight):.2f})",
                title=f"weight: {weight:.4f}",
            )

        net.save_graph(output_path)
        print(f"Graph saved to {output_path}")