"""
Clustering Visualisation
=========================
Generates a single self-contained HTML file with four interactive
panels to help tune clustering parameters.

  Tab 1 — Structural graph      : force-directed layout, cluster colours,
                                  edge weight = thickness + opacity
  Tab 2 — Semantic heatmap      : similarity matrix reordered by cluster,
                                  block structure visible
  Tab 3 — Behavioral graph      : same as structural but for PMI graph
  Tab 4 — Resolution sweep      : staircase plot for structural + behavioral
                                  across a range of γ values

Usage
-----
    from visualise import build_visualisation

    html_path = build_visualisation(
        struct_G      = struct_G,         # nx.Graph from l1_structural
        struct_labels = struct_labels,    # dict {measure: cluster_id}
        sem_S         = 1 - sem_D,        # similarity = 1 - distance matrix
        sem_measures  = working_set,      # ordered list matching sem_S rows
        sem_labels    = sem_labels,       # dict {measure: cluster_id}
        beh_G         = beh_G,            # nx.Graph from l1_behavioral
        beh_labels    = beh_labels,       # dict {measure: cluster_id}
        # --- for resolution sweep ---
        df_vwml       = df_vwml,
        df_md         = df_md,
        beh_df        = beh_df,
        working_set   = working_set,
        struct_params = STRUCTURAL_PARAMS,
        beh_params    = BEHAVIORAL_PARAMS,
        output_path   = "clustering_vis.html",
    )
"""

import numpy as np
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Colour palette — 12 distinct colours for cluster IDs, grey for -1
_PALETTE = [
    "#378ADD", "#1D9E75", "#D85A30", "#7F77DD", "#BA7517",
    "#D4537E", "#639922", "#E24B4A", "#085041", "#993C1D",
    "#534AB7", "#0F6E56",
]
_HUB_COLOUR = "#B4B2A9"


def _cluster_colour(cid: int) -> str:
    if cid == -1:
        return _HUB_COLOUR
    return _PALETTE[cid % len(_PALETTE)]


# ---------------------------------------------------------------------------
# Tab 1 & 3 — Graph (shared logic)
# ---------------------------------------------------------------------------

def _spring_layout(G: nx.Graph, seed: int = 42) -> dict:
    if G.number_of_nodes() == 0:
        return {}
    pos = nx.spring_layout(G, weight="weight", seed=seed, k=2.5)
    return pos


def _graph_figure(
    G:      nx.Graph,
    labels: dict,
    title:  str,
) -> go.Figure:
    """
    Force-directed node-link diagram.
    Edge thickness + opacity encode weight.
    Node colour encodes cluster.
    Node size encodes weighted degree (importance proxy).
    """
    pos = _spring_layout(G)
    if not pos:
        return go.Figure().update_layout(title=title)

    # ----- edges -----
    edge_traces = []
    weights = [d.get("weight", 1.0) for _, _, d in G.edges(data=True)]
    max_w   = max(weights) if weights else 1.0

    for (u, v, d) in G.edges(data=True):
        w     = d.get("weight", 1.0)
        alpha = 0.15 + 0.65 * (w / max_w)
        width = 0.5  + 3.5  * (w / max_w)
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode="lines",
            line=dict(width=width, color=f"rgba(136,135,128,{alpha:.2f})"),
            hoverinfo="none",
            showlegend=False,
        ))

    # ----- nodes -----
    # group by cluster for legend
    cluster_ids = sorted(set(labels.values()))
    node_traces = []

    for cid in cluster_ids:
        members  = [m for m, c in labels.items() if c == cid and m in pos]
        if not members:
            continue
        label_str = f"Cluster {cid}" if cid != -1 else "Hub / isolated"

        xs, ys, texts, sizes = [], [], [], []
        for m in members:
            x, y = pos[m]
            xs.append(x); ys.append(y)
            deg  = G.degree(m, weight="weight") if m in G else 0
            texts.append(f"<b>{m}</b><br>cluster: {label_str}<br>weighted degree: {deg:.2f}")
            sizes.append(10 + 18 * min(deg / (max_w * len(G) + 1e-9), 1.0))

        node_traces.append(go.Scatter(
            x=xs, y=ys,
            mode="markers+text",
            marker=dict(size=sizes, color=_cluster_colour(cid),
                        line=dict(width=1, color="white")),
            text=members,
            textposition="top center",
            textfont=dict(size=9),
            hovertext=texts,
            hoverinfo="text",
            name=label_str,
        ))

    fig = go.Figure(data=edge_traces + node_traces)
    fig.update_layout(
        title=dict(text=title, font=dict(size=14)),
        showlegend=True,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(font=dict(size=11)),
    )
    return fig


