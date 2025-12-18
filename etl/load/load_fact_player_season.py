from load_csv import load_csv

CSV_PATH = "data/processed/players/epl_2011_2012_player_stats.csv"

load_csv(
    CSV_PATH,
    "fact_player_season",
    if_exists="replace"
)
