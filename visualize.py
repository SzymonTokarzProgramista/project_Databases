import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy import text

# Łączymy się z bazą
engine = create_engine("sqlite:///consumption.db")

# Wczytaj dane do Pandas
df = pd.read_sql("SELECT * FROM consumption", engine)

# Przykład: wydatki na żywność (CP01) w różnych typach obszarów w Polsce
filtered = df[
    (df["country"] == "PL") &
    (df["coicop"] == "CP01") &
    (df["unit"] == "PM")  # np. procent udziału
]

# Sortujemy po roku
filtered = filtered.sort_values(by="year")

print("[DEBUG] Przykładowe dane:")
print(df.head(10))

print("[DEBUG] Dostępne kraje:", df["country"].unique())
print("[DEBUG] Dostępne urbanisation:", df["urbanisation"].unique())
print("[DEBUG] Dostępne coicop:", df["coicop"].unique())
print("[DEBUG] Dostępne unit:", df["unit"].unique())



# Wykres
plt.figure(figsize=(10, 6))
sns.lineplot(data=filtered, x="year", y="value", hue="urbanisation", marker="o")

plt.title("Udział wydatków na żywność (CP01) w Polsce wg typu urbanizacji")
plt.xlabel("Rok")
plt.ylabel("Udział (%)")
plt.legend(title="Typ obszaru")
plt.grid(True)
plt.tight_layout()
plt.show()
