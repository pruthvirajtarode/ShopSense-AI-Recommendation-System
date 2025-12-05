# app/streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from pathlib import Path

# -------------------------
# Config & Paths
# -------------------------
st.set_page_config(page_title="ShopSense — Premium Recommender", page_icon="🛍️", layout="wide", initial_sidebar_state="expanded")
BASE_DIR = Path(__file__).resolve().parents[1]      # project root (ShopSense_Full_Project)
DATA_DIR = BASE_DIR / "data" / "processed"
PRODUCTS_FILE = DATA_DIR / "products.csv"

API_URL = os.getenv("API_URL", "DUMMY")


# -------------------------
# Helper utilities
# -------------------------
def safe_read_products(path):
    if not path.exists():
        # create a tiny fallback DataFrame if missing
        df = pd.DataFrame([
            ("P100027","Formal Shirt","Clothing",299.0,4.3,"https://via.placeholder.com/240x240.png?text=P100027"),
            ("P100339","Travel Bottle","Home",149.0,4.0,"https://via.placeholder.com/240x240.png?text=P100339"),
            ("P100118","Smartphone Case","Electronics",399.0,4.2,"https://via.placeholder.com/240x240.png?text=P100118"),
            ("P100195","Backpack","Accessories",999.0,4.5,"https://via.placeholder.com/240x240.png?text=P100195"),
            ("P100212","Digital Alarm Clock","Electronics",499.0,3.9,"https://via.placeholder.com/240x240.png?text=P100212"),
        ], columns=["StockCode","Description","Category","Price","Rating","ImageURL"])
        return df
    df = pd.read_csv(path)
    # normalize columns
    if "StockCode" not in df.columns:
        # try fallback names
        if "product_id" in df.columns: df = df.rename(columns={"product_id":"StockCode"})
        elif "Stockcode" in df.columns: df = df.rename(columns={"Stockcode":"StockCode"})
    # ensure required columns
    if "Description" not in df.columns: df["Description"] = df["StockCode"].apply(lambda x: f"Product {x}")
    if "Category" not in df.columns: df["Category"] = "General"
    if "Price" not in df.columns:
        # create synthetic prices
        np.random.seed(42)
        df["Price"] = np.round(np.random.uniform(100, 2500, size=len(df)), 2)
    if "Rating" not in df.columns:
        np.random.seed(1)
        df["Rating"] = np.round(np.random.uniform(3.5, 5.0, size=len(df)), 1)
    if "ImageURL" not in df.columns:
        # placeholder images
        df["ImageURL"] = df["StockCode"].apply(lambda x: f"https://via.placeholder.com/240x240.png?text={x}")
    return df

def price_predictor(price):
    """
    Returns a simple 'predicted price' (demonstration).
    This could be replaced by an ML model artifact (saved model) later.
    """
    # Add small random markup / discount for demo
    noise = np.random.normal(loc=1.02, scale=0.05)
    return round(price * noise, 2)

def fetch_recommendations(user_id, top_n):
    # ✅ CLOUD MODE: use fallback recommender if FastAPI is not reachable
    if API_URL == "DUMMY":
        return list(products_df["StockCode"].sample(top_n))

    try:
        resp = requests.get(f"{API_URL}/{user_id}?top_n={top_n}", timeout=5)
        resp.raise_for_status()
        return resp.json().get("recommendations", [])
    except:
        return list(products_df["StockCode"].sample(top_n))

def similar_products(df, code, top_k=4):
    """Return similar products by same category (fallback)."""
    row = df[df["StockCode"] == code]
    if row.empty:
        return []
    category = row["Category"].values[0]
    same_cat = df[df["Category"] == category]
    same_cat = same_cat[same_cat["StockCode"] != code]
    # sort by Rating and Price closeness
    same_cat["score"] = (same_cat["Rating"].rank(ascending=False) * 2) - (abs(same_cat["Price"] - row["Price"].values[0]) / (row["Price"].values[0] + 1))
    same_cat = same_cat.sort_values("score", ascending=False)
    return same_cat.head(top_k).to_dict("records")

