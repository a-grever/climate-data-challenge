from pathlib import Path

import pandas as pd

from app.database import engine
from app.models import LandTemperatures

init_data_path = Path("/app/data/GlobalLandTemperaturesByCity.csv")
target_table = LandTemperatures.metadata.tables["land_temperatures"]

fieldnames = [
    "date",
    "average_temperature",
    "average_temperature_uncertainty",
    "city",
    "country",
    "latitude",
    "longitude",
]

if __name__ == "__main__":
    if not init_data_path.exists():
        raise RuntimeError("couldn't find 'GlobalLandTemperaturesByCity.csv' in data folder!")

    print("starting import...")
    csv_iterator = pd.read_csv(
        "./data/GlobalLandTemperaturesByCity.csv",
        names=fieldnames,
        header=0,
        delimiter=",",
        iterator=True,
        chunksize=100_000,
    )
    n_rows = 0
    for data_chunk in csv_iterator:
        data_chunk.to_sql(name=target_table.name, con=engine, if_exists="append", index=False)
        n_rows += data_chunk.shape[0]
        print(f"inserted {n_rows} rows into {target_table.name}")
