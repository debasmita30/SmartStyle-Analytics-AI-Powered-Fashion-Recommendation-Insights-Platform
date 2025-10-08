
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

# ----------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="SmartStyle Analytics",
    page_icon="🛍️",
    layout="wide",
)

# ----------------------------------------------------
# CUSTOM ANIMATED BACKGROUND CSS
# ----------------------------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #a1c4fd, #c2e9fb);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
    color: #000000;
}
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
}
h1, h2, h3, h4, h5, h6 {
    color: #2b2b2b;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# TITLE & INTRODUCTION
# ----------------------------------------------------
st.title("🛍️ SmartStyle Analytics")
st.subheader("AI-Powered Fashion Recommendation & Insights Platform for Myntra")
st.markdown("""
This interactive data science platform uses AI and visualization techniques to explore fashion trends, product performance, and customer preferences.
""")

# ----------------------------------------------------
# LOAD DATASET FROM GITHUB
# ----------------------------------------------------
@st.cache_data
def load_data():
    CSV_URL = "https://raw.githubusercontent.com/debasmita30/SmartStyle-Analytics-AI-Powered-Fashion-Recommendation-Insights-Platform/main/Fashion%20Dataset.csv"
    df = pd.read_csv(CSV_URL)
    df.dropna(subset=["name", "brand", "price", "avg_rating"], inplace=True)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["avg_rating"] = pd.to_numeric(df["avg_rating"], errors="coerce")
    return df

df = load_data()

# ----------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------
st.sidebar.header("🎯 Filter Products")

brands = ["All"] + sorted(df["brand"].dropna().unique().tolist())
selected_brand = st.sidebar.selectbox("Select Brand", brands)

min_price, max_price = int(df["price"].min()), int(df["price"].max())
price_range = st.sidebar.slider("Select Price Range (₹)", min_price, max_price, (min_price, max_price))

min_rating = st.sidebar.slider("Minimum Rating (⭐)", 0.0, 5.0, 3.0)

filtered_df = df[
    ((df["brand"] == selected_brand) | (selected_brand == "All")) &
    (df["price"].between(price_range[0], price_range[1])) &
    (df["avg_rating"] >= min_rating)
]

# ----------------------------------------------------
# DASHBOARD METRICS
# ----------------------------------------------------
st.markdown("### 📊 Fashion Insights Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Products", len(df))
col2.metric("Average Price (₹)", f"{df['price'].mean():.2f}")
col3.metric("Average Rating", f"{df['avg_rating'].mean():.2f}")

# ----------------------------------------------------
# VISUAL INSIGHTS
# ----------------------------------------------------
st.markdown("### 💎 Top 10 Brands by Average Rating")

top_brands = df.groupby("brand")["avg_rating"].mean().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 4))
top_brands.plot(kind="bar", color="#ff7b72", ax=ax)
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 Brands by Average Rating", fontsize=13)
st.pyplot(fig)

# ----------------------------------------------------
# PRODUCT GALLERY
# ----------------------------------------------------
st.markdown("### 👗 Explore Fashion Products")

for _, row in filtered_df.iterrows():
    with st.container():
        cols = st.columns([1, 3])
        with cols[0]:
            try:
                response = requests.get(row["img"], timeout=5)
                img = Image.open(BytesIO(response.content))
                st.image(img, caption=row["name"], width=160)
                if st.button(f"🔍 View: {row['p_id']}", key=row["p_id"]):
                    st.image(img, caption=f"🖼️ {row['name']} – {row['brand']}", use_container_width=True)
            except:
                st.warning("⚠️ Image not available")
        with cols[1]:
            st.subheader(row["name"])
            st.write(f"**Brand:** {row['brand']}")
            st.write(f"**Price:** ₹{row['price']:.2f}")
            st.write(f"**Average Rating:** ⭐ {row['avg_rating']:.1f}")
            st.progress(min(row["avg_rating"] / 5, 1.0))
            st.caption(f"Color: {row.get('colour', 'N/A')}")
            st.markdown("---")

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------
st.markdown("""
---
### 💡 About SmartStyle Analytics  
**SmartStyle Analytics** leverages AI-powered insights to recommend styles, analyze fashion trends, and visualize product data for Myntra.  
""")