# ---------------------------------------------------------------------------
# Tab 2 — Semantic heatmap
# ---------------------------------------------------------------------------

def _semantic_heatmap(
    S:        np.ndarray,
    measures: list,
    labels:   dict,
) -> go.Figure:
    """
    Similarity matrix reordered so same-cluster measures are adjacent.
    Block boundaries drawn as white lines.
    """
    # Reorder rows/cols by cluster then alphabetically within cluster
    order = sorted(range(len(measures)),
                   key=lambda i: (labels.get(measures[i], 999), measures[i]))
    ordered_measures = [measures[i] for i in order]
    S_ordered        = S[np.ix_(order, order)]

    # Cluster boundary positions
    boundaries = []
    prev_cid   = None
    for k, m in enumerate(ordered_measures):
        cid = labels.get(m, -1)
        if cid != prev_cid and k > 0:
            boundaries.append(k - 0.5)
        prev_cid = cid

    # Truncate long names for axis labels
    short_names = [m[:28] + "…" if len(m) > 28 else m for m in ordered_measures]

    fig = go.Figure(go.Heatmap(
        z=S_ordered,
        x=short_names,
        y=short_names,
        colorscale=[
            [0.0, "#EEEDFE"], [0.3, "#AFA9EC"],
            [0.6, "#7F77DD"], [1.0, "#26215C"],
        ],
        zmin=0, zmax=1,
        colorbar=dict(title="similarity", thickness=12),
        hovertemplate="row: %{y}<br>col: %{x}<br>similarity: %{z:.3f}<extra></extra>",
    ))

    # Cluster boundary lines
    n = len(ordered_measures)
    for b in boundaries:
        fig.add_shape(type="line", x0=b, x1=b, y0=-0.5, y1=n - 0.5,
                      line=dict(color="white", width=2))
        fig.add_shape(type="line", y0=b, y1=b, x0=-0.5, x1=n - 0.5,
                      line=dict(color="white", width=2))

    fig.update_layout(
        title=dict(text="Semantic similarity matrix (reordered by cluster)", font=dict(size=14)),
        xaxis=dict(tickfont=dict(size=8), tickangle=-45),
        yaxis=dict(tickfont=dict(size=8), autorange="reversed"),
        margin=dict(l=120, r=20, t=50, b=120),
    )
    return fig


# ---------------------------------------------------------------------------
# Tab 4 — Resolution sweep
# ---------------------------------------------------------------------------

