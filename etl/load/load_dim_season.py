import pandas as pd
from db import get_engine

engine = get_engine()

df = pd.read_csv("data/processed/matches/epl_2011_2012_matches.csv")

dim_season = (
    df[["season"]]
    .drop_duplicates()
    .rename(columns={"season": "season_id"})
)

dim_season.to_sql(
    "dim_season",
    engine,
    if_exists="replace",
    index=False
)

print("dim_season loaded")
