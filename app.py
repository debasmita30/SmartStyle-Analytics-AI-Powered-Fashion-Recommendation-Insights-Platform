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

# ----------------------- ANIMATED BACKGROUND ----------------
# This section creates the animated gradient background and card hover effect
st.markdown(
    """
    <style>
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
    .product-card {
        transition: transform 0.2s, box-shadow 0.2s;
        padding: 10px;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.1); /* Optional: slight background for cards */
        backdrop-filter: blur(5px); /* Optional: frosted glass effect */
    }
    .product-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    # Drop rows where price or rating could not be converted
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
    y=alt.Y('avg_rating', title='Average Rating', scale=alt.Scale(domain=[4, 5])),
    tooltip=['brand', 'avg_rating']
).properties(width=700, height=400)

st.altair_chart(chart, use_container_width=True)

st.markdown("---") # Visual separator

# ----------------------- DYNAMIC PRODUCT GALLERY (FIXED) ---------------------
st.markdown(f"### 👗 Product Gallery ({len(filtered_df)} products found)")

# Sort the filtered results to show the best-rated products first
sorted_filtered_df = filtered_df.sort_values("avg_rating", ascending=False)

if sorted_filtered_df.empty:
    st.warning("No products match your current filter criteria. Please adjust the filters.")
else:
    products_per_row = 3
    # Calculate rows based on the length of the sorted_filtered_df
    rows = (len(sorted_filtered_df) + products_per_row - 1) // products_per_row

    for r in range(rows):
        cols = st.columns(products_per_row)
        for c in range(products_per_row):
            idx = r * products_per_row + c
            if idx < len(sorted_filtered_df):
                product = sorted_filtered_df.iloc[idx]
                with cols[c]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    try:
                        response = requests.get(product["img"], timeout=5)
                        img = Image.open(BytesIO(response.content))
                        st.image(img, use_container_width=True)
                    except Exception as e:
                        st.warning("Image not available.")
                    st.subheader(product["name"])
                    st.write(f"**Brand:** {product['brand']}")
                    st.write(f"**Price:** ₹{product['price']:.2f}")
                    st.write(f"**Rating:** ⭐ {product['avg_rating']}")
                    st.progress(min(product["avg_rating"] / 5, 1.0))
                    st.caption(f"Color: {product['colour']}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.write("") # Adds a little vertical space after each card

# ----------------------- FOOTER -------------------------------
st.markdown("""
---
### 💡 About SmartStyle Analytics
**SmartStyle Analytics** uses AI-powered insights to recommend styles, analyze fashion trends, and visualize data for Myntra’s product catalog.
Developed by *Debasmita Chatterjee*.
""")