def _resolution_sweep(
    df_vwml:      pd.DataFrame,
    df_md:        pd.DataFrame,
    beh_df:       pd.DataFrame,
    working_set:  list,
    struct_params: dict,
    beh_params:   dict,
    gammas:       list | None = None,
) -> go.Figure:
    """
    Staircase plot: n_clusters vs γ for both structural and behavioral.
    Helps choose resolution visually without running the full pipeline.
    """
    from l1_structural  import build_structural_graph
    from l1_behavioral  import build_behavioral_graph
    from _community_detection import run_community_detection

    if gammas is None:
        gammas = [round(x, 3) for x in np.linspace(0.5, 2.5, 60)]

    # Build graphs once — only resolution changes
    struct_G = build_structural_graph(
        df_vwml, df_md, working_set,
        w_widget=struct_params.get("w_widget", 0.5),
        w_grain=struct_params.get("w_grain", 0.3),
        w_mg=struct_params.get("w_mg", 0.2),
        min_edge_weight=struct_params.get("min_edge_weight", 0.0),
    )
    beh_G = build_behavioral_graph(
        beh_df, working_set,
        min_pmi=beh_params.get("min_pmi", 0.1),
    )

    algo_s  = struct_params.get("algorithm", "leiden")
    algo_b  = beh_params.get("algorithm", "leiden")
    part_s  = struct_params.get("leiden_partition", "RBConfiguration")
    part_b  = beh_params.get("leiden_partition", "RBConfiguration")
    iters_s = struct_params.get("leiden_n_iterations", 10)
    iters_b = beh_params.get("leiden_n_iterations", 10)
    seed    = 42

    n_struct, n_beh = [], []
    for g in gammas:
        sl = run_community_detection(struct_G, algorithm=algo_s, resolution=g,
                                     seed=seed, leiden_partition=part_s,
                                     leiden_n_iterations=iters_s)
        bl = run_community_detection(beh_G,    algorithm=algo_b, resolution=g,
                                     seed=seed, leiden_partition=part_b,
                                     leiden_n_iterations=iters_b)
        n_struct.append(len({v for v in sl.values() if v != -1}))
        n_beh.append(  len({v for v in bl.values() if v != -1}))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=gammas, y=n_struct, mode="lines+markers",
        name=f"Structural ({algo_s}/{part_s if algo_s=='leiden' else 'N/A'})",
        line=dict(color="#1D9E75", width=2, shape="hv"),
        marker=dict(size=4),
        hovertemplate="γ=%{x:.3f}  clusters=%{y}<extra>Structural</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=gammas, y=n_beh, mode="lines+markers",
        name=f"Behavioral ({algo_b}/{part_b if algo_b=='leiden' else 'N/A'})",
        line=dict(color="#D85A30", width=2, shape="hv"),
        marker=dict(size=4),
        hovertemplate="γ=%{x:.3f}  clusters=%{y}<extra>Behavioral</extra>",
    ))

    # Vertical line at current resolution
    curr_s = struct_params.get("resolution", 1.0)
    curr_b = beh_params.get("resolution", 1.0)
    for xval, colour, label in [
        (curr_s, "#1D9E75", f"γ_struct = {curr_s}"),
        (curr_b, "#D85A30", f"γ_beh = {curr_b}"),
    ]:
        fig.add_vline(x=xval, line=dict(color=colour, dash="dot", width=1.5),
                      annotation_text=label, annotation_font_size=10)

    fig.update_layout(
        title=dict(text="Resolution sweep — n_clusters vs γ", font=dict(size=14)),
        xaxis=dict(title="resolution γ", gridcolor="#E8E8E8"),
        yaxis=dict(title="number of clusters", gridcolor="#E8E8E8",
                   tickmode="linear", dtick=1),
        plot_bgcolor="white",
        legend=dict(font=dict(size=11)),
        margin=dict(l=60, r=20, t=50, b=50),
    )
    return fig


# ---------------------------------------------------------------------------
# Assemble HTML
# ---------------------------------------------------------------------------