# -------------------------
# Load Data
# -------------------------
products_df = safe_read_products(PRODUCTS_FILE)

# -------------------------
# UI: style & theme toggle
# -------------------------
THEMES = {
    "light": {
        "bg": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "primary": "#667eea",
        "secondary": "#764ba2",
        "text": "#2d3748",
        "accent": "#e53e3e"
    },
    "dark": {
        "bg": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)",
        "card_bg": "rgba(26, 32, 44, 0.9)",
        "primary": "#81a1c1",
        "secondary": "#5e81ac",
        "text": "#e2e8f0",
        "accent": "#f56565"
    }
}
st.sidebar.title("🎨 Display Settings")
theme_choice = st.sidebar.radio("Theme", ["light", "dark"], index=0)
T = THEMES[theme_choice]

# Inject advanced CSS for professional website look, animations, and interactivity
st.markdown(f"""
<style>
    body {{
        background: {T['bg']};
        color: {T['text']};
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
        transition: all 0.3s ease;
    }}
    .navbar {{
        background: linear-gradient(135deg, {T['primary']}, {T['secondary']});
        color: white;
        padding: 15px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 1000;
    }}
    .navbar h1 {{
        margin: 0;
        font-size: 24px;
        font-weight: 700;
    }}
    .navbar .theme-toggle {{
        background: rgba(255,255,255,0.2);
        border: none;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .navbar .theme-toggle:hover {{
        background: rgba(255,255,255,0.3);
    }}
    .hero-section {{
        text-align: center;
        padding: 80px 20px;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)), url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        position: relative;
    }}
    .hero-section::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.3);
        border-radius: 20px;
    }}
    .hero-section > * {{
        position: relative;
        z-index: 1;
    }}
    .hero-section h2 {{
        font-size: 36px;
        margin-bottom: 10px;
        background: linear-gradient(45deg, {T['primary']}, {T['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .hero-section p {{
        font-size: 18px;
        color: {T['text']};
        opacity: 0.8;
    }}
    .section {{
        margin: 40px 0;
        padding: 30px;
        background: {T['card_bg']};
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }}
    .section::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, transparent 70%);
        pointer-events: none;
    }}
    .product-gallery {{
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02)), url('https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        position: relative;
    }}
    .product-gallery::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.1);
    }}
    .product-gallery > * {{
        position: relative;
        z-index: 1;
    }}
    .section h3 {{
        color: {T['primary']};
        margin-bottom: 20px;
        font-size: 28px;
        text-align: center;
        position: relative;
        z-index: 1;
    }}
    .section-icon {{
        display: inline-block;
        width: 40px;
        height: 40px;
        margin-right: 10px;
        vertical-align: middle;
    }}
    .card {{
        background: {T['card_bg']};
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
    }}
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        filter: brightness(1.05);
    }}
    .card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }}
    .card:hover::before {{
        left: 100%;
    }}
    .card::after {{
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, {T['primary']}, {T['secondary']});
        border-radius: 17px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    .card:hover::after {{
        opacity: 0.3;
    }}
    .product-name {{
        color: {T['primary']};
        font-weight: 700;
        font-size: 18px;
        margin-bottom: 8px;
    }}
    .small-muted {{
        color: #a0aec0;
        font-size: 14px;
    }}
    .price {{
        font-weight: 800;
        color: {T['accent']};
        font-size: 20px;
    }}
    .rating {{
        color: #fbbf24;
        font-size: 16px;
    }}
    .btn-primary {{
        background: linear-gradient(45deg, {T['primary']}, {T['secondary']});
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        font-size: 16px;
    }}
    .btn-primary:hover {{
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }}
    .search-input {{
        border-radius: 25px;
        border: 2px solid {T['primary']};
        padding: 10px 15px;
        width: 100%;
        transition: all 0.3s ease;
        font-size: 16px;
    }}
    .search-input:focus {{
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }}
    .sidebar {{
        background: {T['card_bg']};
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }}
    .footer {{
        text-align: center;
        padding: 30px;
        background: {T['card_bg']}, url('https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        margin-top: 40px;
        border-top: 2px solid {T['primary']};
        position: relative;
    }}
    .footer::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.4);
        border-radius: 15px;
    }}
    .footer > * {{
        position: relative;
        z-index: 1;
    }}
    .footer h4 {{
        color: {T['primary']};
        margin-bottom: 10px;
    }}
    .footer p {{
        color: {T['text']};
        opacity: 0.8;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .fade-in {{
        animation: fadeIn 0.5s ease-in;
    }}
    .bounce-in {{
        animation: bounceIn 0.8s ease-out;
    }}
    .pulse {{
        animation: pulse 2s infinite;
    }}
    .float {{
        animation: float 3s ease-in-out infinite;
    }}
    @keyframes bounceIn {{
        0% {{ opacity: 0; transform: scale(0.3); }}
        50% {{ opacity: 1; transform: scale(1.05); }}
        70% {{ transform: scale(0.9); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    .product-image {{
        transition: transform 0.3s ease;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .product-image:hover {{
        transform: scale(1.1);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }}
    .stats-card {{
        background: linear-gradient(135deg, {T['primary']}, {T['secondary']});
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        margin: 10px;
    }}
    .stats-card h4 {{
        margin: 0 0 5px 0;
        font-size: 24px;
        font-weight: 700;
    }}
    .stats-card p {{
        margin: 0;
        opacity: 0.9;
        font-size: 14px;
    }}
    .floating-shapes {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }}
    .shape {{
        position: absolute;
        opacity: 0.1;
        animation: float 6s ease-in-out infinite;
    }}
    .shape:nth-child(1) {{
        top: 10%;
        left: 10%;
        width: 50px;
        height: 50px;
        background: {T['primary']};
        border-radius: 50%;
        animation-delay: 0s;
    }}
    .shape:nth-child(2) {{
        top: 20%;
        right: 10%;
        width: 30px;
        height: 30px;
        background: {T['secondary']};
        border-radius: 50%;
        animation-delay: 2s;
    }}
    .shape:nth-child(3) {{
        bottom: 20%;
        left: 20%;
        width: 40px;
        height: 40px;
        background: {T['accent']};
        clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
        animation-delay: 4s;
    }}
    .shape:nth-child(4) {{
        bottom: 10%;
        right: 20%;
        width: 35px;
        height: 35px;
        background: {T['primary']};
        border-radius: 50%;
        animation-delay: 1s;
    }}
    .loading-spinner {{
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
        margin-right: 10px;
    }}
    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}
    .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
    }}
    .flex {{
        display: flex;
        gap: 20px;
        align-items: center;
    }}
    .input-group {{
        margin-bottom: 20px;
    }}
    .input-group label {{
        display: block;
        margin-bottom: 5px;
        font-weight: 600;
        color: {T['text']};
    }}
</style>
""", unsafe_allow_html=True)

