import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import altair as alt

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Retail Product Analytics & Recommendation Modeling",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# THEME STATE
# ============================================================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

THEME = st.session_state.theme

PALETTES = {
    "dark": {
        "bg": "#16151A",
        "bg_secondary": "#1E1D22",
        "surface": "#23222A",
        "surface_hover": "#2A2932",
        "border": "rgba(255,255,255,0.08)",
        "border_strong": "rgba(255,255,255,0.16)",
        "text": "#F2F0EC",
        "text_muted": "#9A98A0",
        "text_dim": "#6E6C74",
        "thread": "#D4683E",
        "sage": "#8FAA80",
        "rust": "#C45B4F",
        "gold": "#D9B24C",
        "chart_grid": "rgba(255,255,255,0.06)",
    },
    "light": {
        "bg": "#FAF7F2",
        "bg_secondary": "#F1ECE3",
        "surface": "#FFFFFF",
        "surface_hover": "#F6F2EC",
        "border": "rgba(22,21,26,0.10)",
        "border_strong": "rgba(22,21,26,0.18)",
        "text": "#16151A",
        "text_muted": "#6B6960",
        "text_dim": "#9A9890",
        "thread": "#C2542E",
        "sage": "#5F7A52",
        "rust": "#A8392E",
        "gold": "#A9791E",
        "chart_grid": "rgba(22,21,26,0.06)",
    },
}
C = PALETTES[THEME]

# ============================================================
# GLOBAL CSS
# ============================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&family=Caveat:wght@600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: {C['bg']};
    color: {C['text']};
}}

[data-testid="stSidebar"] {{
    background: {C['bg_secondary']};
    border-right: 1px solid {C['border']};
}}

[data-testid="stSidebar"] * {{
    color: {C['text']} !important;
}}

#MainMenu, footer, header {{visibility: hidden;}}

/* ---------- Page-load fade ---------- */
.fade-in {{
    animation: fadeInUp 0.6s ease-out both;
}}
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.fade-1 {{ animation-delay: 0.02s; }}
.fade-2 {{ animation-delay: 0.10s; }}
.fade-3 {{ animation-delay: 0.18s; }}
.fade-4 {{ animation-delay: 0.26s; }}

/* ---------- Hero ---------- */
.hero-wrap {{
    background: {C['bg_secondary']};
    border: 1px solid {C['border']};
    border-radius: 16px;
    padding: 28px 32px 22px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
}}
.hero-title-row {{
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 4px;
}}
.hero-title {{
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 30px;
    letter-spacing: -0.01em;
    color: {C['text']};
    margin: 0;
}}
.hero-script {{
    font-family: 'Caveat', cursive;
    font-weight: 600;
    font-size: 24px;
    color: {C['thread']};
    transform: rotate(-2.5deg);
    display: inline-block;
}}
.hero-sub {{
    font-size: 11.5px;
    letter-spacing: 0.05em;
    color: {C['text_muted']};
    text-transform: uppercase;
    margin-top: 2px;
}}

/* ---------- KPI cards ---------- */
.kpi-card {{
    background: {C['surface']};
    border: 1px solid {C['border']};
    border-radius: 12px;
    padding: 16px 18px;
    transition: border-color 0.25s ease, transform 0.25s ease;
}}
.kpi-card:hover {{
    border-color: {C['border_strong']};
    transform: translateY(-2px);
}}
.kpi-label {{
    font-size: 10.5px;
    letter-spacing: 0.05em;
    color: {C['text_muted']};
    text-transform: uppercase;
    margin-bottom: 7px;
}}
.kpi-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 23px;
    font-weight: 600;
    color: {C['text']};
}}
.kpi-delta-pos {{ color: {C['sage']}; font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:500; }}
.kpi-delta-neg {{ color: {C['rust']}; font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:500; }}

