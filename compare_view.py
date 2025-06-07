import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Połączenie z bazą danych
engine = create_engine("sqlite:///consumption.db")

# Pobieranie opcji do wyboru
@st.cache_data
def load_options():
    df = pd.read_sql("SELECT DISTINCT unit, country, coicop FROM consumption", engine)
    return sorted(df["unit"].dropna().unique()), sorted(df["country"].dropna().unique()), sorted(df["coicop"].dropna().unique())

def show_compare_view():
    st.title("🌍 Country Comparison")

    units, countries, coicops = load_options()

    # Wybór opcji
    unit = st.selectbox("Select unit:", units)
    coicop = st.selectbox("Select COICOP category:", coicops)
    selected_countries = st.multiselect("Select countries to compare:", countries)

    if not selected_countries:
        st.warning("Please select at least one country.")
        return

    # Tworzenie dynamicznego zapytania z IN (...)
    placeholders = ", ".join([f":c{i}" for i in range(len(selected_countries))])
    query = f"""
        SELECT * FROM consumption
        WHERE unit = :unit AND coicop = :coicop AND country IN ({placeholders})
    """
    params = {"unit": unit, "coicop": coicop}
    params.update({f"c{i}": country for i, country in enumerate(selected_countries)})

    # Pobieranie danych
    df = pd.read_sql(query, engine, params=params)

    if df.empty:
        st.warning("No data found for selected countries.")
        return

    df = df.sort_values(by="year")

    # Rysowanie wykresu
    fig, ax = plt.subplots()
    for country in df["country"].unique():
        for urb in df["urbanisation"].unique():
            sub = df[(df["country"] == country) & (df["urbanisation"] == urb)]
            label = f"{country} ({urb})" if urb != ":" else f"{country}"
            ax.plot(sub["year"], sub["value"], marker='o', label=label)

    ax.set_title(f"{coicop} comparison ({unit})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    ax.grid(True)
    ax.legend(title="Country (Urbanisation)", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)
