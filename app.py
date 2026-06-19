import pandas as pd
import plotly.graph_objects as go
import streamlit as st

APP_BG, CARD, BORDER = "#EEF1F5", "#FFFFFF", "#E6EBF1"
NAVY, INK, ACCENT    = "#22344A", "#1F2D3D", "#E8853A"
MUTED, FRAUD, LEGIT  = "#7C8A99", "#D64545", "#1F9D63"
GRID = "#E6EBF1"
RULE_PRECISION = 17.0

st.set_page_config(page_title="Fraud Risk Intelligence", layout="wide")

st.markdown(f"""
<style>
.stApp {{ background:{APP_BG}; }}
#MainMenu, footer, header {{ visibility:hidden; }}
.block-container {{ padding-top:2.4rem; padding-bottom:3rem; max-width:1380px; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ background:{CARD};
   border:1px solid {BORDER} !important; border-radius:14px;
   box-shadow:0 1px 3px rgba(31,45,61,0.05); }}
h1,h2,h3,h4,h5 {{ color:{INK}; font-weight:700; }}
.app-head {{ display:flex; align-items:center; gap:13px; }}
.app-logo {{ width:38px; height:38px; border-radius:9px; background:{ACCENT};
   display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:18px; }}
.app-title {{ font-size:1.65rem; font-weight:700; color:{INK}; line-height:1; }}
.app-sub {{ color:{MUTED}; font-size:0.92rem; margin-top:7px; }}
.badge {{ display:inline-block; padding:2px 10px; border-radius:999px; background:#FBEEE2;
   border:1px solid #F2CBA6; color:#B45F1E; font-size:0.72rem; letter-spacing:0.04em; text-transform:uppercase; }}
.kpi {{ background:{CARD}; border:1px solid {BORDER}; border-radius:14px; padding:17px 19px 19px;
   box-shadow:0 1px 3px rgba(31,45,61,0.06); position:relative; overflow:hidden; }}
.kpi::before {{ content:""; position:absolute; top:0; left:0; right:0; height:3px; background:{ACCENT}; }}
.kpi-label {{ color:{MUTED}; font-size:0.73rem; letter-spacing:0.06em; text-transform:uppercase; }}
.kpi-value {{ color:{INK}; font-size:2.1rem; font-weight:700; margin-top:7px; line-height:1; }}
.kpi-sub {{ color:{MUTED}; font-size:0.83rem; margin-top:9px; }}
.up {{ color:{LEGIT}; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_alerts():
    df = pd.read_parquet("data/processed/alerts.parquet")
    df["trans_time"] = pd.to_datetime(df["trans_time"])
    return df

alerts = load_alerts()
total_fraud      = int(alerts["is_fraud"].sum())
total_fraud_loss = alerts.loc[alerts["is_fraud"] == 1, "amt"].sum()

st.markdown(f"""
<div class="app-head"><div class="app-logo">◆</div>
  <div class="app-title">Fraud Risk Intelligence Platform</div></div>
<div class="app-sub">XGBoost on SQL-engineered features &nbsp;·&nbsp;
  <span class="badge">Backtest · Apr–Jun 2020</span></div>
""", unsafe_allow_html=True)
st.write("")

cc1, cc2 = st.columns([1.1, 2.4], gap="large")
rank_by = cc1.radio("Rank queue by", ["Fraud probability", "Expected loss"], horizontal=True)
key = "p_fraud" if rank_by == "Fraud probability" else "expected_loss"
ranked = alerts.sort_values(key, ascending=False).reset_index(drop=True)
budget = cc2.slider("Analyst review budget", 50, len(ranked), min(1000, len(ranked)), step=50)

reviewed       = ranked.head(budget)
caught         = int(reviewed["is_fraud"].sum())
loss_recovered = reviewed.loc[reviewed["is_fraud"] == 1, "amt"].sum()
precision      = 100 * caught / max(len(reviewed), 1)
recall         = 100 * caught / max(total_fraud, 1)

def kpi(label, value, sub):
    return (f'<div class="kpi"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>')

st.write("")
c1, c2, c3, c4 = st.columns(4, gap="medium")
c1.markdown(kpi("Alerts reviewed", f"{budget:,}", f"of {len(ranked):,} flagged"), unsafe_allow_html=True)
c2.markdown(kpi("Fraud caught", f"{caught:,}", f'<span class="up">↑ {recall:.0f}%</span> of all fraud'), unsafe_allow_html=True)
c3.markdown(kpi("Precision", f"{precision:.0f}%", f'<span class="up">↑</span> vs {RULE_PRECISION:.0f}% rule baseline'), unsafe_allow_html=True)
c4.markdown(kpi("Fraud $ recovered", f"${loss_recovered:,.0f}", f'<span class="up">↑ {100*loss_recovered/total_fraud_loss:.0f}%</span> of fraud losses'), unsafe_allow_html=True)
st.write("")

cum_loss_pct   = 100 * (ranked["is_fraud"] * ranked["amt"]).cumsum() / total_fraud_loss
cum_recall_pct = 100 *  ranked["is_fraud"].cumsum() / total_fraud
x = list(range(1, len(ranked) + 1))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=cum_loss_pct, name="Fraud $ recovered",
                         line=dict(color=ACCENT, width=2.6),
                         fill="tozeroy", fillcolor="rgba(232,133,58,0.10)"))
fig.add_trace(go.Scatter(x=x, y=cum_recall_pct, name="Fraud caught (recall)",
                         line=dict(color=NAVY, width=1.8, dash="dot")))
fig.add_vline(x=budget, line=dict(color=ACCENT, width=1, dash="dash"))
fig.update_layout(height=340, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                  font=dict(color=INK, size=12),
                  legend=dict(orientation="h", y=1.13, x=0, bgcolor="rgba(0,0,0,0)"),
                  xaxis=dict(title="Alerts reviewed", gridcolor=GRID, zeroline=False),
                  yaxis=dict(title="% of total", gridcolor=GRID, range=[0, 101], zeroline=False),
                  margin=dict(l=10, r=10, t=30, b=10))

with st.container(border=True):
    st.markdown("##### Alert-budget curve")
    st.plotly_chart(fig, use_container_width=True)

view = reviewed.copy()
view["Card"] = "•••• " + view["cc_num"].astype("int64").astype(str).str[-4:]
table = view.rename(columns={"trans_time": "Time", "category": "Category",
                             "amt": "Amount", "p_fraud": "Fraud prob",
                             "expected_loss": "Expected loss"})
table["Fraud prob"] = (100 * table["Fraud prob"]).round(1)
table["Outcome"] = view["is_fraud"].map({1: "Fraud", 0: "Legit"})
table = table[["Time", "Card", "Category", "Amount", "Fraud prob", "Expected loss", "Outcome"]]

with st.container(border=True):
    st.markdown("##### Alert queue")
    st.dataframe(
        table.head(200), hide_index=True, use_container_width=True, height=430,
        column_config={
            "Amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
            "Fraud prob": st.column_config.ProgressColumn("Fraud prob", format="%.0f%%",
                                                          min_value=0, max_value=100),
            "Expected loss": st.column_config.NumberColumn("Expected loss", format="$%.0f"),
        },
    )