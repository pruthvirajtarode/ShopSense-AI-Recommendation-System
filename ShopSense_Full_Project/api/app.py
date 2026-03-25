
from fastapi import FastAPI
import pickle

app = FastAPI()
model = pickle.load(open('models/als_model.pkl','rb'))

@app.get('/recommend/{user_id}')
def rec(user_id: int):
    return {'user': user_id, 'items': ['P001','P002','P003']}
