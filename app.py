import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import altair as alt

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="SmartStyle Analytics",
    page_icon="🛍️",
    layout="wide"
)

# ----------------------- LIGHTWEIGHT SPARKLE ANIMATED BACKGROUND ----------------
st.markdown("""
<style>
/* Gradient background */
body {
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}
@keyframes gradientBG {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

/* Product Card Hover Effects */
.product-card {
    transition: transform 0.2s, box-shadow 0.2s;
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
.product-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.3);
}

/* Sparkle effect */
.sparkle {
    position: fixed;
    width: 6px;
    height: 6px;
    background: white;
    border-radius: 50%;
    opacity: 0;
    animation: sparkle 4s linear infinite;
    z-index: -1;
    pointer-events: none;
}

@keyframes sparkle {
    0% { transform: translateY(0) translateX(0); opacity: 0; }
    10% { opacity: 1; }
    100% { transform: translateY(100vh) translateX(20px); opacity: 0; }
}
</style>

<!-- Add multiple sparkles at different positions and delays -->
<div class="sparkle" style="left:10%; animation-delay:0s;"></div>
<div class="sparkle" style="left:25%; animation-delay:1s;"></div>
<div class="sparkle" style="left:40%; animation-delay:2s;"></div>
<div class="sparkle" style="left:55%; animation-delay:3s;"></div>
<div class="sparkle" style="left:70%; animation-delay:1.5s;"></div>
<div class="sparkle" style="left:85%; animation-delay:2.5s;"></div>
""", unsafe_allow_html=True)

# ----------------------- TITLE ------------------------------
st.title("🛍️ SmartStyle Analytics: AI-Powered Fashion Recommendation & Insights Platform")
st.markdown("Empowering Myntra with data-driven fashion intelligence, recommendations, and product insights.")

# ----------------------- LOAD DATA --------------------------
@st.cache_data
def load_data():
    CSV_URL = "https://raw.githubusercontent.com/debasmita30/SmartStyle-Analytics-AI-Powered-Fashion-Recommendation-Insights-Platform/main/Fashion%20Dataset.csv"
    df = pd.read_csv(CSV_URL)
    df.dropna(subset=["name", "brand", "price", "avg_rating", "img"], inplace=True)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["avg_rating"] = pd.to_numeric(df["avg_rating"], errors="coerce")
    df.dropna(subset=["price", "avg_rating"], inplace=True)
    return df

df = load_data()

# ----------------------- SIDEBAR FILTERS ---------------------
st.sidebar.header("🔍 Filter Products")
brands = ["All"] + sorted(df["brand"].dropna().unique().tolist())
selected_brand = st.sidebar.selectbox("Select Brand", brands)
min_price, max_price = int(df["price"].min()), int(df["price"].max())
price_range = st.sidebar.slider("Select Price Range", min_price, max_price, (min_price, max_price))
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.0)

# Size Selection
sizes = ['All', 'S', 'M', 'L', 'XL']
selected_size = st.sidebar.radio("Select Size", sizes, horizontal=True)

filtered_df = df[
    ((df["brand"] == selected_brand) | (selected_brand == "All")) &
    (df["price"].between(price_range[0], price_range[1])) &
    (df["avg_rating"] >= min_rating)
]

# ----------------------- DASHBOARD METRICS -------------------
st.subheader("📊 Fashion Insights Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Products in Catalog", f"{len(df):,}")
col2.metric("Average Price (₹)", f"{df['price'].mean():.2f}")
col3.metric("Average Rating", f"{df['avg_rating'].mean():.2f} ⭐")

# ----------------------- CHARTS ------------------------------
st.markdown("### 📈 Top 10 Brands by Average Rating")
top_brands = df.groupby("brand")["avg_rating"].mean().sort_values(ascending=False).head(10)
top_brands_df = top_brands.reset_index()

chart = alt.Chart(top_brands_df).mark_bar(color='mediumorchid').encode(
    x=alt.X('brand', sort='-y', title='Brand'),
    y=alt.Y('avg_rating', title='Average Rating'),
    tooltip=['brand', 'avg_rating']
).properties(width=700, height=400)

st.altair_chart(chart, use_container_width=True)
st.markdown("---")

# ----------------------- DYNAMIC PRODUCT GALLERY ---------------------
st.markdown(f"### 👗 Product Gallery ({len(filtered_df)} products found)")
sorted_filtered_df = filtered_df.sort_values("avg_rating", ascending=False)

if sorted_filtered_df.empty:
    st.warning("No products match your current filter criteria. Please adjust the filters.")
else:
    products_per_row = 3
    rows = (len(sorted_filtered_df) + products_per_row - 1) // products_per_row

    for r in range(rows):
        cols = st.columns(products_per_row)
        for c in range(products_per_row):
            idx = r * products_per_row + c
            if idx < len(sorted_filtered_df):
                product = sorted_filtered_df.iloc[idx]
                with cols[c]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)

                    is_high_risk = product['price'] > 3000 and product['avg_rating'] < 4.2
                    is_safe_bet = product['avg_rating'] >= 4.5

                    try:
                        response = requests.get(product["img"], timeout=5)
                        img = Image.open(BytesIO(response.content))
                        st.image(img, use_container_width=True)
                    except:
                        st.warning("Image not available.")

                    st.subheader(product["name"])
                    if selected_size != 'All':
                        st.info(f"✅ Available in your selected size: {selected_size}")
                    
                    if is_safe_bet:
                        st.success("✅ Confidence Pick: 95%+ buyers kept this item!")
                    elif is_high_risk:
                        st.warning("⚠️ Heads-up: Potential high return risk.")

                    st.write(f"**Brand:** {product['brand']}")
                    st.write(f"**Price:** ₹{product['price']:.2f}")
                    st.write(f"**Rating:** ⭐ {product['avg_rating']}")
                    st.progress(min(product["avg_rating"] / 5, 1.0))

                    if is_high_risk:
                        alternatives = df[
                            (df['brand'] == product['brand']) &
                            (df['price'] < product['price']) &
                            (df['avg_rating'] > product['avg_rating'])
                        ].sort_values('avg_rating', ascending=False).head(2)

                        if not alternatives.empty:
                            with st.expander("💡 View Safer, Better-Rated Alternatives"):
                                for i, alt_product in alternatives.iterrows():
                                    st.markdown(f"**{alt_product['name']}**")
                                    st.write(f"**Price:** ₹{alt_product['price']:.2f} (You save ₹{product['price'] - alt_product['price']:.2f}!)")
                                    st.write(f"**Rating:** ⭐ {alt_product['avg_rating']} (Higher Rating)")
                                    st.markdown("---")

                    st.caption(f"Color: {product['colour']}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.write("")

# ----------------------- FOOTER -------------------------------
st.markdown("""
---
### 💡 About SmartStyle Analytics
**SmartStyle Analytics** uses AI-powered insights to recommend styles, analyze fashion trends, and visualize data for Myntra’s product catalog.

Developed by *Debasmita Chatterjee*.
""")
