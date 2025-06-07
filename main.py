import streamlit as st
from app_view import show_app_view
from compare_view import show_compare_view

st.set_page_config(page_title="Urban Consumption Dashboard", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to:", ["Single Country View", "Compare Countries"])

if page == "Single Country View":
    show_app_view()
elif page == "Compare Countries":
    show_compare_view()
