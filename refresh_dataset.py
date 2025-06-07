import os
import requests
import gzip
import shutil
from datetime import datetime

def download_urb_clcc_data(output_dir="data"):
    # Tworzymy folder, jeśli nie istnieje
    os.makedirs(output_dir, exist_ok=True)
    
    url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/hbs_str_t226?format=TSV&compressed=true"

    gz_path = os.path.join(output_dir, "urb_clcc.tsv.gz")
    tsv_path = os.path.join(output_dir, "urb_clcc.tsv")

    print("[INFO] Downloading latest urb_clcc.tsv.gz from Eurostat...")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(gz_path, "wb") as f:
            f.write(response.content)
        print("[INFO] File downloaded successfully.")

        # Rozpakowujemy .gz do .tsv
        with gzip.open(gz_path, 'rb') as f_in:
            with open(tsv_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        print(f"[INFO] File extracted to: {tsv_path}")

        # (Opcjonalnie) zapisujemy datę pobrania
        with open(os.path.join(output_dir, "last_download.txt"), "w") as f:
            f.write(f"Downloaded on: {datetime.utcnow().isoformat()} UTC")

        return tsv_path
    else:
        print(f"[ERROR] Failed to download file: {response.status_code}")
        return None