# Inject JavaScript for interactivity
st.components.v1.html(f"""
<script>
    // Add hover tooltips and zoom effects
    document.addEventListener('DOMContentLoaded', function() {{
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {{
            card.addEventListener('mouseenter', function() {{
                const img = card.querySelector('img');
                if (img) {{
                    img.style.transform = 'scale(1.1)';
                }}
            }});
            card.addEventListener('mouseleave', function() {{
                const img = card.querySelector('img');
                if (img) {{
                    img.style.transform = 'scale(1)';
                }}
            }});
        }});
        
        // Add tooltips to ratings
        const ratings = document.querySelectorAll('.rating');
        ratings.forEach(rating => {{
            rating.title = 'Customer Rating';
        }});
    }});
</script>
""", height=0, width=0)

# -------------------------
# Navigation Bar
# -------------------------
st.markdown(f"""
<div class="navbar">
    <h1>🛍️ ShopSense</h1>
    <button class="theme-toggle" onclick="document.querySelector('input[value=\'{theme_choice}\']').click()">🌙 {theme_choice.title()} Mode</button>
</div>
<div class="floating-shapes">
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
</div>
<div class="particles" id="particles"></div>
<script>
    // Generate random particles
    const particlesContainer = document.getElementById('particles');
    for (let i = 0; i < 20; i++) {{
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.width = Math.random() * 4 + 2 + 'px';
        particle.style.height = particle.style.width;
        particle.style.animationDelay = Math.random() * 10 + 's';
        particle.style.animationDuration = (Math.random() * 5 + 5) + 's';
        particlesContainer.appendChild(particle);
    }}
</script>
""", unsafe_allow_html=True)

