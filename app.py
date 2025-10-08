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

# ----------------------- ANIMATED BACKGROUND (UPDATED) ----------------
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

    /* --- NEW: Falling Icons Animation --- */
    .falling-icons {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: -1; /* Ensure it stays behind content */
        pointer-events: none; /* Make sure it doesn't interfere with clicks */
    }

    .falling-icons i {
        position: absolute;
        display: block;
        font-size: 20px; /* Base size */
        color: rgba(255, 255, 255, 0.6); /* Semi-transparent white */
        animation: fall linear infinite;
    }

    /* Animation definition for falling objects */
    @keyframes fall {
        0% {
            transform: translateY(-100px) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }

    /* Individual icon styles for variety */
    .falling-icons i:nth-child(even) {
        animation-duration: 10s;
        animation-delay: 0s;
        left: 5%;
        font-size: 25px;
    }
    .falling-icons i:nth-child(odd) {
        animation-duration: 12s;
        animation-delay: 2s;
        left: 15%;
        font-size: 18px;
    }
    .falling-icons i:nth-child(3n) {
        animation-duration: 8s;
        animation-delay: 4s;
        left: 25%;
        font-size: 30px;
    }
    .falling-icons i:nth-child(4n) {
        animation-duration: 11s;
        animation-delay: 6s;
        left: 35%;
        font-size: 22px;
    }
    .falling-icons i:nth-child(5n) {
        animation-duration: 9s;
        animation-delay: 1s;
        left: 45%;
        font-size: 28px;
    }
    .falling-icons i:nth-child(6n) {
        animation-duration: 13s;
        animation-delay: 3s;
        left: 55%;
        font-size: 20px;
    }
    .falling-icons i:nth-child(7n) {
        animation-duration: 10s;
        animation-delay: 5s;
        left: 65%;
        font-size: 32px;
    }
    .falling-icons i:nth-child(8n) {
        animation-duration: 14s;
        animation-delay: 7s;
        left: 75%;
        font-size: 24px;
    }
    .falling-icons i:nth-child(9n) {
        animation-duration: 11s;
        animation-delay: 0.5s;
        left: 85%;
        font-size: 26px;
    }
    .falling-icons i:nth-child(10n) {
        animation-duration: 9s;
        animation-delay: 2.5s;
        left: 95%;
        font-size: 19px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Insert the falling icons. We'll use Font Awesome icons.
# Make sure to include Font Awesome CSS in your Streamlit app for this to work.
# You can add this line at the very beginning of your app (outside st.markdown for CSS):
# st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="falling-icons">
        <i class="fas fa-shopping-bag"></i>
        <i class="fas fa-tshirt"></i>
        <i class="fas fa-shoe-prints"></i>
        <i class="fas fa-tag"></i>
        <i class="fas fa-hat-cowboy"></i>
        <i class="fas fa-socks"></i>
        <i class="fas fa-gem"></i>
        <i class="fas fa-scarf"></i>
        <i class="fas fa-handbag"></i>
        <i class="fas fa-glasses"></i>
        <i class="fas fa-shopping-bag"></i>
        <i class="fas fa-tshirt"></i>
        <i class="fas fa-shoe-prints"></i>
        <i class="fas fa-tag"></i>
        <i class="fas fa-hat-cowboy"></i>
        <i class="fas fa-socks"></i>
        <i class="fas fa-gem"></i>
        <i class="fas fa-scarf"></i>
        <i class="fas fa-handbag"></i>
        <i class="fas fa-glasses"></i>
    </div>
    """,
    unsafe_allow_html=True
)
# Make sure to include Font Awesome CSS for the icons to display:
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)


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
    y=alt.Y('avg_rating', title='Average Rating'), # Removed the hardcoded scale for dynamic range
    tooltip=['brand', 'avg_rating']
).properties(width=700, height=400)

st.altair_chart(chart, use_container_width=True)

st.markdown("---") 

# ----------------------- DYNAMIC PRODUCT GALLERY WITH SUGGESTION ENGINE ---------------------
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
                    
                    # --- SUGGESTION ENGINE LOGIC ---
                    is_high_risk = product['price'] > 3000 and product['avg_rating'] < 4.2
                    is_safe_bet = product['avg_rating'] >= 4.5

                    try:
                        response = requests.get(product["img"], timeout=5)
                        img = Image.open(BytesIO(response.content))
                        st.image(img, use_container_width=True)
                    except Exception as e:
                        st.warning("Image not available.")
                    
                    st.subheader(product["name"])

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
