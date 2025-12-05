
import pandas as pd, os, pickle
from sklearn.metrics.pairwise import cosine_similarity
def train():
    # Prefer processed pivot
    ppath = 'data/processed/user_item_matrix.csv'
    if os.path.exists(ppath):
        uif = pd.read_csv(ppath)
        users = uif.iloc[:,0].tolist()
        mat = uif.iloc[:,1:].values
        products = list(uif.columns)[1:]
    else:
        df = pd.read_csv('data/raw/interactions.csv')
        pivot = df.pivot_table(index='user_id', columns='product_id', values='rating', aggfunc='sum', fill_value=0)
        users = pivot.index.tolist()
        mat = pivot.values
        products = pivot.columns.tolist()
    sim = cosine_similarity(mat)
    model = {'users': users, 'products': products, 'similarity': sim, 'matrix_shape': mat.shape}
    os.makedirs('models', exist_ok=True)
    with open('models/recommender.pkl','wb') as f: pickle.dump(model,f)
    print('Saved models/recommender.pkl')
if __name__ == '__main__':
    train()
