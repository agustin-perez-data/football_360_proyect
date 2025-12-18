import pandas as pd
from db import get_engine

engine = get_engine()

matches = pd.read_csv("data/processed/matches/epl_2011_2012_matches.csv")
players = pd.read_csv("data/processed/players/epl_2011_2012_player_stats.csv")

teams = pd.concat([
    matches[["home_team"]].rename(columns={"home_team": "team"}),
    matches[["away_team"]].rename(columns={"away_team": "team"}),
    players[["team"]]
]).drop_duplicates()

teams = teams.rename(columns={"team": "team_id"})

teams.to_sql(
    "dim_team",
    engine,
    if_exists="replace",
    index=False
)

print("dim_team loaded")
