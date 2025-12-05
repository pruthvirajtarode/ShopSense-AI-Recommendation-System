
import pandas as pd
from scipy.sparse import csr_matrix
from implicit.als import AlternatingLeastSquares
import pickle

def train():
    df = pd.read_csv('data/processed/transactions.csv')
    df['Quantity'] = df['Quantity'].astype(float)

    users = df['CustomerID'].astype("category").cat.codes
    items = df['StockCode'].astype("category").cat.codes

    matrix = csr_matrix((df['Quantity'], (users, items)))
    model = AlternatingLeastSquares(factors=50)
    model.fit(matrix)

    pickle.dump(model, open('models/als_model.pkl','wb'))

if __name__ == '__main__':
    train()