def build_visualisation(
    struct_G:      nx.Graph,
    struct_labels: dict,
    sem_S:         np.ndarray,
    sem_measures:  list,
    sem_labels:    dict,
    beh_G:         nx.Graph,
    beh_labels:    dict,
    # --- resolution sweep inputs ---
    df_vwml:       pd.DataFrame | None = None,
    df_md:         pd.DataFrame | None = None,
    beh_df:        pd.DataFrame | None = None,
    working_set:   list | None         = None,
    struct_params: dict | None         = None,
    beh_params:    dict | None         = None,
    sweep_gammas:  list | None         = None,
    output_path:   str = "clustering_vis.html",
) -> str:
    """
    Build all four figures and write a single self-contained HTML file.

    Returns the output path.
    """
    import plotly.io as pio

    print("  Building structural graph figure...")
    fig_struct = _graph_figure(
        struct_G, struct_labels,
        f"Structural graph  ({len({v for v in struct_labels.values() if v!=-1})} clusters)"
    )

    print("  Building semantic heatmap...")
    fig_sem = _semantic_heatmap(sem_S, sem_measures, sem_labels)

    print("  Building behavioral graph figure...")
    fig_beh = _graph_figure(
        beh_G, beh_labels,
        f"Behavioral graph  ({len({v for v in beh_labels.values() if v!=-1})} clusters)"
    )

    has_sweep = all(x is not None for x in [df_vwml, df_md, beh_df, working_set,
                                             struct_params, beh_params])
    if has_sweep:
        print("  Running resolution sweep (this may take ~10s)...")
        fig_sweep = _resolution_sweep(
            df_vwml, df_md, beh_df, working_set,
            struct_params, beh_params, sweep_gammas,
        )
    else:
        fig_sweep = go.Figure().update_layout(
            title="Resolution sweep — pass df_vwml, df_md, beh_df, "
                  "working_set, struct_params, beh_params to enable"
        )

    # Assemble as tabbed HTML
    div_struct = pio.to_html(fig_struct, full_html=False, include_plotlyjs=False)
    div_sem    = pio.to_html(fig_sem,    full_html=False, include_plotlyjs=False)
    div_beh    = pio.to_html(fig_beh,    full_html=False, include_plotlyjs=False)
    div_sweep  = pio.to_html(fig_sweep,  full_html=False, include_plotlyjs=False)

    # Cluster stats table
    def _stats_table(labels: dict, G: nx.Graph | None = None) -> str:
        from collections import Counter
        counts = Counter(v for v in labels.values())
        rows = ""
        for cid in sorted(counts.keys()):
            members = sorted(m for m, v in labels.items() if v == cid)
            label   = f"Cluster {cid}" if cid != -1 else "Hub / isolated"
            colour  = _cluster_colour(cid)
            rows += (
                f"<tr>"
                f"<td><span style='background:{colour};color:white;"
                f"padding:2px 8px;border-radius:3px;font-size:11px'>{label}</span></td>"
                f"<td style='text-align:center'>{counts[cid]}</td>"
                f"<td style='font-size:11px;color:#555'>{', '.join(members)}</td>"
                f"</tr>"
            )
        return (
            "<table style='width:100%;border-collapse:collapse;font-size:12px'>"
            "<thead><tr style='background:#f5f5f5'>"
            "<th style='text-align:left;padding:6px'>Cluster</th>"
            "<th style='padding:6px'>Size</th>"
            "<th style='text-align:left;padding:6px'>Members</th>"
            "</tr></thead><tbody>" + rows + "</tbody></table>"
        )

    stats_struct = _stats_table(struct_labels, struct_G)
    stats_sem    = _stats_table(sem_labels)
    stats_beh    = _stats_table(beh_labels, beh_G)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Clustering visualisation</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  body {{ font-family: -apple-system, sans-serif; margin: 0; padding: 16px;
          background: #fafafa; color: #222; }}
  h1   {{ font-size: 18px; font-weight: 500; margin: 0 0 16px; }}
  .tabs  {{ display: flex; gap: 4px; margin-bottom: 16px; flex-wrap: wrap; }}
  .tab   {{ padding: 7px 18px; border: 1px solid #ccc; border-radius: 4px;
             background: white; cursor: pointer; font-size: 13px; }}
  .tab.active {{ background: #378ADD; color: white; border-color: #378ADD; }}
  .panel {{ display: none; }}
  .panel.active {{ display: block; }}
  .stats {{ margin-top: 12px; background: white; border: 1px solid #e8e8e8;
             border-radius: 6px; padding: 12px; }}
  .stats h3 {{ font-size: 13px; font-weight: 500; margin: 0 0 8px; color: #555; }}
  td, th {{ padding: 5px 10px; border-bottom: 1px solid #eee; }}
</style>
</head>
<body>
<h1>Clustering visualisation</h1>
<div class="tabs">
  <button class="tab active"  onclick="show(0)">Structural graph</button>
  <button class="tab"         onclick="show(1)">Semantic heatmap</button>
  <button class="tab"         onclick="show(2)">Behavioral graph</button>
  <button class="tab"         onclick="show(3)">Resolution sweep</button>
</div>

<div id="p0" class="panel active">
  {div_struct}
  <div class="stats"><h3>Structural cluster membership</h3>{stats_struct}</div>
</div>
<div id="p1" class="panel">
  {div_sem}
  <div class="stats"><h3>Semantic cluster membership</h3>{stats_sem}</div>
</div>
<div id="p2" class="panel">
  {div_beh}
  <div class="stats"><h3>Behavioral cluster membership</h3>{stats_beh}</div>
</div>
<div id="p3" class="panel">
  {div_sweep}
  <div class="stats" style="font-size:12px;color:#555">
    Dotted vertical lines mark the current γ values from STRUCTURAL_PARAMS and
    BEHAVIORAL_PARAMS. The step function shows where each γ increment causes a
    split — look for stable plateaus (good γ choices) vs cliffs (fragile zones).
  </div>
</div>

<script>
function show(idx) {{
  document.querySelectorAll('.panel').forEach((p, i) => {{
    p.classList.toggle('active', i === idx);
  }});
  document.querySelectorAll('.tab').forEach((t, i) => {{
    t.classList.toggle('active', i === idx);
  }});
  // Trigger plotly resize after tab switch
  setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
}}
</script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Saved: {output_path}")
    return output_path
