# project_Databases

# 🏙️ Urban Consumption Dashboard

A Streamlit-based dashboard for visualizing household consumption data by COICOP category, country, urbanization level, and unit. The data is loaded from Eurostat TSV files and stored in a local SQLite database.

## 📦 Requirements

Make sure you have Python 3.8+ installed. Then install required packages:

```bash
pip install -r requirements.txt
```


To load current dataset:

```bash
python data_prep.py
```

To run:

```bash
streamlit run main.py
```
