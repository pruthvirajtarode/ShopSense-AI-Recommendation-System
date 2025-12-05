
import streamlit as st
import pickle

st.title("ShopSense — Smart Product Recommender")

model = pickle.load(open('models/als_model.pkl','rb'))

user_id = st.text_input("Enter Customer ID")

if st.button("Recommend"):
    st.write(["P001","P002","P003"])
