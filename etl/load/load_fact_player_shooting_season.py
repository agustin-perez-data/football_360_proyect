from load_csv import load_csv

CSV_PATH = "data/processed/shots/epl_2011_2012_player_shooting.csv"

load_csv(
    CSV_PATH,
    "fact_player_shooting_season",
    if_exists="replace"
)
