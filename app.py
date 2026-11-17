import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ───────────────────────────────────────────────────────────────
# Page config
# ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SuperRR Selector · Season 2",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────────────────────────────────────────────
# Custom CSS — dark cricket-analytics theme
# ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Global ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
.stApp {
    background: linear-gradient(145deg, #0a0e1a 0%, #111827 50%, #0d1321 100%);
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1729 0%, #131d33 100%);
    border-right: 1px solid rgba(99,102,241,0.15);
}
[data-testid="stSidebar"] .stMarkdown h2 { color: #f4b942; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1500px; }

/* ---- Hero banner ---- */
.hero-container {
    background: linear-gradient(135deg, #1e1145 0%, #0f172a 40%, #0c2d48 100%);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute; top: -50%; right: -20%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(244,185,66,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.6rem; font-weight: 900;
    background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0; line-height: 1.2;
}
.hero-accent { -webkit-text-fill-color: #f4b942; }
.hero-sub { color: #94a3b8; font-size: 1rem; margin-top: .5rem; font-weight: 500; }
.hero-badge {
    display: inline-block;
    background: rgba(244,185,66,0.15); color: #f4b942;
    padding: 4px 14px; border-radius: 20px;
    font-size: .78rem; font-weight: 600;
    margin-top: .6rem; border: 1px solid rgba(244,185,66,0.3);
}

/* ---- KPI cards ---- */
.kpi-card {
    background: linear-gradient(145deg, #161e35 0%, #111827 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px; padding: 20px 22px;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); border-color: rgba(244,185,66,0.4); }
.kpi-icon { font-size: 1.6rem; margin-bottom: 4px; }
.kpi-value {
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, #f4b942, #fbbf24);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.kpi-label { font-size: .78rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: .5px; margin-top: 2px; }

/* ---- Section headers ---- */
.section-header {
    font-size: 1.4rem; font-weight: 800; color: #f8fafc;
    margin: 1.6rem 0 .8rem 0;
    padding-bottom: .4rem;
    border-bottom: 2px solid rgba(244,185,66,0.3);
    display: inline-block;
}

/* ---- Rank badges ---- */
.rank-gold { color: #f4b942; font-weight: 800; }
.rank-silver { color: #c0c0c0; font-weight: 700; }
.rank-bronze { color: #cd7f32; font-weight: 700; }

/* ---- Tables ---- */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    overflow: hidden;
}

/* ---- Info / caption ---- */
.methodology-card {
    background: linear-gradient(145deg, #161e35, #111827);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px; padding: 24px;
    margin-bottom: 1rem;
}
.method-title { font-size: 1rem; font-weight: 700; color: #f4b942; margin-bottom: 8px; }
.method-text { color: #cbd5e1; font-size: .9rem; line-height: 1.6; }

/* Footer */
.footer-text {
    text-align: center; color: #64748b; font-size: .8rem;
    padding: 1rem 0; margin-top: 2rem;
    border-top: 1px solid rgba(99,102,241,0.1);
}
</style>
""", unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
# Plotly theme helper
# ───────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#e2e8f0"),
    margin=dict(l=10, r=10, t=40, b=10),
    hoverlabel=dict(bgcolor="#1e293b", font_size=13, font_color="#f8fafc"),
)

GOLD = "#f4b942"
ACCENT_BAT = ["#312e81", "#4338ca", "#6366f1", "#818cf8", "#a5b4fc", "#c7d2fe", "#e0e7ff", GOLD, "#fbbf24", "#f59e0b"]
ACCENT_BOWL = ["#134e4a", "#0f766e", "#14b8a6", "#2dd4bf", "#5eead4", "#99f6e4", "#b2f5ea", GOLD, "#fbbf24", "#f59e0b"]


# ───────────────────────────────────────────────────────────────
# Data loading
# ───────────────────────────────────────────────────────────────
DATA = Path(__file__).parent / "data"

@st.cache_data
def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / name)

bat = load_csv("overall_top10_batters.csv")
bowl = load_csv("overall_top10_bowlers.csv")
sens = load_csv("sensitivity_summary.csv")
method = load_csv("methodology.csv")

bat["final_score"] = pd.to_numeric(bat["final_score"], errors="coerce").round(2)
bowl["final_score"] = pd.to_numeric(bowl["final_score"], errors="coerce").round(2)

bat_name = "striker_name"
bowl_name = "bowler_name_pressure"


# ───────────────────────────────────────────────────────────────
# Hero banner
# ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🏏 SUPERRR SELECTOR <span class="hero-accent">SEASON 2</span></div>
    <div class="hero-sub">Pressure-based player evaluation engine · IPL + T20 International · 2022 onwards</div>
    <span class="hero-badge">📊 Primary Model — Top 25 % Pressure Index</span>
</div>
""", unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
# Sidebar
# ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏏 Navigation")
    page = st.radio(
        "Go to",
        ["🏠 Overview", "🏏 Batting", "🎯 Bowling", "📊 Sensitivity", "🔬 Methodology"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("#### ⚙️ Model Settings")
    st.markdown("""
    - **Threshold:** Top 25 %
    - **Formats:** IPL + T20I
    - **Period:** 2022 →
    """)
    st.markdown("---")
    st.caption("Built with Streamlit · Data-driven cricket analytics")


# ===================================================================
# PAGE — Overview
# ===================================================================
if page == "🏠 Overview":

    # --- KPI row ---
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        ("🏏", "10", "Top Batters"),
        ("🎯", "10", "Top Bowlers"),
        ("📅", "853", "Matches Analysed"),
        ("🌍", "IPL + T20I", "Formats Covered"),
    ]
    for col, (icon, value, label) in zip([c1, c2, c3, c4], kpis):
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # --- Top Batters section ---
    st.markdown('<div class="section-header">🏏 Top 10 Batters — Pressure Performance</div>', unsafe_allow_html=True)

    left, right = st.columns([2, 3])

    with left:
        display_bat = bat[["Rank", bat_name, "final_score", "pressure_balls", "pressure_runs", "formats"]].copy()
        display_bat.columns = ["#", "Player", "Score", "P. Balls", "P. Runs", "Format"]
        st.dataframe(display_bat, hide_index=True, use_container_width=True, height=420)

    with right:
        bat_sorted = bat.sort_values("final_score", ascending=True)
        colors = [GOLD if i == len(bat_sorted) - 1 else "#6366f1" for i in range(len(bat_sorted))]
        fig = go.Figure(go.Bar(
            x=bat_sorted["final_score"],
            y=bat_sorted[bat_name],
            orientation="h",
            marker=dict(color=colors, line=dict(width=0), cornerradius=6),
            text=bat_sorted["final_score"].round(1),
            textposition="outside",
            textfont=dict(color="#e2e8f0", size=12, family="Inter"),
            hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>",
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=420,
            title=dict(text="Model Score Distribution", font=dict(size=15, color="#94a3b8")),
            xaxis=dict(title="Score", gridcolor="rgba(99,102,241,0.08)", range=[0, 100]),
            yaxis=dict(title=""),
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- Top Bowlers section ---
    st.markdown('<div class="section-header">🎯 Top 10 Bowlers — Pressure Performance</div>', unsafe_allow_html=True)

    left2, right2 = st.columns([2, 3])

    with left2:
        display_bowl = bowl[["Rank", bowl_name, "final_score", "pressure_balls", "pressure_wickets", "formats"]].copy()
        display_bowl.columns = ["#", "Player", "Score", "P. Balls", "P. Wkts", "Format"]
        st.dataframe(display_bowl, hide_index=True, use_container_width=True, height=420)

    with right2:
        bowl_sorted = bowl.sort_values("final_score", ascending=True)
        colors_b = [GOLD if i == len(bowl_sorted) - 1 else "#14b8a6" for i in range(len(bowl_sorted))]
        fig2 = go.Figure(go.Bar(
            x=bowl_sorted["final_score"],
            y=bowl_sorted[bowl_name],
            orientation="h",
            marker=dict(color=colors_b, line=dict(width=0), cornerradius=6),
            text=bowl_sorted["final_score"].round(1),
            textposition="outside",
            textfont=dict(color="#e2e8f0", size=12, family="Inter"),
            hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>",
        ))
        fig2.update_layout(
            **PLOTLY_LAYOUT,
            height=420,
            title=dict(text="Model Score Distribution", font=dict(size=15, color="#94a3b8")),
            xaxis=dict(title="Score", gridcolor="rgba(99,102,241,0.08)", range=[0, 100]),
            yaxis=dict(title=""),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # --- Comparative radar ---
    st.markdown('<div class="section-header">📈 Score Comparison — Batters vs Bowlers</div>', unsafe_allow_html=True)

    fig_comp = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]],
                             subplot_titles=["Batters — Format Split", "Bowlers — Format Split"])

    bat_format_counts = bat["formats"].value_counts()
    bowl_format_counts = bowl["formats"].value_counts()

    fig_comp.add_trace(go.Pie(
        labels=bat_format_counts.index, values=bat_format_counts.values,
        marker=dict(colors=["#6366f1", "#f4b942", "#a855f7"]),
        textinfo="label+percent", hole=0.45,
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
    ), row=1, col=1)

    fig_comp.add_trace(go.Pie(
        labels=bowl_format_counts.index, values=bowl_format_counts.values,
        marker=dict(colors=["#14b8a6", "#f4b942", "#06b6d4"]),
        textinfo="label+percent", hole=0.45,
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
    ), row=1, col=2)

    fig_comp.update_layout(**PLOTLY_LAYOUT, height=350, showlegend=False)
    st.plotly_chart(fig_comp, use_container_width=True)

    st.info("💡 Scores are relative percentile-based model scores (0 – 100), not probabilities or predicted match outcomes.")


# ===================================================================
# PAGE — Batting Leaderboard
# ===================================================================
elif page == "🏏 Batting":
    st.markdown('<div class="section-header">🏏 Batting Leaderboard — Top 10 Under Pressure</div>', unsafe_allow_html=True)

    formats = sorted(set(",".join(bat["formats"].fillna("")).replace(" ", "").split(",")) - {""})
    selected = st.multiselect("Filter by format", formats, default=formats)
    view = bat[bat["formats"].apply(lambda x: any(f in str(x).replace(" ", "").split(",") for f in selected))]

    # Metric cards for top 3
    if len(view) >= 3:
        t1, t2, t3 = st.columns(3)
        medals = ["🥇", "🥈", "🥉"]
        medal_colors = ["#f4b942", "#c0c0c0", "#cd7f32"]
        for col, i, medal, mc in zip([t1, t2, t3], range(3), medals, medal_colors):
            row = view.iloc[i]
            col.markdown(f"""
            <div class="kpi-card" style="border-color: {mc}40;">
                <div style="font-size:2rem;">{medal}</div>
                <div style="font-size:1.1rem; font-weight:700; color:#f8fafc; margin:4px 0;">{row[bat_name]}</div>
                <div class="kpi-value">{row['final_score']}</div>
                <div class="kpi-label">{row['formats']} · {int(row['pressure_runs'])} P. Runs</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Table
    display = view[["Rank", bat_name, "final_score", "pressure_balls", "pressure_runs", "formats"]].copy()
    display.columns = ["#", "Player", "Score", "Pressure Balls", "Pressure Runs", "Format"]
    st.dataframe(display, hide_index=True, use_container_width=True)

    # Scatter: balls vs score, size = runs
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(
            view, x="pressure_balls", y="final_score",
            size="pressure_runs", color="formats",
            hover_name=bat_name,
            color_discrete_sequence=["#6366f1", "#f4b942", "#a855f7"],
            labels={"pressure_balls": "Pressure Balls Faced", "final_score": "Model Score", "formats": "Format"},
            size_max=35,
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=430,
                          title=dict(text="Volume vs Score (Bubble = Runs)", font=dict(size=14, color="#94a3b8")),
                          xaxis=dict(gridcolor="rgba(99,102,241,0.08)"),
                          yaxis=dict(gridcolor="rgba(99,102,241,0.08)"))
        fig.update_traces(marker=dict(line=dict(width=1, color="#1e293b")))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Radar chart for top 5
        top5 = view.head(5)
        categories = ["Score", "P. Balls", "P. Runs"]
        fig_radar = go.Figure()
        radar_colors = ["#6366f1", "#f4b942", "#a855f7", "#ec4899", "#14b8a6"]
        for idx, (_, row) in enumerate(top5.iterrows()):
            vals = [
                row["final_score"],
                min(row["pressure_balls"] / 7, 100),  # normalize to ~100
                min(row["pressure_runs"] / 12, 100),
            ]
            vals.append(vals[0])  # close the shape
            fig_radar.add_trace(go.Scatterpolar(
                r=vals, theta=categories + [categories[0]],
                fill="toself", fillcolor=f"rgba({int(radar_colors[idx][1:3],16)},{int(radar_colors[idx][3:5],16)},{int(radar_colors[idx][5:7],16)},0.1)",
                line=dict(color=radar_colors[idx], width=2),
                name=row[bat_name],
                hovertemplate=f"<b>{row[bat_name]}</b><br>%{{theta}}: %{{r:.1f}}<extra></extra>",
            ))
        fig_radar.update_layout(
            **PLOTLY_LAYOUT, height=430,
            title=dict(text="Top 5 — Multi-Metric Radar", font=dict(size=14, color="#94a3b8")),
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(99,102,241,0.15)", tickfont=dict(color="#64748b")),
                angularaxis=dict(gridcolor="rgba(99,102,241,0.15)", tickfont=dict(color="#94a3b8")),
            ),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=11)),
        )
        st.plotly_chart(fig_radar, use_container_width=True)


# ===================================================================
# PAGE — Bowling Leaderboard
# ===================================================================
elif page == "🎯 Bowling":
    st.markdown('<div class="section-header">🎯 Bowling Leaderboard — Top 10 Under Pressure</div>', unsafe_allow_html=True)

    formats = sorted(set(",".join(bowl["formats"].fillna("")).replace(" ", "").split(",")) - {""})
    selected = st.multiselect("Filter by format", formats, default=formats)
    view = bowl[bowl["formats"].apply(lambda x: any(f in str(x).replace(" ", "").split(",") for f in selected))]

    # Top 3 podium
    if len(view) >= 3:
        t1, t2, t3 = st.columns(3)
        medals = ["🥇", "🥈", "🥉"]
        medal_colors = ["#f4b942", "#c0c0c0", "#cd7f32"]
        for col, i, medal, mc in zip([t1, t2, t3], range(3), medals, medal_colors):
            row = view.iloc[i]
            col.markdown(f"""
            <div class="kpi-card" style="border-color: {mc}40;">
                <div style="font-size:2rem;">{medal}</div>
                <div style="font-size:1.1rem; font-weight:700; color:#f8fafc; margin:4px 0;">{row[bowl_name]}</div>
                <div class="kpi-value">{row['final_score']}</div>
                <div class="kpi-label">{row['formats']} · {int(row['pressure_wickets'])} P. Wkts</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")

    display = view[["Rank", bowl_name, "final_score", "pressure_balls", "pressure_wickets", "formats"]].copy()
    display.columns = ["#", "Player", "Score", "Pressure Balls", "Pressure Wkts", "Format"]
    st.dataframe(display, hide_index=True, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(
            view, x="pressure_balls", y="final_score",
            size="pressure_wickets", color="formats",
            hover_name=bowl_name,
            color_discrete_sequence=["#14b8a6", "#f4b942", "#06b6d4"],
            labels={"pressure_balls": "Pressure Legal Balls", "final_score": "Model Score", "formats": "Format"},
            size_max=35,
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=430,
                          title=dict(text="Volume vs Score (Bubble = Wickets)", font=dict(size=14, color="#94a3b8")),
                          xaxis=dict(gridcolor="rgba(99,102,241,0.08)"),
                          yaxis=dict(gridcolor="rgba(99,102,241,0.08)"))
        fig.update_traces(marker=dict(line=dict(width=1, color="#1e293b")))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Lollipop chart: wickets per pressure ball (efficiency)
        view_eff = view.copy()
        view_eff["efficiency"] = (view_eff["pressure_wickets"] / view_eff["pressure_balls"] * 100).round(2)
        view_eff = view_eff.sort_values("efficiency", ascending=True)

        fig_lollipop = go.Figure()
        for _, row in view_eff.iterrows():
            fig_lollipop.add_trace(go.Scatter(
                x=[0, row["efficiency"]], y=[row[bowl_name], row[bowl_name]],
                mode="lines", line=dict(color="#14b8a6", width=2),
                showlegend=False, hoverinfo="skip",
            ))
        fig_lollipop.add_trace(go.Scatter(
            x=view_eff["efficiency"], y=view_eff[bowl_name],
            mode="markers+text",
            marker=dict(size=12, color=GOLD, line=dict(width=1, color="#1e293b")),
            text=view_eff["efficiency"].apply(lambda v: f"{v:.1f}%"),
            textposition="middle right", textfont=dict(color="#e2e8f0", size=11),
            showlegend=False,
            hovertemplate="<b>%{y}</b><br>Wicket Rate: %{x:.2f}%<extra></extra>",
        ))
        fig_lollipop.update_layout(
            **PLOTLY_LAYOUT, height=430,
            title=dict(text="Wicket Efficiency (Wkts / 100 Pressure Balls)", font=dict(size=14, color="#94a3b8")),
            xaxis=dict(title="Wickets per 100 Balls", gridcolor="rgba(99,102,241,0.08)"),
            yaxis=dict(title=""),
        )
        st.plotly_chart(fig_lollipop, use_container_width=True)


# ===================================================================
# PAGE — Sensitivity Analysis
# ===================================================================
elif page == "📊 Sensitivity":
    st.markdown('<div class="section-header">📊 Sensitivity Analysis — Threshold Comparison</div>', unsafe_allow_html=True)

    st.markdown("""
    > The **25 % threshold** is the primary model. Changing the cutoff to 20 % (stricter) or 30 % (broader)
    > produces materially different shortlists, confirming that the threshold choice is consequential.
    """)

    # Load all threshold datasets
    thresholds = ["20", "25", "30"]
    bat_data = {t: load_csv(f"batters_{t}pct.csv") for t in thresholds}
    bowl_data = {t: load_csv(f"bowlers_{t}pct.csv") for t in thresholds}

    # Round scores
    for t in thresholds:
        bat_data[t]["score"] = pd.to_numeric(bat_data[t]["score"], errors="coerce").round(2)
        bowl_data[t]["score"] = pd.to_numeric(bowl_data[t]["score"], errors="coerce").round(2)

    tab1, tab2 = st.tabs(["🏏 Batters Comparison", "🎯 Bowlers Comparison"])

    with tab1:
        # Grouped bar: scores across thresholds
        all_bat_players = set()
        for t in thresholds:
            all_bat_players.update(bat_data[t]["player"].tolist())

        fig_bat = go.Figure()
        bar_colors = {"20": "#a855f7", "25": "#f4b942", "30": "#6366f1"}
        for t in thresholds:
            df = bat_data[t].sort_values("Rank")
            fig_bat.add_trace(go.Bar(
                x=df["player"], y=df["score"],
                name=f"{t}% Threshold",
                marker_color=bar_colors[t],
                text=df["score"].round(1), textposition="outside",
                textfont=dict(size=10, color="#e2e8f0"),
                hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}<br>Threshold: " + t + "%<extra></extra>",
            ))
        fig_bat.update_layout(
            **PLOTLY_LAYOUT, height=480, barmode="group",
            title=dict(text="Batter Scores Across Thresholds", font=dict(size=15, color="#94a3b8")),
            xaxis=dict(tickangle=-35, gridcolor="rgba(99,102,241,0.05)"),
            yaxis=dict(title="Model Score", gridcolor="rgba(99,102,241,0.08)", range=[0, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_bat, use_container_width=True)

        # Side-by-side tables
        cols = st.columns(3)
        for col, t in zip(cols, thresholds):
            with col:
                label = "🏆 Primary" if t == "25" else ("🔒 Stricter" if t == "20" else "📂 Broader")
                st.markdown(f"**{label} · {t}% Cutoff**")
                df = bat_data[t][["Rank", "player", "score", "formats"]].copy()
                df.columns = ["#", "Player", "Score", "Format"]
                st.dataframe(df, hide_index=True, use_container_width=True)

    with tab2:
        fig_bowl = go.Figure()
        for t in thresholds:
            df = bowl_data[t].sort_values("Rank")
            fig_bowl.add_trace(go.Bar(
                x=df["player"], y=df["score"],
                name=f"{t}% Threshold",
                marker_color=bar_colors[t],
                text=df["score"].round(1), textposition="outside",
                textfont=dict(size=10, color="#e2e8f0"),
                hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}<br>Threshold: " + t + "%<extra></extra>",
            ))
        fig_bowl.update_layout(
            **PLOTLY_LAYOUT, height=480, barmode="group",
            title=dict(text="Bowler Scores Across Thresholds", font=dict(size=15, color="#94a3b8")),
            xaxis=dict(tickangle=-35, gridcolor="rgba(99,102,241,0.05)"),
            yaxis=dict(title="Model Score", gridcolor="rgba(99,102,241,0.08)", range=[0, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_bowl, use_container_width=True)

        cols = st.columns(3)
        for col, t in zip(cols, thresholds):
            with col:
                label = "🏆 Primary" if t == "25" else ("🔒 Stricter" if t == "20" else "📂 Broader")
                st.markdown(f"**{label} · {t}% Cutoff**")
                df = bowl_data[t][["Rank", "player", "score", "formats"]].copy()
                df.columns = ["#", "Player", "Score", "Format"]
                st.dataframe(df, hide_index=True, use_container_width=True)

    # Stability heatmap: which players appear across all 3 thresholds?
    st.markdown('<div class="section-header">🔄 Player Stability Across Thresholds</div>', unsafe_allow_html=True)

    stab_left, stab_right = st.columns(2)
    with stab_left:
        all_bat = sorted(set().union(*[set(bat_data[t]["player"]) for t in thresholds]))
        heatmap_bat = []
        for p in all_bat:
            row = []
            for t in thresholds:
                df = bat_data[t]
                match = df[df["player"] == p]
                row.append(match["Rank"].values[0] if len(match) else 0)
            heatmap_bat.append(row)

        fig_hm = go.Figure(go.Heatmap(
            z=heatmap_bat, x=[f"{t}%" for t in thresholds], y=all_bat,
            colorscale=[[0, "#1e1b4b"], [0.1, "#312e81"], [0.5, "#6366f1"], [1.0, "#f4b942"]],
            text=[[v if v > 0 else "—" for v in row] for row in heatmap_bat],
            texttemplate="%{text}",
            hovertemplate="<b>%{y}</b><br>Threshold: %{x}<br>Rank: %{z}<extra></extra>",
            showscale=False,
        ))
        fig_hm.update_layout(**PLOTLY_LAYOUT, height=450,
                             title=dict(text="Batter Rank Stability", font=dict(size=14, color="#94a3b8")),
                             yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_hm, use_container_width=True)

    with stab_right:
        all_bowl = sorted(set().union(*[set(bowl_data[t]["player"]) for t in thresholds]))
        heatmap_bowl = []
        for p in all_bowl:
            row = []
            for t in thresholds:
                df = bowl_data[t]
                match = df[df["player"] == p]
                row.append(match["Rank"].values[0] if len(match) else 0)
            heatmap_bowl.append(row)

        fig_hm2 = go.Figure(go.Heatmap(
            z=heatmap_bowl, x=[f"{t}%" for t in thresholds], y=all_bowl,
            colorscale=[[0, "#042f2e"], [0.1, "#134e4a"], [0.5, "#14b8a6"], [1.0, "#f4b942"]],
            text=[[v if v > 0 else "—" for v in row] for row in heatmap_bowl],
            texttemplate="%{text}",
            hovertemplate="<b>%{y}</b><br>Threshold: %{x}<br>Rank: %{z}<extra></extra>",
            showscale=False,
        ))
        fig_hm2.update_layout(**PLOTLY_LAYOUT, height=450,
                              title=dict(text="Bowler Rank Stability", font=dict(size=14, color="#94a3b8")),
                              yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_hm2, use_container_width=True)


# ===================================================================
# PAGE — Methodology
# ===================================================================
elif page == "🔬 Methodology":
    st.markdown('<div class="section-header">🔬 Methodology & Model Architecture</div>', unsafe_allow_html=True)

    # Methodology cards instead of a raw table
    for _, row in method.iterrows():
        st.markdown(f"""
        <div class="methodology-card">
            <div class="method-title">📌 {row['Parameter']}</div>
            <div class="method-text">{row['Details']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Scoring weights as donut charts
    st.markdown('<div class="section-header">⚖️ Scoring Weight Distribution</div>', unsafe_allow_html=True)

    w1, w2 = st.columns(2)
    with w1:
        bat_weights = {"Strike Rate": 30, "Improvement": 20, "Inv. Dismissal Rate": 20, "Runs": 15, "Consistency": 15}
        fig_w = go.Figure(go.Pie(
            labels=list(bat_weights.keys()), values=list(bat_weights.values()),
            hole=0.55,
            marker=dict(colors=["#6366f1", "#a855f7", "#f4b942", "#ec4899", "#14b8a6"],
                        line=dict(color="#0f172a", width=2)),
            textinfo="label+percent",
            textfont=dict(size=12, color="#e2e8f0"),
            hovertemplate="<b>%{label}</b><br>Weight: %{value}%<extra></extra>",
        ))
        fig_w.update_layout(**PLOTLY_LAYOUT, height=380,
                            title=dict(text="🏏 Batter Scoring Weights", font=dict(size=15, color="#f4b942")),
                            annotations=[dict(text="Batting", x=0.5, y=0.5, font_size=16, font_color="#94a3b8", showarrow=False)])
        st.plotly_chart(fig_w, use_container_width=True)

    with w2:
        bowl_weights = {"Wicket Rate": 35, "Improvement": 20, "Consistency": 20, "Wickets": 15, "Sample Size": 10}
        fig_w2 = go.Figure(go.Pie(
            labels=list(bowl_weights.keys()), values=list(bowl_weights.values()),
            hole=0.55,
            marker=dict(colors=["#14b8a6", "#06b6d4", "#f4b942", "#a855f7", "#6366f1"],
                        line=dict(color="#0f172a", width=2)),
            textinfo="label+percent",
            textfont=dict(size=12, color="#e2e8f0"),
            hovertemplate="<b>%{label}</b><br>Weight: %{value}%<extra></extra>",
        ))
        fig_w2.update_layout(**PLOTLY_LAYOUT, height=380,
                             title=dict(text="🎯 Bowler Scoring Weights", font=dict(size=15, color="#f4b942")),
                             annotations=[dict(text="Bowling", x=0.5, y=0.5, font_size=16, font_color="#94a3b8", showarrow=False)])
        st.plotly_chart(fig_w2, use_container_width=True)

    # Pressure index explanation
    st.markdown('<div class="section-header">📐 Pressure Index Formula</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="methodology-card">
        <div class="method-text" style="font-size: 1rem;">
            <strong style="color: #f4b942;">Pressure Index</strong> = Average of two percentile measures:<br><br>
            <code style="background:#1e293b; padding:2px 8px; border-radius:4px; color:#a5b4fc;">
            Pressure Index = (Stage Percentile + Wickets-Lost Percentile) / 2
            </code><br><br>
            • <strong>Stage Percentile</strong> — percentile rank of legal balls elapsed before the delivery, within format and innings.<br>
            • <strong>Wickets-Lost Percentile</strong> — percentile rank of wickets lost before the delivery, within format and innings.<br>
            • <strong>High Pressure</strong> — deliveries in the top 25 % of the pressure-index distribution for each format/innings group.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Important limitations
    st.markdown('<div class="section-header">⚠️ Important Limitations</div>', unsafe_allow_html=True)
    st.warning("""
    - This is an **innings-context proxy**, not a direct measure of match leverage, target difficulty, or win probability.
    - Bowling economy and dot-ball percentage were **excluded** because source run fields did not support reliable reconstruction.
    - The 25 % cutoff and scoring weights are **analytical choices**; sensitivity analysis shows rankings change at 20 % and 30 %.
    - Percentile scores are **relative within format**. Cross-format scores are combined using pressure exposure weights.
    """)

    # Download buttons
    st.markdown("")
    d1, d2, d3 = st.columns([1, 1, 1])
    with d1:
        st.download_button("⬇️ Download Batter Rankings", bat.to_csv(index=False).encode("utf-8"),
                           "SuperRR_Top10_Batters.csv", "text/csv", use_container_width=True)
    with d2:
        st.download_button("⬇️ Download Bowler Rankings", bowl.to_csv(index=False).encode("utf-8"),
                           "SuperRR_Top10_Bowlers.csv", "text/csv", use_container_width=True)
    with d3:
        st.download_button("⬇️ Download Methodology", method.to_csv(index=False).encode("utf-8"),
                           "SuperRR_Methodology.csv", "text/csv", use_container_width=True)


# ───────────────────────────────────────────────────────────────
# Footer
# ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-text">
    SuperRR Selector Season 2 · Pressure-based player evaluation · Analysis based on the supplied summary workbook<br>
    Interpret rankings under the documented assumptions and limitations · Built with ❤️ using Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
