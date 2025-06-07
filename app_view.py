import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def show_app_view():
    engine = create_engine("sqlite:///consumption.db")

    @st.cache_data
    def load_options():
        df = pd.read_sql("SELECT DISTINCT unit, country, coicop FROM consumption", engine)
        return sorted(df["unit"].dropna().unique()), sorted(df["country"].dropna().unique()), sorted(df["coicop"].dropna().unique())

    units, countries, coicops = load_options()

    st.title("📊 Single Country: Household Expenditure by Urbanisation")
    unit = st.selectbox("Select unit:", units)
    country = st.selectbox("Select country:", countries)
    coicop = st.selectbox("Select COICOP category:", coicops)

    query = """
        SELECT * FROM consumption
        WHERE unit = :unit AND country = :country AND coicop = :coicop
    """
    df = pd.read_sql(query, engine, params={"unit": unit, "country": country, "coicop": coicop})

    if df.empty:
        st.warning("No data available for the selected options.")
    else:
        df = df.sort_values(by="year")
        fig, ax = plt.subplots()
        for urb in df["urbanisation"].unique():
            df_urb = df[df["urbanisation"] == urb]
            ax.plot(df_urb["year"], df_urb["value"], marker='o', label=urb)
        ax.set_title(f"{coicop} in {country} ({unit})")
        ax.set_xlabel("Year")
        ax.set_ylabel("Value")
        ax.legend(title="Urbanisation")
        ax.grid(True)
        st.pyplot(fig)
