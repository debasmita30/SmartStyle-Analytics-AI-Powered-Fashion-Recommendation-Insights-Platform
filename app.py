"""
SmartStyle Analytics — AI-Powered Fashion Intelligence Platform
================================================================
A production-grade fashion analytics dashboard built on a 14k-product
Myntra-style catalog. Designed as a portfolio-grade data-analytics
deliverable: rigorous EDA, a documented confidence-scoring model, an
honest data-quality audit, and a recommendation engine.

Author: Debasmita Chatterjee
Run:    streamlit run app.py
"""

import os
import textwrap
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartStyle Analytics",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Point this at your GitHub raw URL after you upload fashion_clean.csv.
# The app falls back to a local file of the same name if the URL fails.
DATA_URL = "https://raw.githubusercontent.com/debasmita30/SmartStyle-Analytics-AI-Powered-Fashion-Recommendation-Insights-Platform/main/fashion_clean.csv"
LOCAL_FALLBACK = "fashion_clean.csv"

# ──────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM  —  editorial fashion-tech
#   ink/plum canvas · couture magenta accent · serif display + grotesque body
# ──────────────────────────────────────────────────────────────────────────
INK      = "#120a1f"   # canvas
INK_2    = "#1b1030"   # raised surface
PLUM     = "#2a1747"   # card
ACCENT   = "#e0479e"   # couture magenta
ACCENT_2 = "#a855f7"   # violet
ELECTRIC = "#5de4ff"   # gen-z electric cyan pop
GOLD     = "#f2c879"   # data highlight
MINT     = "#5ad1a8"   # positive
INK_TX   = "#f4ecff"   # primary text
MUTE_TX  = "#a594c4"   # muted text
LINE     = "rgba(224,71,158,0.18)"

PLOTLY_FONT = "Space Grotesk, Inter, sans-serif"


