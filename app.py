
import streamlit as st
import pandas as pd
import pickle
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Myntra StyleGuard (Public Demo)", page_icon="👗")

# ---------------------------
# Loading Dataset from GitHub 
# ---------------------------
CSV_URL = "https://raw.githubusercontent.com/yourusername/myntra-styleguard-demo/main/Fashion%20Dataset.csv"  # ← Replace with your own raw link
EMBEDDINGS_PATH = "demo_embeddings.pkl"

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    if len(df) > 10:
        df = df.sample(10, random_state=42).reset_index(drop=True)
    df.fillna({'description': '', 'p_attributes': '', 'img': '', 'brand': ''}, inplace=True)
    df['avg_rating'] = df['avg_rating'].fillna(0)
    if 'category' not in df.columns:
        df['category'] = 'General'
    df['combined_text'] = df['name'] + " " + df['description'] + " " + df['p_attributes']
    df['confidence'] = (df['avg_rating'] / df['avg_rating'].max() * 100).round(0)
    df['buyers_kept'] = df['confidence'].apply(lambda x: f"{int(x)}% buyers kept this product")
    return df

df = load_data()

# ---------------------------
# Load or Compute Embeddings
# ---------------------------
@st.cache_resource
def get_embeddings(df):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['combined_text'].tolist(), show_progress_bar=False)
    return embeddings

embeddings = get_embeddings(df)
cos_sim = cosine_similarity(embeddings, embeddings)

# ---------------------------
#  Helper Functions
# ---------------------------
def get_similar_products(index, top_n=5, min_rating=0):
    sim_scores = sorted(enumerate(cos_sim[index]), key=lambda x: x[1], reverse=True)
    result = []
    for idx, score in sim_scores[1:]:
        if df.loc[idx, 'avg_rating'].round() < min_rating:
            continue
        result.append(idx)
        if len(result) >= top_n:
            break
    return df.iloc[result]

def get_cheaper_alternatives(index, top_n=5, min_rating=0):
    base_price = df.loc[index, 'price']
    sim_scores = sorted(enumerate(cos_sim[index]), key=lambda x: x[1], reverse=True)
    result = []
    for idx, score in sim_scores[1:]:
        if df.loc[idx, 'price'] >= base_price:
            continue
        if df.loc[idx, 'avg_rating'].round() < min_rating:
            continue
        result.append(idx)
        if len(result) >= top_n:
            break
    return df.iloc[result]

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("👗 Myntra StyleGuard — Public Demo")

min_rating = st.slider("Minimum Rating (⭐)", 0, 5, 0, 1)
product_choice = st.selectbox("Choose a Product:", df['name'].tolist())

product_index = df[df['name'] == product_choice].index[0]
row = df.iloc[product_index]

st.image(row['img'], width=400)
st.subheader(row['name'])
st.markdown(f"**Brand:** {row['brand']}")
st.markdown(f"**Price:** ₹{row['price']}")
st.markdown(f"**Rating:** {'⭐'*int(round(row['avg_rating']))} ({row['avg_rating']:.1f})")
st.markdown(f"**{row['buyers_kept']}**")

# Similar Products
st.markdown("### 🔹 Similar Products")
sim_df = get_similar_products(product_index, top_n=5, min_rating=min_rating)
cols = st.columns(5)
for i, (idx, r) in enumerate(sim_df.iterrows()):
    with cols[i]:
        st.image(r['img'], width=120)
        st.caption(f"{r['name']} — ₹{r['price']}")

# Cheaper Alternatives
st.markdown("### 🔹 Cheaper Alternatives")
cheap_df = get_cheaper_alternatives(product_index, top_n=5, min_rating=min_rating)
cols = st.columns(5)
for i, (idx, r) in enumerate(cheap_df.iterrows()):
    with cols[i]:
        st.image(r['img'], width=120)
        st.caption(f"{r['name']} — ₹{r['price']}")

st.markdown("### 💹 Price Comparison")
fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(df['name'], df['price'], color='lightcoral')
ax.set_ylabel("Price (₹)")
ax.set_xticklabels(df['name'], rotation=45, ha='right', fontsize=8)
st.pyplot(fig)