# -------------------------
# Hero Section
# -------------------------
st.markdown(f"""
<div class="hero-section fade-in">
    <h2>Welcome to ShopSense</h2>
    <p>Discover personalized product recommendations powered by advanced AI. Explore our curated collection and find your perfect match.</p>
</div>
""", unsafe_allow_html=True)

# -------------------------
# Search & Filter Section
# -------------------------
st.markdown("""
<div class="section fade-in">
    <h3>🔍 Search & Filter</h3>
    <div class="grid" style="grid-template-columns: 2fr 1fr;">
""", unsafe_allow_html=True)
left, right = st.columns([3,1])
with left:
    query = st.text_input("Search products (name or id)", "", key="search", help="Type product name or ID to search")
    categories = ["All"] + sorted(products_df["Category"].unique().tolist())
    chosen_cat = st.selectbox("Filter category", categories, help="Select a category to filter products")
with right:
    st.write("")  # spacing
    user_id = st.number_input("User ID", min_value=10000, max_value=99999, value=10000, step=1, help="Enter user ID for recommendations")
    top_n = st.slider("Top-N", 5, 20, 10, help="Number of recommendations to generate")

st.markdown("</div></div>", unsafe_allow_html=True)

# -------------------------
# Data Filtering for product listing
# -------------------------
filtered = products_df.copy()
if query:
    q = str(query).lower()
    filtered = filtered[filtered["Description"].str.lower().str.contains(q) | filtered["StockCode"].str.lower().str.contains(q)]
if chosen_cat != "All":
    filtered = filtered[filtered["Category"] == chosen_cat]

# -------------------------
# Product Gallery Section
# -------------------------
st.markdown("""
<div class="section fade-in">
    <h3>🛒 Product Gallery</h3>
    <div class="grid">
""", unsafe_allow_html=True)

def render_product_card(p):
    return f"""
    <div class="card">
      <div class="flex">
        <img src="{p['ImageURL']}" width="120" class="product-image" />
        <div style="flex: 1;">
          <div class="product-name">{p['Description']}</div>
          <div class="small-muted">{p['Category']} • ID: {p['StockCode']}</div>
          <div style="margin-top:8px;">
            <span class="price">₹{p['Price']}</span>
            &nbsp;&nbsp;<span class="rating">{'★'*int(round(p['Rating']))}</span>
            &nbsp;&nbsp;<span class="small-muted">({p['Rating']}/5)</span>
          </div>
        </div>
      </div>
    </div>
    """