def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,500&family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {{
        --ink:{INK}; --ink2:{INK_2}; --plum:{PLUM}; --accent:{ACCENT};
        --accent2:{ACCENT_2}; --electric:{ELECTRIC}; --gold:{GOLD}; --mint:{MINT};
        --tx:{INK_TX}; --mute:{MUTE_TX}; --line:{LINE};
    }}

    .stApp {{ background:{INK}; color:var(--tx); font-family:'Space Grotesk',sans-serif; }}
    .main .block-container {{ padding-top: 1.4rem; max-width: 1280px; }}

    h1,h2,h3,h4 {{ font-family:'Fraunces', Georgia, serif !important; letter-spacing:-.01em; color:var(--tx); }}
    p, span, div, label, li {{ color: var(--tx); }}

    /* ── ANIMATED AURORA BACKGROUND ─────────────────────────── */
    .aurora {{ position:fixed; inset:0; z-index:-2; overflow:hidden; pointer-events:none; }}
    .blob {{ position:absolute; border-radius:50%; filter:blur(70px); opacity:.55;
        mix-blend-mode:screen; }}
    .blob.b1 {{ width:46vw; height:46vw; left:-8vw; top:-10vw;
        background: radial-gradient(circle, {ACCENT}, transparent 65%); animation: drift1 22s ease-in-out infinite; }}
    .blob.b2 {{ width:40vw; height:40vw; right:-6vw; top:-4vw;
        background: radial-gradient(circle, {ACCENT_2}, transparent 65%); animation: drift2 26s ease-in-out infinite; }}
    .blob.b3 {{ width:48vw; height:48vw; left:28vw; bottom:-22vw;
        background: radial-gradient(circle, {ELECTRIC}, transparent 68%); opacity:.32; animation: drift3 30s ease-in-out infinite; }}
    @keyframes drift1 {{ 0%,100%{{transform:translate(0,0) scale(1)}} 50%{{transform:translate(8vw,6vh) scale(1.12)}} }}
    @keyframes drift2 {{ 0%,100%{{transform:translate(0,0) scale(1.05)}} 50%{{transform:translate(-7vw,5vh) scale(.92)}} }}
    @keyframes drift3 {{ 0%,100%{{transform:translate(0,0) scale(1)}} 50%{{transform:translate(-6vw,-7vh) scale(1.15)}} }}
    .grain {{ position:fixed; inset:0; z-index:-1; pointer-events:none; opacity:.05;
        background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }}

    /* ── page-load stagger ───────────────────────────────────── */
    @keyframes rise {{ from {{opacity:0; transform:translateY(16px);}} to {{opacity:1; transform:none;}} }}
    .rise {{ animation: rise .7s cubic-bezier(.22,1,.36,1) both; }}
    .d1{{animation-delay:.05s}} .d2{{animation-delay:.13s}} .d3{{animation-delay:.21s}}
    .d4{{animation-delay:.29s}} .d5{{animation-delay:.37s}} .d6{{animation-delay:.45s}}
    @media (prefers-reduced-motion: reduce) {{
        .rise,.blob,.shine,.ticker-track,.chip.high{{animation:none !important}}
    }}

    /* ── masthead ────────────────────────────────────────────── */
    .masthead {{
        border:1px solid var(--line); border-radius:22px; padding:34px 36px;
        background: linear-gradient(135deg, rgba(42,23,71,.82), rgba(27,16,48,.55));
        backdrop-filter: blur(16px); position:relative; overflow:hidden;
    }}
    .masthead:before {{ content:""; position:absolute; inset:0;
        background: radial-gradient(440px 220px at 88% 8%, rgba(93,228,255,.22), transparent 60%);
        pointer-events:none; }}
    .eyebrow {{ font-family:'JetBrains Mono', monospace; font-size:.7rem; letter-spacing:.3em;
        text-transform:uppercase; margin-bottom:.6rem;
        background:linear-gradient(90deg,var(--accent),var(--electric),var(--accent));
        background-size:200% auto; -webkit-background-clip:text; background-clip:text;
        -webkit-text-fill-color:transparent; animation: shine 4s linear infinite; }}
    @keyframes shine {{ to {{ background-position:200% center; }} }}
    .masthead h1 {{ font-size:3.4rem; line-height:1.0; margin:.1rem 0 .5rem; font-weight:700; }}
    .masthead h1 .grad {{
        background:linear-gradient(100deg,#fff 10%,var(--electric) 35%,var(--accent) 60%,var(--gold) 85%);
        background-size:220% auto; -webkit-background-clip:text; background-clip:text;
        -webkit-text-fill-color:transparent; animation: shine 6s linear infinite; }}
    .masthead .sub {{ color:var(--mute); max-width:680px; font-size:1.04rem; }}

    /* ── ticker tape ─────────────────────────────────────────── */
    .ticker {{ overflow:hidden; border:1px solid var(--line); border-radius:999px;
        background:rgba(27,16,48,.5); backdrop-filter:blur(8px); padding:9px 0; margin:14px 0 2px; }}
    .ticker-track {{ display:inline-block; white-space:nowrap; animation: scroll 26s linear infinite;
        font-family:'JetBrains Mono',monospace; font-size:.78rem; letter-spacing:.06em; }}
    .ticker:hover .ticker-track {{ animation-play-state:paused; }}
    .ticker-track span {{ color:var(--mute); padding:0 6px; }}
    .ticker-track b {{ color:var(--electric); }}
    .ticker-track .dot {{ color:var(--accent); padding:0 16px; }}
    @keyframes scroll {{ from{{transform:translateX(0)}} to{{transform:translateX(-50%)}} }}

    /* ── generic panel ───────────────────────────────────────── */
    .panel {{ border:1px solid var(--line); border-radius:16px; padding:22px 24px;
        background: linear-gradient(180deg, rgba(27,16,48,.6), rgba(18,10,31,.4)); }}
    .panel h3 {{ margin-top:0; }}
    .tag {{ display:inline-block; font-family:'JetBrains Mono',monospace; font-size:.66rem;
        padding:3px 9px; border-radius:999px; margin:2px 4px 2px 0; border:1px solid var(--line);
        color:var(--mute); }}

    /* ── product card ────────────────────────────────────────── */
    .pcard {{ border:1px solid var(--line); border-radius:16px; overflow:hidden; position:relative;
        background: linear-gradient(180deg, rgba(42,23,71,.5), rgba(18,10,31,.35));
        transition: transform .4s cubic-bezier(.22,1,.36,1), box-shadow .4s, border-color .4s; }}
    .pcard:before {{ content:""; position:absolute; inset:0; border-radius:16px; padding:1px;
        background:linear-gradient(135deg,transparent,var(--accent),var(--electric),transparent);
        -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
        -webkit-mask-composite:xor; mask-composite:exclude; opacity:0; transition:opacity .4s; }}
    .pcard:hover {{ transform: translateY(-8px) scale(1.012);
        box-shadow:0 26px 52px -24px rgba(224,71,158,.7); }}
    .pcard:hover:before {{ opacity:1; }}
    .pname {{ font-family:'Fraunces',serif; font-size:1.02rem; line-height:1.25; min-height:2.5em; }}
    .pbrand {{ font-family:'JetBrains Mono',monospace; font-size:.66rem; letter-spacing:.14em;
        text-transform:uppercase; color:var(--accent); }}
    .price {{ font-family:'Fraunces',serif; font-size:1.4rem; color:var(--gold); }}

    /* confidence chip */
    .chip {{ display:inline-flex; align-items:center; gap:6px; font-family:'JetBrains Mono',monospace;
        font-size:.72rem; padding:4px 10px; border-radius:999px; font-weight:600; }}
    .chip.high {{ background:rgba(90,209,168,.14); color:var(--mint); border:1px solid rgba(90,209,168,.4);
        animation: glowpulse 2.4s ease-in-out infinite; }}
    @keyframes glowpulse {{ 0%,100%{{box-shadow:0 0 0 0 rgba(90,209,168,0)}} 50%{{box-shadow:0 0 14px 0 rgba(90,209,168,.45)}} }}
    .chip.med  {{ background:rgba(242,200,121,.13); color:var(--gold); border:1px solid rgba(242,200,121,.4); }}
    .chip.low  {{ background:rgba(224,71,158,.14); color:var(--accent); border:1px solid rgba(224,71,158,.45); }}
    .chip.unr  {{ background:rgba(165,148,196,.12); color:var(--mute); border:1px solid rgba(165,148,196,.3); }}

    section[data-testid="stSidebar"] {{ background: linear-gradient(180deg, {INK_2}, {INK}); border-right:1px solid var(--line); }}
    section[data-testid="stSidebar"] * {{ color: var(--tx); }}

    .stTabs [data-baseweb="tab-list"] {{ gap:4px; border-bottom:1px solid var(--line); }}
    .stTabs [data-baseweb="tab"] {{ font-family:'JetBrains Mono',monospace; font-size:.78rem;
        letter-spacing:.08em; text-transform:uppercase; color:var(--mute); padding:10px 16px;
        transition:color .3s; }}
    .stTabs [data-baseweb="tab"]:hover {{ color:var(--electric); }}
    .stTabs [aria-selected="true"] {{ color:var(--tx) !important; border-bottom:2px solid var(--accent) !important; }}

    .stProgress > div > div > div > div {{ background: linear-gradient(90deg, var(--accent), var(--electric)); }}
    [data-testid="stMetricValue"] {{ font-family:'Fraunces',serif; }}
    .footer {{ text-align:center; color:var(--mute); font-family:'JetBrains Mono',monospace;
        font-size:.72rem; letter-spacing:.1em; padding:30px 0 10px; }}
    hr {{ border-color: var(--line); }}
    </style>
    <div class='aurora'><div class='blob b1'></div><div class='blob b2'></div><div class='blob b3'></div></div>
    <div class='grain'></div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading catalog…")
def load_data():
    src, used = None, None
    try:
        src = pd.read_csv(DATA_URL)
        used = "remote"
    except Exception:
        if os.path.exists(LOCAL_FALLBACK):
            src = pd.read_csv(LOCAL_FALLBACK)
            used = "local"
        else:
            raise FileNotFoundError(
                "Could not load data. Set DATA_URL to your GitHub raw link "
                "or place fashion_clean.csv next to app.py."
            )
    # guard types
    for c in ["price", "avg_rating", "ratingCount", "bayesian_rating",
              "confidence_score", "desc_length"]:
        if c in src:
            src[c] = pd.to_numeric(src[c], errors="coerce")
    return src, used


def conf_class(t):
    return {"High": "high", "Medium": "med", "Low": "low"}.get(t, "unr")


def stitch_thread(key=""):
    """A self-drawing 'needle & thread' line — fashion-coded signature motion.
    Pure CSS draw + SMIL needle-follow; decorative only, never overlaps content."""
    st.markdown(f"""
    <div style="margin:6px 0 2px" aria-hidden="true">
    <svg viewBox="0 0 1200 40" width="100%" height="40" preserveAspectRatio="none"
         style="overflow:visible">
      <defs>
        <linearGradient id="th{key}" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="{ACCENT}"/>
          <stop offset="50%" stop-color="{ELECTRIC}"/>
          <stop offset="100%" stop-color="{GOLD}"/>
        </linearGradient>
        <filter id="gl{key}"><feGaussianBlur stdDeviation="2.5" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      <path id="thread{key}" pathLength="1"
        d="M0,20 C150,2 250,38 400,20 S650,2 800,20 S1050,38 1200,20"
        fill="none" stroke="rgba(224,71,158,.18)" stroke-width="1.4"/>
      <path pathLength="1"
        d="M0,20 C150,2 250,38 400,20 S650,2 800,20 S1050,38 1200,20"
        fill="none" stroke="url(#th{key})" stroke-width="2"
        stroke-dasharray="1" stroke-dashoffset="1" stroke-linecap="round">
        <animate attributeName="stroke-dashoffset" from="1" to="0"
          dur="2.4s" begin="0.2s" fill="freeze"
          calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/>
      </path>
      <circle r="3.4" fill="#fff" filter="url(#gl{key})">
        <animateMotion dur="4.6s" repeatCount="indefinite" begin="1s"
          keyPoints="0;1" keyTimes="0;1" calcMode="linear">
          <mpath href="#thread{key}"/>
        </animateMotion>
      </circle>
    </svg></div>
    """, unsafe_allow_html=True)


def plotly_theme(fig, h=380):
    fig.update_layout(
        template="plotly_dark", height=h,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=PLOTLY_FONT, color=INK_TX, size=12),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        title=dict(font=dict(family="Fraunces, serif", size=16)),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    return fig


# ──────────────────────────────────────────────────────────────────────────
# APP
# ──────────────────────────────────────────────────────────────────────────
inject_css()

try:
    df, source = load_data()
except Exception as e:
    st.error(str(e))
    st.stop()

rated = df[df["is_rated"] == True] if "is_rated" in df else df

# ── SIDEBAR FILTERS ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='eyebrow'>SmartStyle</div>", unsafe_allow_html=True)
    st.markdown("### Filters")

    q = st.text_input("Search name or brand", "")
    cats = ["All"] + sorted(df["category"].dropna().unique().tolist())
    sel_cat = st.selectbox("Category", cats)

    brand_opts = ["All"] + sorted(df["brand"].dropna().unique().tolist())
    sel_brand = st.selectbox("Brand", brand_opts)

    pmin, pmax = int(df["price"].min()), int(df["price"].max())
    price_range = st.slider("Price (₹)", pmin, pmax, (pmin, min(pmax, 12000)))

    colours = ["All"] + (df["colour"].value_counts().head(20).index.tolist())
    sel_colour = st.selectbox("Colour", colours)

    conf_tiers = st.multiselect(
        "Confidence tier", ["High", "Medium", "Low", "Unrated"],
        default=["High", "Medium", "Low", "Unrated"])

    rated_only = st.toggle("Rated products only", value=False)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.caption(f"Data source: **{source}** · {len(df):,} products")


def apply_filters(data):
    d = data.copy()
    if q:
        ql = q.lower()
        d = d[d["name"].str.lower().str.contains(ql, na=False) |
              d["brand"].str.lower().str.contains(ql, na=False)]
    if sel_cat != "All":
        d = d[d["category"] == sel_cat]
    if sel_brand != "All":
        d = d[d["brand"] == sel_brand]
    if sel_colour != "All":
        d = d[d["colour"] == sel_colour]
    d = d[d["price"].between(*price_range)]
    if conf_tiers:
        d = d[d["confidence_tier"].isin(conf_tiers)]
    if rated_only:
        d = d[d["is_rated"] == True]
    return d


fdf = apply_filters(df)

# ── MASTHEAD ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='masthead rise d1'>
  <div class='eyebrow'>AI-Powered Fashion Intelligence · 14K Catalog</div>
  <h1>SmartStyle <span class='grad'>Analytics</span></h1>
  <div class='sub'>Confidence scoring, market intelligence, and a transparent
  data-quality audit over a {len(df):,}-product fashion catalog — turning a noisy
  e-commerce export into decisions a merchandiser can actually act on.</div>
</div>
""", unsafe_allow_html=True)

# ── LIVE DATA TICKER ──────────────────────────────────────────────────────
_corr = rated["price"].corr(rated["avg_rating"]) if len(rated) else 0
_topc = df["colour"].value_counts(normalize=True).head(2).sum() * 100
_hi = (df["confidence_tier"] == "High").sum()
_items = (
    f"<b>{len(df):,}</b> PRODUCTS <span class='dot'>◆</span>"
    f"<b>{df['brand'].nunique():,}</b> BRANDS <span class='dot'>◆</span>"
    f"PRICE↔RATING r = <b>{_corr:.2f}</b> <span class='dot'>◆</span>"
    f"TOP 2 COLOURS = <b>{_topc:.0f}%</b> OF DEMAND <span class='dot'>◆</span>"
    f"<b>{_hi:,}</b> HIGH-CONFIDENCE PICKS <span class='dot'>◆</span>"
    f"MEAN RATING <b>{rated['avg_rating'].mean():.2f}★</b> <span class='dot'>◆</span>"
    f"<b>{rated['is_rated'].mean()*100:.0f}%</b> RATED COVERAGE <span class='dot'>◆</span>"
)
st.markdown(f"""<div class='ticker rise d2'>
  <div class='ticker-track'>{_items}&nbsp;&nbsp;{_items}</div>
</div>""", unsafe_allow_html=True)
st.write("")

# ── HERO KPIs  (animated count-up, rotating gradient borders) ──────────────
_kpis = [
    ("Products", len(df), 0, "", "#fff", "full catalog"),
    ("Rated coverage", rated["is_rated"].mean()*100 if len(rated) else 0, 0, "%", ACCENT, f"{len(rated):,} with reviews"),
    ("Mean rating", rated["avg_rating"].mean() if len(rated) else 0, 2, "★", GOLD, "rated only"),
    ("Mean confidence", df["confidence_score"].mean(), 0, "", MINT, "0–100 scale"),
    ("Brands", df["brand"].nunique(), 0, "", ELECTRIC, f"{df['category'].nunique()} categories"),
]
_cards = ""
for i, (lab, val, dec, suf, col, delta) in enumerate(_kpis):
    _cards += f"""
    <div class="kpi" style="animation-delay:{i*0.09+0.1}s">
      <div class="lab">{lab}</div>
      <div class="val" style="color:{col}" data-target="{val}" data-dec="{dec}" data-suf="{suf}">0{suf}</div>
      <div class="delta">{delta}</div>
    </div>"""

components.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=JetBrains+Mono:wght@600&display=swap');
*{{box-sizing:border-box}}
body{{margin:0;background:transparent;font-family:'JetBrains Mono',monospace;}}
.grid{{display:flex;gap:14px;flex-wrap:wrap}}
.kpi{{flex:1;min-width:150px;border:1px solid rgba(224,71,158,.18);border-radius:16px;
  padding:18px 20px;position:relative;overflow:hidden;
  background:linear-gradient(180deg,rgba(42,23,71,.55),rgba(18,10,31,.4));
  opacity:0;transform:translateY(16px);animation:rise .7s cubic-bezier(.22,1,.36,1) forwards;
  transition:transform .35s cubic-bezier(.22,1,.36,1),box-shadow .35s;}}
.kpi:before{{content:"";position:absolute;inset:0;border-radius:16px;padding:1px;
  background:conic-gradient(from var(--a,0deg),transparent,{ACCENT},{ELECTRIC},transparent 60%);
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;opacity:0;transition:opacity .4s;
  animation:spin 4s linear infinite;}}
.kpi:hover{{transform:translateY(-7px);box-shadow:0 20px 44px -22px rgba(224,71,158,.6)}}
.kpi:hover:before{{opacity:1}}
@property --a{{syntax:'<angle>';inherits:false;initial-value:0deg}}
@keyframes spin{{to{{--a:360deg}}}}
@keyframes rise{{to{{opacity:1;transform:none}}}}
.lab{{font-size:.66rem;letter-spacing:.18em;text-transform:uppercase;color:{MUTE_TX}}}
.val{{font-family:'Fraunces',serif;font-size:2.1rem;font-weight:700;line-height:1.1;margin-top:.25rem}}
.delta{{font-size:.72rem;color:{MUTE_TX};margin-top:.15rem}}
@media (prefers-reduced-motion:reduce){{.kpi{{animation:none;opacity:1;transform:none}}.kpi:before{{animation:none}}}}
</style>
<div class="grid">{_cards}</div>
<script>
function fmt(n,d){{return Number(n.toFixed(d)).toLocaleString('en-IN')}}
document.querySelectorAll('.val').forEach(function(el){{
  var t=parseFloat(el.dataset.target||'0'),d=parseInt(el.dataset.dec||'0'),s=el.dataset.suf||'';
  var dur=1500,st=null;
  function step(ts){{if(!st)st=ts;var p=Math.min((ts-st)/dur,1);p=1-Math.pow(1-p,3);
    el.textContent=fmt(t*p,d)+s;if(p<1)requestAnimationFrame(step);}}
  requestAnimationFrame(step);
}});
</script>
""", height=140)
st.write("")

