from fastapi import FastAPI
import pickle, os, numpy as np

app = FastAPI()

MODEL_PATH = "models/recommender.pkl"
model = pickle.load(open(MODEL_PATH, "rb")) if os.path.exists(MODEL_PATH) else None

@app.get("/recommend/{user_id}")
def recommend(user_id: int, n: int = 10):
    if model is None:
        return {"error": "Model not trained."}

    users = model["users"]
    if user_id not in users:
        return {"error": "User not found"}

    idx = users.index(user_id)

    # similarity vector of the current user
    sim = model["similarity"][idx]

    # Get top similar users (excluding the user itself)
    top_sim_users = np.argsort(sim)[-n-1:-1][::-1]

    # load user-item matrix
    import pandas as pd
    uif = pd.read_csv("data/processed/user_item_matrix.csv")

    mat = uif.iloc[:, 1:].values
    product_ids = list(uif.columns[1:])

    recommended = set()

    # For each similar user, pick their top-rated items
    for u in top_sim_users:
        user_row = mat[u]
        top_items = np.where(user_row > 0)[0]  # items they interacted with
        for item_idx in top_items:
            recommended.add(product_ids[item_idx])

    # return only top-N unique items
    recommended = list(recommended)[:n]

    return {
        "user": user_id,
        "top_n": n,
        "recommendations": recommended
    }
