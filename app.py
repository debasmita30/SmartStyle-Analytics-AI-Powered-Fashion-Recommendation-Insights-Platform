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

# ----------------------- TITLE ------------------------------
st.title("🛍️ SmartStyle Analytics: AI-Powered Fashion Recommendation & Insights Platform")
st.markdown("Empowering Myntra with data-driven fashion intelligence, recommendations, and product insights.")

# ----------------------- LOAD DATA --------------------------
@st.cache_data
def load_data():
    CSV_URL = "https://raw.githubusercontent.com/debasmita30/SmartStyle-Analytics-AI-Powered-Fashion-Recommendation-Insights-Platform/main/Fashion%20Dataset.csv"
    df = pd.read_csv(CSV_URL)
    df.dropna(subset=["name", "brand", "price", "avg_rating"], inplace=True)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["avg_rating"] = pd.to_numeric(df["avg_rating"], errors="coerce")
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
col1.metric("Total Products", len(df))
col2.metric("Average Price (₹)", f"{df['price'].mean():.2f}")
col3.metric("Average Rating", f"{df['avg_rating'].mean():.2f}")

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

# ----------------------- TOP RATED PRODUCTS CAROUSEL --------
st.markdown("### 🌟 Top Rated Products")

# Horizontal scroll CSS
st.markdown(
    """
    <style>
    .scroll-container {
        display: flex;
        overflow-x: auto;
        padding: 10px 0px;
    }
    .scroll-item {
        flex: 0 0 auto;
        margin-right: 15px;
        max-width: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

top_rated = df.sort_values("avg_rating", ascending=False).head(10)

scroll_html = '<div class="scroll-container">'
for _, product in top_rated.iterrows():
    try:
        response = requests.get(product["img"], timeout=5)
        img = Image.open(BytesIO(response.content))
        img.save(f"/tmp/{product['name']}.png")
        scroll_html += f'''
        <div class="scroll-item">
            <img src="data:image/png;base64,{st.image(img, output_format="PNG")._repr_png_().decode("utf-8")}" width="200">
            <p style="font-size:12px; font-weight:bold;">{product["name"]} ({product["avg_rating"]}⭐)</p>
        </div>
        '''
    except:
        scroll_html += f'''
        <div class="scroll-item">
            <p style="font-size:12px;">Image not available</p>
        </div>
        '''
scroll_html += '</div>'
st.markdown(scroll_html, unsafe_allow_html=True)

# ----------------------- PRODUCT GALLERY ---------------------
st.markdown("### 👗 Product Gallery")
products_per_row = 3
rows = (len(filtered_df) + products_per_row - 1) // products_per_row

for r in range(rows):
    cols = st.columns(products_per_row)
    for c in range(products_per_row):
        idx = r * products_per_row + c
        if idx < len(filtered_df):
            product = filtered_df.iloc[idx]
            with cols[c]:
                try:
                    response = requests.get(product["img"], timeout=5)
                    img = Image.open(BytesIO(response.content))
                    st.image(img, use_container_width=True)
                except:
                    st.warning("Image not available.")
                st.subheader(product["name"])
                st.write(f"**Brand:** {product['brand']}")
                st.write(f"**Price:** ₹{product['price']:.2f}")
                st.write(f"**Rating:** ⭐ {product['avg_rating']}")
                st.progress(min(product["avg_rating"] / 5, 1.0))
                st.caption(f"Color: {product['colour']}")
                st.markdown("---")

# ----------------------- FOOTER -------------------------------
st.markdown("""
---
### 💡 About SmartStyle Analytics  
**SmartStyle Analytics** uses AI-powered insights to recommend styles, analyze fashion trends, and visualize data for Myntra’s product catalog.  
Developed by *Debasmita Chatterjee*.
""")
