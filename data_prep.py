import os
from refresh_dataset import download_urb_clcc_data
from load_data_to_db import load_data_to_db

def main():
    print("=== Konsumpcja vs Urbanizacja (Eurostat: urb_clcc) ===")

    # Ścieżka do katalogu na dane
    data_dir = "data"

    # 1. Pobierz i rozpakuj plik TSV z Eurostatu
    tsv_path = download_urb_clcc_data(output_dir=data_dir)
    if not tsv_path:
        print("[ERROR] Nie udało się pobrać pliku. Zakończono.")
        return

    # 2. Ścieżka do bazy danych SQLite
    db_path = "sqlite:///consumption.db"

    # 3. Załaduj dane do bazy
    print("[INFO] Ładowanie danych do bazy...")
    load_data_to_db(tsv_path, db_path=db_path)
    print("[DONE] Gotowe.")

if __name__ == "__main__":
    main()