rows = filtered.to_dict("records")
for r in rows[:9]:
    st.markdown(render_product_card(r), unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------
# User Profile Section
# -------------------------
st.markdown("""
<div class="section fade-in">
    <h3>👤 User Profile Insights</h3>
    <p style="text-align: center; margin-bottom: 20px;">Discover your shopping preferences through data visualization</p>
""", unsafe_allow_html=True)

# Mock user data for demonstration
sample_size = min(20, len(products_df))
user_purchases = products_df.sample(sample_size, random_state=user_id).copy()
user_categories = user_purchases['Category'].value_counts()
user_price_range = pd.cut(user_purchases['Price'], bins=[0, 500, 1000, 2000, 5000], labels=['Under ₹500', '₹500-₹1000', '₹1000-₹2000', 'Over ₹2000'])

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="stats-card bounce-in">
        <h4>{len(user_purchases)}</h4>
        <p>Total Purchases</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stats-card bounce-in" style="animation-delay: 0.2s;">
        <h4>₹{user_purchases['Price'].mean():.0f}</h4>
        <p>Average Order Value</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-card bounce-in" style="animation-delay: 0.4s;">
        <h4>{user_categories.index[0] if len(user_categories) > 0 else 'N/A'}</h4>
        <p>Favorite Category</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stats-card bounce-in" style="animation-delay: 0.6s;">
        <h4>{user_purchases['Rating'].mean():.1f}⭐</h4>
        <p>Average Rating Given</p>
    </div>
    """, unsafe_allow_html=True)

# Charts
st.markdown("<div class='fade-in' style='margin-top: 30px;'><h4 style='color: " + T['primary'] + "; text-align: center;'>Your Shopping Insights</h4></div>", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    # Category preferences
    category_data = user_categories.head(5)
    st.markdown(f"<div style='background: {T['card_bg']}; padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);'><h5 style='color: {T['primary']}; margin-bottom: 15px;'>🛍️ Category Preferences</h5></div>", unsafe_allow_html=True)
    st.bar_chart(category_data)

with chart_col2:
    # Price range preferences
    price_data = user_price_range.value_counts()
    st.markdown(f"<div style='background: {T['card_bg']}; padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);'><h5 style='color: {T['primary']}; margin-bottom: 15px;'>💰 Price Range Preferences</h5></div>", unsafe_allow_html=True)
    st.bar_chart(price_data)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------
# Session-Based Recommendations
# -------------------------
st.markdown("""
<div class="section fade-in">
    <h3>🕒 Session-Based Recommendations</h3>
    <p style="text-align: center; margin-bottom: 20px;">Recommendations based on your current browsing session</p>
""", unsafe_allow_html=True)

# Simulate session data
session_views = products_df.sample(5, random_state=42).copy()
session_recs = products_df.sample(6, random_state=43).copy()

st.markdown(f"<div class='fade-in' style='margin-bottom: 15px;'><h5 style='color: {T['primary']};'>👀 Recently Viewed</h5></div>", unsafe_allow_html=True)

session_html = "<div style='display:flex; gap:10px; margin-bottom:20px; overflow-x: auto;'>"
for _, row in session_views.iterrows():
    session_html += f"""
    <div class='card' style='width:180px; flex-shrink: 0;'>
        <img src="{row['ImageURL']}" width="180" class="product-image" />
        <div class="product-name" style="font-size: 14px;">{row['Description'][:30]}...</div>
        <div class="small-muted">{row['Category']}</div>
    </div>
    """
session_html += "</div>"
st.components.v1.html(session_html, height=200)

st.markdown(f"<div class='fade-in' style='margin-bottom: 15px;'><h5 style='color: {T['primary']};'>💡 Because You Viewed These</h5></div>", unsafe_allow_html=True)

session_rec_html = "<div style='display:flex; gap:10px; overflow-x: auto;'>"
for _, row in session_recs.iterrows():
    session_rec_html += f"""
    <div class='card' style='width:180px; flex-shrink: 0;'>
        <img src="{row['ImageURL']}" width="180" class="product-image" />
        <div class="product-name" style="font-size: 14px;">{row['Description'][:30]}...</div>
        <div class="small-muted">{row['Category']} • ₹{row['Price']}</div>
        <div class="rating">{'★'*int(round(row['Rating']))}</div>
    </div>
    """
session_rec_html += "</div>"
st.components.v1.html(session_rec_html, height=200)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------
# Recommendation Section
# -------------------------
st.markdown("""
<div class="section fade-in">
    <h3>🎯 Get Personalized Recommendations</h3>
""", unsafe_allow_html=True)
if st.button("🔮 Generate Recommendations"):
    with st.spinner(""):
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div class="loading-spinner"></div>
            <strong style="color: """ + T['primary'] + """;">🔍 Analyzing your preferences and generating personalized recommendations...</strong>
        </div>
        """, unsafe_allow_html=True)
        import time
        time.sleep(1)  # Simulate processing time
        recs = fetch_recommendations(user_id, top_n)
    if not recs:
        st.warning("No recommendations returned by API.")
    else:
        # Map rec codes to product rows
        rec_rows = products_df[products_df["StockCode"].isin(recs)].copy()
        # Add predicted price column
        rec_rows["PredictedPrice"] = rec_rows["Price"].apply(price_predictor)
        rec_rows = rec_rows.sort_values("Rating", ascending=False)

        st.markdown(f"<div class='fade-in' style='margin-bottom: 20px;'><h3>🎉 Top {len(rec_rows)} Recommendations for User {user_id}</h3></div>", unsafe_allow_html=True)
        # show recommendations as grid
        for idx, row in rec_rows.iterrows():
            card_html = f"""
            <div class='card fade-in' style='display:flex; gap:14px; align-items:center; margin-bottom: 20px;'>
                <img src="{row['ImageURL']}" width="140" class="product-image" />
                <div style="flex:1;">
                    <div class='product-name'>{row['Description']}</div>
                    <div class='small-muted'>{row['Category']} • ID: {row['StockCode']}</div>
                    <div style="margin-top:8px;">
                        <span class='price'>₹{row['Price']}</span>
                        &nbsp;&nbsp;<span class="rating">{'★'*int(round(row['Rating']))}</span>
                        &nbsp;&nbsp;<span class='small-muted'>({row['Rating']}/5)</span>
                    </div>
                    <div style="margin-top:8px;">
                        <strong style="color: {T['primary']};">Predicted Price:</strong> <span class='price'>₹{row['PredictedPrice']}</span>
                    </div>
                    <div style="margin-top:8px;">
                        <strong style="color: {T['secondary']};">Why Recommended:</strong>
                        <p style="color: {T['text']}; margin: 5px 0; font-size: 14px;">
                            Based on your preference for {user_categories.index[0] if len(user_categories) > 0 else 'similar products'} and price range around ₹{int(user_purchases['Price'].mean())}, this {row['Category'].lower()} item matches your shopping profile with a {row['Rating']}/5 rating.
                        </p>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            # Similar products rows
            sim_prods = similar_products(products_df, row["StockCode"], top_k=4)
            if sim_prods:
                st.markdown(f"<div class='fade-in' style='margin-top: 15px;'><h5 style='color: {T['primary']};'>🔗 Similar Products</h5></div>", unsafe_allow_html=True)
                sim_html = "<div style='display:flex; gap:8px; margin-top:8px; overflow-x: auto;'>"
                for sp in sim_prods:
                    sim_html += f"""
                    <div class='card fade-in' style='width:150px; flex-shrink: 0;'>
                        <img src="{sp['ImageURL']}" width="150" class="product-image" />
                        <div class="product-name" style="font-size: 14px;">{sp['Description']}</div>
                        <div class="small-muted">₹{sp['Price']} • {sp['Rating']}/5</div>
                    </div>
                    """
                sim_html += "</div>"
                st.components.v1.html(sim_html, height=180)

        st.markdown(f"""
        <div class="fade-in" style="text-align: center; padding: 20px; background: {T['card_bg']}; border-radius: 15px; backdrop-filter: blur(10px); margin-top: 20px;">
            <h4 style="color: {T['primary']}; margin-bottom: 10px;">🎊 Recommendations Generated Successfully!</h4>
            <p style="color: {T['text']}; margin: 0;">Enjoy exploring these personalized picks tailored just for you.</p>
        </div>
        <script>
            // Trigger confetti effect
            for (let i = 0; i < 50; i++) {{
                setTimeout(() => {{
                    const confetti = document.createElement('div');
                    confetti.className = 'confetti';
                    confetti.style.left = Math.random() * 100 + '%';
                    confetti.style.animationDelay = Math.random() * 3 + 's';
                    document.body.appendChild(confetti);
                    setTimeout(() => document.body.removeChild(confetti), 3000);
                }}, i * 50);
            }}
        </script>
        """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Footer
# -------------------------
st.markdown(f"""
<div class="footer">
    <h4>🚀 About ShopSense</h4>
    <p>ShopSense is an AI-powered product recommendation platform that helps users discover personalized products based on their preferences. Built with cutting-edge machine learning algorithms and modern web technologies.</p>
    <p style="margin-top: 10px; font-size: 14px; opacity: 0.7;">To deploy, set the <code>API_URL</code> in Streamlit secrets to your hosted FastAPI endpoint. Images are placeholders by default.</p>
</div>
""", unsafe_allow_html=True)