/* ---------- Section labels ---------- */
.section-label {{
    font-size: 11.5px;
    letter-spacing: 0.06em;
    color: {C['text_muted']};
    text-transform: uppercase;
    margin: 26px 0 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.section-label::before {{
    content: '';
    width: 3px;
    height: 12px;
    background: {C['thread']};
    border-radius: 1px;
    display: inline-block;
}}

/* ---------- Tag card (product) ---------- */
.tag-card {{
    background: {C['surface']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    padding: 14px 13px 13px;
    position: relative;
    margin-bottom: 16px;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}}
.tag-card:hover {{
    transform: translateY(-4px);
    border-color: {C['border_strong']};
    box-shadow: 0 8px 24px rgba(0,0,0,0.18);
}}
.tag-hole {{
    position: absolute;
    top: 11px;
    left: 11px;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: {C['bg']};
    border: 1.2px solid {C['border_strong']};
    z-index: 3;
}}
.tag-name {{
    font-size: 13.5px;
    font-weight: 500;
    line-height: 1.35;
    margin: 10px 0 2px;
    color: {C['text']};
    min-height: 36px;
}}
.tag-brand {{
    font-size: 11px;
    color: {C['text_muted']};
    margin-bottom: 10px;
}}
.tag-price-row {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-top: 1px dashed {C['border_strong']};
    padding-top: 9px;
    margin-top: 6px;
}}
.tag-price {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 14.5px;
    font-weight: 600;
    color: {C['text']};
}}
.badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 10.5px;
    font-weight: 500;
    padding: 4px 9px;
    border-radius: 20px;
    margin-bottom: 8px;
}}
.badge-gem {{ background: rgba(143,170,128,0.16); color: {C['sage']}; }}
.badge-risk {{ background: rgba(196,91,79,0.16); color: {C['rust']}; }}
.badge-premium {{ background: rgba(217,178,76,0.16); color: {C['gold']}; }}

/* ---------- Theme toggle button styling ---------- */
div[data-testid="stButton"] button {{
    background: {C['surface']} !important;
    border: 1px solid {C['border_strong']} !important;
    color: {C['text']} !important;
    border-radius: 20px !important;
    font-size: 12.5px !important;
    transition: all 0.2s ease !important;
}}
div[data-testid="stButton"] button:hover {{
    background: {C['surface_hover']} !important;
    border-color: {C['thread']} !important;
}}