stitch_thread("hero")

# ── TABS ──────────────────────────────────────────────────────────────────
tab_intel, tab_explore, tab_conf, tab_reco, tab_quality = st.tabs(
    ["Market Intelligence", "Product Explorer", "Confidence Engine",
     "Recommendations", "Data Quality"])

# ===========================================================================
# 1 · MARKET INTELLIGENCE
# ===========================================================================
with tab_intel:
    st.markdown("### What the catalog is telling us")
    st.caption("All charts respect the sidebar filters. Rating-based views use "
               "rated products only and say so.")

    c1, c2 = st.columns([1.1, 1])

    # colour demand
    with c1:
        cc = fdf["colour"].value_counts().head(10).reset_index()
        cc.columns = ["colour", "count"]
        fig = px.bar(cc, x="count", y="colour", orientation="h",
                     color="count", color_continuous_scale=["#5a2a6e", ACCENT, GOLD],
                     title="Top 10 colours by catalog volume")
        fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
        st.plotly_chart(plotly_theme(fig), use_container_width=True)
        share = fdf["colour"].value_counts(normalize=True).head(2).sum() * 100
        st.caption(f"Top 2 colours = **{share:.0f}%** of the filtered catalog — "
                   "demand is concentrated in neutral/cool tones.")

    # category performance (rated)
    with c2:
        rr = fdf[fdf["is_rated"] == True]
        if len(rr):
            cp = (rr.groupby("category")
                    .agg(rating=("avg_rating", "mean"), n=("p_id", "count"))
                    .query("n >= 15").sort_values("rating", ascending=False).head(10).reset_index())
            fig = px.bar(cp, x="rating", y="category", orientation="h",
                         color="rating", color_continuous_scale=["#5a2a6e", ACCENT_2, MINT],
                         title="Best-rated categories (≥15 rated items)")
            fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
            fig.update_xaxes(range=[3.8, 4.5])
            st.plotly_chart(plotly_theme(fig), use_container_width=True)
        else:
            st.info("No rated products in the current filter.")

    c3, c4 = st.columns([1, 1.1])

    # price distribution
    with c3:
        fig = px.histogram(fdf[fdf["price"] < fdf["price"].quantile(0.98)],
                           x="price", nbins=44, title="Price distribution (≤ p98)")
        fig.update_traces(marker_color=ACCENT, marker_line_width=0)
        st.plotly_chart(plotly_theme(fig), use_container_width=True)
        st.caption(f"Median price **₹{fdf['price'].median():,.0f}** · "
                   f"long right tail up to ₹{fdf['price'].max():,.0f}.")

    # the honest finding: price vs rating
    with c4:
        rr = fdf[fdf["is_rated"] == True]
        if len(rr) > 30:
            corr = rr["price"].corr(rr["avg_rating"])
            samp = rr.sample(min(2500, len(rr)), random_state=1)
            fig = px.scatter(samp, x="price", y="avg_rating", opacity=0.45,
                             color="confidence_score",
                             color_continuous_scale=["#5a2a6e", ACCENT, GOLD],
                             title=f"Price vs rating  ·  r = {corr:.2f}")
            fig.update_traces(marker=dict(size=5))
            st.plotly_chart(plotly_theme(fig), use_container_width=True)
            st.caption("Near-zero correlation: **paying more does not buy a better "
                       "rating.** This is the platform's headline merchandising insight.")
        else:
            st.info("Not enough rated products to show correlation.")

    # brand leaderboard
    st.markdown("#### Brand leaderboard")
    rr = fdf[fdf["is_rated"] == True]
    if len(rr):
        bl = (rr.groupby("brand")
                .agg(products=("p_id", "count"),
                     avg_rating=("avg_rating", "mean"),
                     avg_conf=("confidence_score", "mean"),
                     med_price=("price", "median"),
                     reviews=("ratingCount", "sum"))
                .query("products >= 5")
                .sort_values("avg_conf", ascending=False).head(15).round(2)).reset_index()
        bl.columns = ["Brand", "Products", "Avg rating", "Avg confidence",
                      "Median ₹", "Total reviews"]
        st.dataframe(bl, use_container_width=True, hide_index=True)
        st.caption("Ranked by average confidence (brands with ≥5 rated products).")
    else:
        st.info("No rated products to rank under the current filter.")

