from load_csv import load_csv

CSV_PATH = "data/processed/matches/epl_2011_2012_matches.csv"

load_csv(
    CSV_PATH,
    "fact_matches",
    if_exists="replace"
)
