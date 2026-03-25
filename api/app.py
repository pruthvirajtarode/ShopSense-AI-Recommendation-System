import os
from fastapi import FastAPI
import pickle, numpy as np
import pandas as pd

app = FastAPI()

# Absolute paths for Vercel
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "recommender.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "user_item_matrix.csv")

model = pickle.load(open(MODEL_PATH, "rb")) if os.path.exists(MODEL_PATH) else None

@app.get("/")
def home():
    return {"message": "ShopSense AI Recommendation API is running", "model_loaded": model is not None}

@app.get("/recommend/{user_id}")
def recommend(user_id: int, n: int = 10):
    if model is None:
        return {"error": "Model not trained."}

    users = model["users"]
    if user_id not in users:
        return {"error": "User not found"}

    idx = users.index(user_id)
    sim = model["similarity"][idx]
    top_sim_users = np.argsort(sim)[-n-1:-1][::-1]

    uif = pd.read_csv(DATA_PATH)
    mat = uif.iloc[:, 1:].values
    product_ids = list(uif.columns[1:])

    recommended = set()
    for u in top_sim_users:
        user_row = mat[u]
        top_items = np.where(user_row > 0)[0]
        for item_idx in top_items:
            recommended.add(product_ids[item_idx])

    return {
        "user": user_id,
        "top_n": n,
        "recommendations": list(recommended)[:n]
    }

@app.get("/api/products")
def get_products():
    products_path = os.path.join(BASE_DIR, "data", "processed", "products.csv")
    if not os.path.exists(products_path):
        return []
    df = pd.read_csv(products_path)
    return df.to_dict("records")

@app.get("/api/categories")
def get_categories():
    products_path = os.path.join(BASE_DIR, "data", "processed", "products.csv")
    if not os.path.exists(products_path):
        return ["General"]
    df = pd.read_csv(products_path)
    return sorted(df["Category"].unique().tolist()) if "Category" in df.columns else ["General"]
