import pandas as pd
from db import get_engine

def load_csv(csv_path, table_name, if_exists="replace"):
    engine = get_engine()
    df = pd.read_csv(csv_path)

    df.to_sql(
        table_name,
        engine,
        if_exists=if_exists,
        index=False,
        method="multi",
        chunksize=1000
    )

    print(f"Loaded {len(df)} rows into {table_name}")