hr {{ border-color: {C['border']} !important; }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================
CATEGORY_TOKENS = ['Kurta','Saree','Dress','Sweatshirt','T-Shirt','Tshirt','Shirt','Jeans','Trousers','Top',
                    'Jacket','Sweater','Poncho','Skirt','Palazzo','Leggings','Blazer','Co-ords','Jumpsuit',
                    'Dupatta','Kurti','Salwar','Lehenga','Gown','Tunic','Shrug','Cardigan','Hoodie','Pyjama',
                    'Track Pants','Shorts','Capris','Tights']

def extract_category(name):
    name = str(name)
    for t in CATEGORY_TOKENS:
        if t.lower() in name.lower():
            return t
    return "Other"

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/debasmita30/SmartStyle-Analytics-AI-Powered-Fashion-Recommendation-Insights-Platform/main/Fashion%20Dataset.csv"
    df = pd.read_csv(url)
    df.dropna(subset=["name", "brand", "price", "img"], inplace=True)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["avg_rating"] = pd.to_numeric(df["avg_rating"], errors="coerce")
    df.dropna(subset=["price"], inplace=True)
    df["avg_rating"] = df["avg_rating"].fillna(df["avg_rating"].median())

    df["category"] = df["name"].apply(extract_category)

    cat_median = df.groupby("category")["price"].median()
    df["category_median_price"] = df["category"].map(cat_median)
    df["price_deviation"] = ((df["price"] - df["category_median_price"]) / df["category_median_price"]) * 100

    cat_avg_rating = df.groupby("category")["avg_rating"].mean()
    df["category_avg_rating"] = df["category"].map(cat_avg_rating)

    rating_norm = (df["avg_rating"] - df["avg_rating"].min()) / (df["avg_rating"].max() - df["avg_rating"].min() + 1e-9)
    price_norm = (df["price"] - df["price"].min()) / (df["price"].max() - df["price"].min() + 1e-9)
    df["value_score"] = (rating_norm - price_norm).round(3)

    df["is_hidden_gem"] = (df["price_deviation"] < -10) & (df["avg_rating"] >= 4.2)
    df["is_overpriced_risk"] = (df["price_deviation"] > 25) & (df["avg_rating"] < 4.0)
    df["is_premium_justified"] = (df["price_deviation"] > 15) & (df["avg_rating"] >= 4.4)

    return df

df = load_data()

# ============================================================
# SIDEBAR FILTERS
# ============================================================
with st.sidebar:
    st.markdown(f"<div style='font-family:Fraunces,serif; font-weight:600; font-size:17px; margin-bottom:2px;'>Filter catalog</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:11px; color:{C['text_muted']}; margin-bottom:18px;'>Narrow the 14,330-SKU dataset</div>", unsafe_allow_html=True)

    categories = ["All"] + sorted([c for c in df["category"].unique() if c != "Other"]) + ["Other"]
    selected_category = st.selectbox("Category", categories)

    brands_pool = df if selected_category == "All" else df[df["category"] == selected_category]
    brands = ["All"] + sorted(brands_pool["brand"].dropna().unique().tolist())
    selected_brand = st.selectbox("Brand", brands)

    min_price, max_price = int(df["price"].min()), int(df["price"].max())
    price_range = st.slider("Price range (₹)", min_price, max_price, (min_price, max_price))

    min_rating = st.slider("Minimum rating", 0.0, 5.0, 3.0, step=0.1)

    st.markdown("---")
    signal_filter = st.radio(
        "Highlight",
        ["All products", "Hidden gems only", "Overpriced risk only", "Premium justified only"],
        index=0
    )

    st.markdown("---")
    st.button(f"Switch to {'light' if THEME=='dark' else 'dark'} mode", on_click=toggle_theme, use_container_width=True)

filtered_df = df[
    ((df["brand"] == selected_brand) | (selected_brand == "All")) &
    ((df["category"] == selected_category) | (selected_category == "All")) &
    (df["price"].between(price_range[0], price_range[1])) &
    (df["avg_rating"] >= min_rating)
].copy()

if signal_filter == "Hidden gems only":
    filtered_df = filtered_df[filtered_df["is_hidden_gem"]]
elif signal_filter == "Overpriced risk only":
    filtered_df = filtered_df[filtered_df["is_overpriced_risk"]]
elif signal_filter == "Premium justified only":
    filtered_df = filtered_df[filtered_df["is_premium_justified"]]

# ============================================================
# HERO
# ============================================================
st.markdown(f"""
<div class="hero-wrap fade-in fade-1">
  <div class="hero-title-row">
    <span class="hero-title">Retail Product Analytics</span>
    <span class="hero-script">&amp; Recommendation Modeling</span>
  </div>
  <div class="hero-sub">{len(df):,} SKUs · {df['brand'].nunique():,} brands · price &amp; rating intelligence across the live catalog</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KPI ROW (with real signed metrics)
# ============================================================
overpriced_pct = (df["is_overpriced_risk"].sum() / len(df)) * 100
gem_count = int(df["is_hidden_gem"].sum())
underpriced_share = (df["price_deviation"] < -10).sum() / len(df) * 100
gem_share = gem_count / len(df) * 100

k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (k1, "Catalog size", f"{len(df):,}", None),
    (k2, "Median price", f"₹{df['price'].median():,.0f}", None),
    (k3, "Avg rating", f"{df['avg_rating'].mean():.2f}", None),
    (k4, "Hidden gem share", f"+{gem_share:.1f}%", "pos"),
    (k5, "Overpriced risk share", f"-{overpriced_pct:.1f}%", "neg"),
]
for i, (col, label, value, sign) in enumerate(kpis):
    delta_class = ""
    if sign == "neg":
        value_html = f"<span class='kpi-delta-neg'>{value}</span>"
    elif sign == "pos":
        value_html = f"<span class='kpi-delta-pos'>{value}</span>"
    else:
        value_html = value
    with col:
        st.markdown(f"""
        <div class="kpi-card fade-in fade-{min(i+1,4)}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value_html}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# SIGNATURE SKETCH LINE — price journey budget -> luxury
# ============================================================
st.markdown('<div class="section-label">Catalog price journey</div>', unsafe_allow_html=True)

bins = pd.qcut(df["price"], 12, duplicates="drop")
journey = df.groupby(bins, observed=True)["avg_rating"].mean().values
journey_norm = (journey - journey.min()) / (journey.max() - journey.min() + 1e-9)

n = len(journey_norm)
xs = np.linspace(10, 590, n)
ys = 140 - (journey_norm * 110) - 10
path_d = f"M {xs[0]:.1f} {ys[0]:.1f} "
for i in range(1, n):
    cx = (xs[i-1] + xs[i]) / 2
    path_d += f"Q {cx:.1f} {ys[i-1]:.1f}, {xs[i]:.1f} {ys[i]:.1f} "

sketch_svg = f"""
<div class="fade-in fade-2" style="background:{C['bg_secondary']}; border:1px solid {C['border']}; border-radius:14px; padding:20px 24px 14px;">
<div style="font-size:11px; color:{C['text_muted']}; margin-bottom:6px;">avg rating across price deciles — budget to luxury</div>
<svg viewBox="0 0 600 150" style="width:100%; height:160px;" preserveAspectRatio="none">
  <defs>
    <filter id="wob">
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.06" numOctaves="2" seed="7" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="3"/>
    </filter>
  </defs>
  <path id="sketchline" d="{path_d}" fill="none" stroke="{C['thread']}" stroke-width="2.5"
    stroke-linecap="round" style="filter:url(#wob); stroke-dasharray:1400; stroke-dashoffset:1400;"/>
</svg>
<div style="display:flex; justify-content:space-between; font-size:10px; color:{C['text_dim']}; padding:0 4px 4px;">
  <span>₹{int(df['price'].min())}</span><span>₹{int(df['price'].median())}</span><span>₹{int(df['price'].max()):,}</span>
</div>
</div>
<script>
const p = document.getElementById('sketchline');
if (p) {{ requestAnimationFrame(() => {{ p.style.transition = 'stroke-dashoffset 1.6s ease-out'; p.style.strokeDashoffset = '0'; }}); }}
</script>
"""
st.markdown(sketch_svg, unsafe_allow_html=True)

# ============================================================
# CHARTS ROW
# ============================================================
st.markdown('<div class="section-label">Brand &amp; value intelligence</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Only rank brands with enough rated products for the average to mean anything —
    # most brands in this catalog have a single rated SKU, which made every bar
    # look identical (all ~5.0) and crammed ten long brand names onto the axis.
    MIN_RATED_PRODUCTS = 20
    rated = df.dropna(subset=["avg_rating"])
    brand_sample_size = rated.groupby("brand").size()
    eligible_brands = brand_sample_size[brand_sample_size >= MIN_RATED_PRODUCTS].index
    reliable = rated[rated["brand"].isin(eligible_brands)]

    top_brands = reliable.groupby("brand")["avg_rating"].mean().sort_values(ascending=False).head(8).reset_index()
    top_brands["brand_short"] = top_brands["brand"].str.slice(0, 14)

    rating_color_scale = alt.Scale(
        domain=[top_brands["avg_rating"].min(), top_brands["avg_rating"].max()],
        range=[C["rust"], C["gold"], C["sage"]]
    )
    bar = alt.Chart(top_brands).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X("brand_short", sort="-y", title=None, axis=alt.Axis(labelAngle=-30, labelColor=C["text_muted"], labelFontSize=10.5, labelLimit=120)),
        y=alt.Y("avg_rating", title="Avg rating", scale=alt.Scale(domain=[3.5, 4.5]),
                axis=alt.Axis(labelColor=C["text_muted"], gridColor=C["chart_grid"], titleColor=C["text_muted"])),
        color=alt.Color("avg_rating", scale=rating_color_scale, legend=None),
        tooltip=["brand", alt.Tooltip("avg_rating", format=".2f")]
    ).properties(height=300, title=alt.TitleParams(f"Top brands by rating (min {MIN_RATED_PRODUCTS} rated products)", color=C["text"], fontSize=12, font="Inter")
    ).configure_view(strokeWidth=0).configure_axis(domainColor=C["border_strong"])
    st.altair_chart(bar, use_container_width=True)
    st.caption(f"Scale starts at 3.5 to show real spread — {len(eligible_brands)} of {df['brand'].nunique()} brands have enough ratings to compare fairly.")

with chart_col2:
    # Real product colors, not a generic palette — uses the dataset's own colour column,
    # mapped to actual swatches so the chart matches what the products look like.
    SWATCH_MAP = {
        "black": "#2B2B2B", "blue": "#3266AD", "pink": "#D4537E", "green": "#5C8A4A",
        "navy blue": "#1B2A4A", "white": "#E8E5DC", "red": "#B33A2E", "grey": "#8C8A82",
        "maroon": "#6B2330", "yellow": "#D9B23A", "beige": "#C9B89A", "mustard": "#C68A2E",
        "off white": "#EDE8DA", "peach": "#E8A98C", "purple": "#6B4A8A",
    }
    color_counts = df["colour"].str.strip().value_counts().head(10).reset_index()
    color_counts.columns = ["colour", "count"]
    color_counts["share"] = color_counts["count"] / len(df) * 100
    color_counts["swatch"] = color_counts["colour"].str.lower().map(SWATCH_MAP).fillna(C["text_dim"])

    donut = alt.Chart(color_counts).mark_arc(innerRadius=58, stroke=C["bg"], strokeWidth=2).encode(
        theta=alt.Theta("count", stack=True),
        color=alt.Color("colour", scale=alt.Scale(domain=color_counts["colour"].tolist(), range=color_counts["swatch"].tolist()), legend=None),
        order=alt.Order("count", sort="descending"),
        tooltip=["colour", "count", alt.Tooltip("share", format=".1f", title="share %")]
    ).properties(height=300, title=alt.TitleParams("Catalog share by colour (top 10)", color=C["text"], fontSize=12, font="Inter")
    ).configure_view(strokeWidth=0)
    st.altair_chart(donut, use_container_width=True)

    top4_share = color_counts.head(4)["share"].sum()
    st.caption(f"Top 4 colours make up {top4_share:.1f}% of the catalog — demand is concentrated, not evenly spread.")

st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
scatter_full = df.sample(min(900, len(df)), random_state=42).copy()
scatter_full["signal"] = np.where(scatter_full["is_hidden_gem"], "Hidden gem",
                      np.where(scatter_full["is_overpriced_risk"], "Overpriced risk",
                      np.where(scatter_full["is_premium_justified"], "Premium justified", "Standard")))
signal_scale = alt.Scale(domain=["Hidden gem", "Overpriced risk", "Premium justified", "Standard"],
                         range=[C["sage"], C["rust"], C["gold"], C["text_dim"]])
scatter = alt.Chart(scatter_full).mark_circle(size=42, opacity=0.75).encode(
    x=alt.X("price", title="Price (₹)", axis=alt.Axis(labelColor=C["text_muted"], gridColor=C["chart_grid"], titleColor=C["text_muted"])),
    y=alt.Y("avg_rating", title="Rating", scale=alt.Scale(domain=[0, 5]),
            axis=alt.Axis(labelColor=C["text_muted"], gridColor=C["chart_grid"], titleColor=C["text_muted"])),
    color=alt.Color("signal", scale=signal_scale, legend=alt.Legend(title=None, labelColor=C["text_muted"], orient="bottom")),
    tooltip=["name", "brand", "price", alt.Tooltip("avg_rating", format=".2f"), "signal"]
).properties(height=300, title=alt.TitleParams("Price vs rating — value quadrants", color=C["text"], fontSize=12, font="Inter")
).configure_view(strokeWidth=0).configure_axis(domainColor=C["border_strong"])
st.altair_chart(scatter, use_container_width=True)

# ============================================================
# PRODUCT GALLERY
# ============================================================
st.markdown(f'<div class="section-label">Product gallery — {len(filtered_df):,} matches</div>', unsafe_allow_html=True)

sorted_df = filtered_df.sort_values("avg_rating", ascending=False)

if sorted_df.empty:
    st.warning("No products match the current filters. Try widening the price range or lowering the minimum rating.")
else:
    per_row = 4
    show_df = sorted_df.head(40)
    rows = (len(show_df) + per_row - 1) // per_row

    for r in range(rows):
        cols = st.columns(per_row)
        for c in range(per_row):
            idx = r * per_row + c
            if idx >= len(show_df):
                continue
            product = show_df.iloc[idx]
            with cols[c]:
                badge_html = ""
                if product["is_hidden_gem"]:
                    badge_html = f'<span class="badge badge-gem">Hidden gem</span><br>'
                elif product["is_overpriced_risk"]:
                    badge_html = f'<span class="badge badge-risk">Overpriced risk</span><br>'
                elif product["is_premium_justified"]:
                    badge_html = f'<span class="badge badge-premium">Premium justified</span><br>'

                dev = product["price_deviation"]
                dev_class = "kpi-delta-neg" if dev < 0 else "kpi-delta-pos"
                dev_sign = f"{dev:+.1f}%"

                st.markdown(f"""
                <div class="tag-card">
                    <div class="tag-hole"></div>
                """, unsafe_allow_html=True)

                try:
                    resp = requests.get(product["img"], timeout=4)
                    img = Image.open(BytesIO(resp.content))
                    st.image(img, use_container_width=True)
                except Exception:
                    st.markdown(f"<div style='height:140px; background:{C['bg_secondary']}; border-radius:4px; display:flex; align-items:center; justify-content:center; color:{C['text_dim']}; font-size:11px;'>image unavailable</div>", unsafe_allow_html=True)

                st.markdown(f"""
                    {badge_html}
                    <div class="tag-name">{product['name'][:48]}{'…' if len(str(product['name']))>48 else ''}</div>
                    <div class="tag-brand">{product['brand']} · ⭐ {product['avg_rating']:.2f}</div>
                    <div class="tag-price-row">
                        <span class="tag-price">₹{product['price']:,.0f}</span>
                        <span class="{dev_class}">{dev_sign}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<div style="margin-top:36px; padding-top:18px; border-top:1px solid {C['border']}; font-size:11.5px; color:{C['text_dim']};">
Retail Product Analytics &amp; Recommendation Modeling · price deviation, value score, and risk signals computed live from catalog medians per category · built by Debasmita Chatterjee
</div>
""", unsafe_allow_html=True)
