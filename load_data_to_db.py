import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ConsumptionRecord

def load_data_to_db(tsv_path, db_path='sqlite:///consumption.db'):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(tsv_path, 'r', encoding='utf-8') as f:
        # Parsujemy nagłówki: 1988, 1994, ...
        header = f.readline()
        header_parts = header.strip().split('\t')
        years = [int(year.strip()) for year in header_parts[1:]]  # bez TIME_PERIOD

        for line in f:
            line = line.strip()
            if not line:
                continue

            # Rozdzielamy pierwsze 5 pól (część metadanych)
            try:
                meta_part, *data_part = line.split('\t', maxsplit=1)
                freq, deg_urb, coicop, unit, geo = meta_part.split(',', maxsplit=4)
            except ValueError:
                continue  # źle sformatowana linia

            # Dalsze dane: liczby rozdzielone tabami/spacjami
            if not data_part:
                continue

            values = data_part[0].split()  # domyślnie rozdziela spacje/taby

            for i, val in enumerate(values):
                if i >= len(years):
                    continue  # więcej wartości niż lat

                val = val.strip()
                if val in (":", "", " "):
                    continue

                try:
                    value = float(val.split()[0])  # np. 123.4 u
                except ValueError:
                    continue

                record = ConsumptionRecord(
                    unit=unit.strip(),
                    country=geo.strip(),
                    urbanisation=deg_urb.strip(),
                    coicop=coicop.strip(),
                    year=years[i],
                    value=value
                )
                session.add(record)

    session.commit()
    print("[OK] Wszystkie dane zostały poprawnie załadowane.")
