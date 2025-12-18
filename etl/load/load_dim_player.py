import pandas as pd
from db import get_engine

engine = get_engine()

players = pd.read_csv("data/processed/players/epl_2011_2012_player_stats.csv")

dim_player = (
    players[["player"]]
    .drop_duplicates()
    .rename(columns={"player": "player_id"})
)

dim_player.to_sql(
    "dim_player",
    engine,
    if_exists="replace",
    index=False
)

print("dim_player loaded")