# ===========================================================================
# 2 · PRODUCT EXPLORER  (paginated over the full catalog)
# ===========================================================================
with tab_explore:
    top = st.columns([2, 1, 1])
    sort_by = top[0].selectbox(
        "Sort by", ["Confidence (high→low)", "Rating (high→low)",
                    "Price (low→high)", "Price (high→low)", "Most reviewed"])
    per_page = top[1].selectbox("Per page", [12, 24, 48], index=0)
    gdf = fdf.copy()
    sort_map = {
        "Confidence (high→low)": ("confidence_score", False),
        "Rating (high→low)": ("avg_rating", False),
        "Price (low→high)": ("price", True),
        "Price (high→low)": ("price", False),
        "Most reviewed": ("ratingCount", False),
    }
    col, asc = sort_map[sort_by]
    gdf = gdf.sort_values(col, ascending=asc, na_position="last")

    n = len(gdf)
    pages = max(1, (n + per_page - 1) // per_page)
    page = top[2].number_input(f"Page (1–{pages})", 1, pages, 1)
    st.caption(f"**{n:,}** products match your filters · showing page {page} of {pages}")

    start = (page - 1) * per_page
    chunk = gdf.iloc[start:start + per_page]

    if chunk.empty:
        st.warning("No products match these filters. Try widening the price range "
                   "or clearing the search.")
    else:
        ncols = 4
        rows = (len(chunk) + ncols - 1) // ncols
        for r in range(rows):
            cols = st.columns(ncols)
            for ci in range(ncols):
                i = r * ncols + ci
                if i >= len(chunk):
                    continue
                p = chunk.iloc[i]
                with cols[ci]:
                    st.markdown("<div class='pcard'>", unsafe_allow_html=True)
                    img = p.get("img", "")
                    if isinstance(img, str) and img.startswith("http"):
                        st.image(img, use_container_width=True)
                    cls = conf_class(p["confidence_tier"])
                    if p["confidence_tier"] == "Unrated":
                        chip = "<span class='chip unr'>○ Unrated</span>"
                    else:
                        chip = f"<span class='chip {cls}'>◆ {p['confidence_score']:.0f} · {p['confidence_tier']}</span>"
                    rating_txt = (f"★ {p['avg_rating']:.2f} · {int(p['ratingCount']):,} reviews"
                                  if p["is_rated"] else "No reviews yet")
                    st.markdown(f"""
                    <div style='padding:12px 14px 16px'>
                      <div class='pbrand'>{p['brand']}</div>
                      <div class='pname'>{p['name'][:64]}</div>
                      <div style='margin:8px 0'>{chip}</div>
                      <div class='price'>₹{p['price']:,.0f}</div>
                      <div style='color:var(--mute);font-size:.78rem;margin-top:4px'>{rating_txt}</div>
                      <div style='margin-top:8px'>
                        <span class='tag'>{p['category']}</span>
                        <span class='tag'>{p['colour']}</span>
                        {f"<span class='tag'>{p['occasion']}</span>" if isinstance(p.get('occasion'), str) else ""}
                      </div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.write("")

# ===========================================================================
# 3 · CONFIDENCE ENGINE
# ===========================================================================
with tab_conf:
    _mean_conf = float(df["confidence_score"].mean())
    _hi_pct = (df["confidence_tier"] == "High").mean() * 100
    _med_pct = (df["confidence_tier"] == "Medium").mean() * 100
    _circ = 2 * np.pi * 78  # r=78
    _off = _circ * (1 - _mean_conf / 100)
    components.html(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=JetBrains+Mono:wght@600&family=Space+Grotesk&display=swap');
    body{{margin:0;background:transparent;font-family:'Space Grotesk',sans-serif}}
    .wrap{{display:flex;align-items:center;gap:34px;border:1px solid rgba(224,71,158,.18);
      border-radius:20px;padding:24px 30px;
      background:linear-gradient(135deg,rgba(42,23,71,.7),rgba(18,10,31,.45));
      opacity:0;transform:translateY(16px);animation:rise .8s cubic-bezier(.22,1,.36,1) .1s forwards}}
    @keyframes rise{{to{{opacity:1;transform:none}}}}
    .gauge{{position:relative;flex:0 0 auto}}
    .gauge svg{{transform:rotate(-90deg)}}
    .ring-bg{{fill:none;stroke:rgba(255,255,255,.07);stroke-width:12}}
    .ring-fg{{fill:none;stroke:url(#g);stroke-width:12;stroke-linecap:round;
      stroke-dasharray:{_circ:.1f};stroke-dashoffset:{_circ:.1f};
      animation:draw 1.8s cubic-bezier(.22,1,.36,1) .3s forwards;
      filter:drop-shadow(0 0 6px rgba(224,71,158,.6))}}
    @keyframes draw{{to{{stroke-dashoffset:{_off:.1f}}}}}
    .center{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}
    .center .num{{font-family:'Fraunces',serif;font-size:2.5rem;font-weight:700;color:#fff;line-height:1}}
    .center .of{{font-family:'JetBrains Mono',monospace;font-size:.62rem;letter-spacing:.2em;color:{MUTE_TX}}}
    .copy h3{{font-family:'Fraunces',serif;margin:0 0 6px;color:#fff;font-size:1.4rem}}
    .copy p{{color:{MUTE_TX};margin:0 0 12px;font-size:.92rem;max-width:440px;line-height:1.55}}
    .bars{{display:flex;gap:10px;flex-wrap:wrap}}
    .bar{{font-family:'JetBrains Mono',monospace;font-size:.72rem;padding:6px 12px;border-radius:999px}}
    .bar.h{{background:rgba(90,209,168,.14);color:{MINT};border:1px solid rgba(90,209,168,.4)}}
    .bar.m{{background:rgba(242,200,121,.13);color:{GOLD};border:1px solid rgba(242,200,121,.4)}}
    @media(prefers-reduced-motion:reduce){{.ring-fg{{animation:none;stroke-dashoffset:{_off:.1f}}}.wrap{{animation:none;opacity:1;transform:none}}}}
    </style>
    <div class="wrap">
      <div class="gauge">
        <svg width="180" height="180" viewBox="0 0 180 180">
          <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{ACCENT}"/><stop offset="55%" stop-color="{ELECTRIC}"/>
            <stop offset="100%" stop-color="{GOLD}"/></linearGradient></defs>
          <circle class="ring-bg" cx="90" cy="90" r="78"/>
          <circle class="ring-fg" cx="90" cy="90" r="78"/>
        </svg>
        <div class="center"><div class="num" id="cnum">0</div><div class="of">CATALOG / 100</div></div>
      </div>
      <div class="copy">
        <h3>Catalog confidence health</h3>
        <p>A single composite read on how trustworthy the rated catalog looks —
        the average of every product's confidence score, traced live.</p>
        <div class="bars">
          <div class="bar h">◆ {_hi_pct:.0f}% High tier</div>
          <div class="bar m">◆ {_med_pct:.0f}% Medium tier</div>
        </div>
      </div>
    </div>
    <script>
    (function(){{var el=document.getElementById('cnum'),t={_mean_conf:.1},dur=1800,st=null;
    function step(ts){{if(!st)st=ts;var p=Math.min((ts-st)/dur,1);p=1-Math.pow(1-p,3);
    el.textContent=(t*p).toFixed(0);if(p<1)requestAnimationFrame(step);}}requestAnimationFrame(step);}})();
    </script>
    """, height=240)
    st.write("")

    left, right = st.columns([1, 1])
    with left:
        st.markdown("### The Confidence Score, explained")
        st.markdown("""
A single **0–100** signal that ranks how *trustworthy* a product looks from the
data we actually have. It is a transparent heuristic — **not** a returns
predictor, because the source export contains no returns data. Being explicit
about that is the point.

**Three components:**
""")
        st.markdown(f"""
<div class='panel'>
<b style='color:{ACCENT}'>50% · Bayesian-shrunk rating</b><br>
<span style='color:{MUTE_TX}'>A 4.9★ from 3 reviews is not a 4.9. We pull every
rating toward the catalog mean in proportion to how few reviews back it
(prior strength m = 50 reviews), so confidence is earned by evidence.</span>
<br><br>
<b style='color:{ACCENT_2}'>30% · Review-volume reliability</b><br>
<span style='color:{MUTE_TX}'>Log-scaled review count vs the 95th percentile —
rewards products with a statistically meaningful sample.</span>
<br><br>
<b style='color:{GOLD}'>20% · Price-value sanity</b><br>
<span style='color:{MUTE_TX}'>Expensive items with weak ratings are penalised;
fairly-priced, well-rated items are not.</span>
</div>
""", unsafe_allow_html=True)
        st.code(textwrap.dedent("""
        bayes = (v/(v+m))*R + (m/(v+m))*C      # m=50, C=global mean
        s_rating = clip((bayes-3)/2, 0, 1)
        s_volume = clip(log1p(v)/log1p(p95_v), 0, 1)
        s_value  = clip(1 - price_pct*(1-s_rating), 0, 1)
        score    = 100*(0.50*s_rating + 0.30*s_volume + 0.20*s_value)
        """).strip(), language="python")

    with right:
        # distribution
        rr = df[df["is_rated"] == True]
        fig = px.histogram(rr, x="confidence_score", nbins=40,
                           title="Confidence distribution (rated products)")
        fig.update_traces(marker_color=ACCENT_2, marker_line_width=0)
        for x, lab, col in [(45, "Med", GOLD), (70, "High", MINT)]:
            fig.add_vline(x=x, line_dash="dash", line_color=col,
                          annotation_text=lab, annotation_font_color=col)
        st.plotly_chart(plotly_theme(fig, h=330), use_container_width=True)

        tier_counts = df["confidence_tier"].value_counts()
        fig2 = px.pie(values=tier_counts.values, names=tier_counts.index, hole=.62,
                      color=tier_counts.index,
                      color_discrete_map={"High": MINT, "Medium": GOLD,
                                          "Low": ACCENT, "Unrated": "#6b5a85"},
                      title="Catalog by confidence tier")
        fig2.update_traces(textinfo="label+percent")
        st.plotly_chart(plotly_theme(fig2, h=330), use_container_width=True)

    st.markdown("#### Highest-confidence products in the catalog")
    show = (df[df["is_rated"] == True]
            .nlargest(10, "confidence_score")
            [["name", "brand", "category", "price", "avg_rating",
              "ratingCount", "confidence_score"]].round(2))
    show.columns = ["Product", "Brand", "Category", "₹", "Rating", "Reviews", "Confidence"]
    st.dataframe(show, use_container_width=True, hide_index=True)

# ===========================================================================
# 4 · RECOMMENDATIONS  —  safer picks
# ===========================================================================
with tab_reco:
    st.markdown("### Find a safer, better-rated alternative")
    st.caption("Pick any product; the engine surfaces same-category items with a "
               "higher confidence score, ranked by confidence and price proximity.")

    pick_pool = fdf if len(fdf) else df
    names = pick_pool["name"].head(400).tolist()
    chosen = st.selectbox("Choose a product", names) if names else None

    if chosen:
        base = pick_pool[pick_pool["name"] == chosen].iloc[0]
        a, b = st.columns([1, 2])
        with a:
            if isinstance(base.get("img"), str) and base["img"].startswith("http"):
                st.image(base["img"], use_container_width=True)
        with b:
            st.markdown(f"#### {base['name']}")
            st.markdown(f"<span class='pbrand'>{base['brand']}</span>", unsafe_allow_html=True)
            m = st.columns(3)
            m[0].metric("Price", f"₹{base['price']:,.0f}")
            m[1].metric("Rating", f"{base['avg_rating']:.2f}★" if base["is_rated"] else "—")
            m[2].metric("Confidence", f"{base['confidence_score']:.0f}" if base["is_rated"] else "Unrated")
            st.markdown(f"<span class='tag'>{base['category']}</span>"
                        f"<span class='tag'>{base['colour']}</span>", unsafe_allow_html=True)

        base_conf = base["confidence_score"] if base["is_rated"] else 0
        alts = df[(df["category"] == base["category"]) &
                  (df["p_id"] != base["p_id"]) &
                  (df["is_rated"] == True) &
                  (df["confidence_score"] > base_conf)].copy()
        if len(alts):
            alts["price_gap"] = (alts["price"] - base["price"]).abs()
            alts = alts.sort_values(["confidence_score", "price_gap"],
                                    ascending=[False, True]).head(4)
            st.markdown("#### Safer picks")
            cols = st.columns(4)
            for col, (_, ap) in zip(cols, alts.iterrows()):
                with col:
                    st.markdown("<div class='pcard'>", unsafe_allow_html=True)
                    if isinstance(ap.get("img"), str) and ap["img"].startswith("http"):
                        st.image(ap["img"], use_container_width=True)
                    save = base["price"] - ap["price"]
                    save_txt = (f"Save ₹{save:,.0f}" if save > 0 else f"+₹{-save:,.0f}")
                    st.markdown(f"""
                    <div style='padding:12px 14px 16px'>
                      <div class='pbrand'>{ap['brand']}</div>
                      <div class='pname'>{ap['name'][:54]}</div>
                      <div style='margin:8px 0'><span class='chip high'>◆ {ap['confidence_score']:.0f}</span></div>
                      <div class='price'>₹{ap['price']:,.0f}</div>
                      <div style='color:var(--mint);font-size:.76rem'>★ {ap['avg_rating']:.2f} · {save_txt}</div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.success("This is already among the strongest picks in its category — "
                       "no higher-confidence alternative found.")

# ===========================================================================
# 5 · DATA QUALITY  (the part recruiters love)
# ===========================================================================
with tab_quality:
    st.markdown("### Data-quality audit")
    st.caption("A real export is messy. This page documents exactly what was wrong "
               "and how it was handled — the analytical decisions behind the numbers.")

    q1, q2, q3 = st.columns(3)
    with q1:
        st.markdown(f"""<div class='panel'><h3>Cleaning</h3>
        <span class='tag'>14,330 → {len(df):,} rows</span>
        <ul style='color:{MUTE_TX};font-size:.86rem;line-height:1.7'>
        <li>Dropped junk index column</li>
        <li>Removed 18 empty + 106 duplicate IDs</li>
        <li>Coerced price / rating to numeric</li>
        <li>Parsed colour, category, occasion, fabric</li>
        </ul></div>""", unsafe_allow_html=True)
    with q2:
        cov = rated["is_rated"].mean() * 100 if len(rated) else 0
        st.markdown(f"""<div class='panel'><h3>The honest catch</h3>
        <span class='tag' style='color:{ACCENT};border-color:{ACCENT}'>{100-cov:.0f}% unrated</span>
        <p style='color:{MUTE_TX};font-size:.86rem;line-height:1.6'>
        Only <b style='color:{INK_TX}'>{cov:.0f}%</b> of products carry any rating.
        Rather than invent ratings, unrated items are flagged
        <code>is_rated=False</code> and excluded from every rating-based stat.
        No fabricated 4.1★ averages here.</p></div>""", unsafe_allow_html=True)
    with q3:
        st.markdown(f"""<div class='panel'><h3>Why Bayesian</h3>
        <p style='color:{MUTE_TX};font-size:.86rem;line-height:1.6'>
        Raw means over-reward tiny samples. Shrinking ratings toward the global
        mean by review volume produces a fair, evidence-weighted score — the same
        idea behind IMDb's Top-250 weighting.</p>
        <span class='tag'>prior m = 50</span><span class='tag'>log-scaled volume</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Missingness by field")
    miss = (df.isna().mean() * 100).round(1)
    miss = miss[miss > 0].sort_values(ascending=False).reset_index()
    miss.columns = ["field", "missing_pct"]
    fig = px.bar(miss, x="missing_pct", y="field", orientation="h",
                 color="missing_pct", color_continuous_scale=["#5a2a6e", ACCENT],
                 title="Percent missing per column")
    fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
    st.plotly_chart(plotly_theme(fig, h=max(320, 26 * len(miss))), use_container_width=True)
    st.caption("Attribute fields (waistband, pockets, neck…) are sparsely populated "
               "in the source — surfaced honestly rather than hidden.")

    with st.expander("Download the cleaned dataset"):
        st.download_button("⬇ fashion_clean.csv",
                           df.to_csv(index=False).encode("utf-8"),
                           "fashion_clean.csv", "text/csv")

# ── FOOTER ────────────────────────────────────────────────────────────────
st.markdown(f"""<div class='footer'>SMARTSTYLE ANALYTICS · {len(df):,} PRODUCTS ·
BUILT BY DEBASMITA CHATTERJEE · CONFIDENCE SCORING + TRANSPARENT EDA</div>""",
            unsafe_allow_html=True)
