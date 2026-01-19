import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/fbref/epl_2011_2012_player_stats.csv")
OUTPUT_PATH = Path("data/processed/players/epl_2011_2012_player_stats.csv")

SEASON = "2011-2012"


def main():
    df = pd.read_csv(
    INPUT_PATH,
    sep=";",
    engine="python",
    encoding="utf-8",
    on_bad_lines="skip")


    df = df[~df["Player"].str.contains("League", na=False)]

    df = df.rename(columns={
        "Player": "player",
        "Squad": "team",
        "MP": "matches_played",
        "Starts": "starts",
        "Min": "minutes",
        "90s": "minutes_90s",
        "Gls": "goals",
        "Ast": "assists",
        "G+A": "goals_assists",
        "G-PK": "non_penalty_goals",
        "PK": "penalties_scored",
        "PKatt": "penalties_attempted",
        "CrdY": "yellow_cards",
        "CrdR": "red_cards",
        "G+A-PK": "goals_assists_non_penalty_per_90"
    })

    numeric_cols = [
        "matches_played", "starts", "minutes", "minutes_90s",
        "goals", "assists", "goals_assists", "non_penalty_goals",
        "penalties_scored", "penalties_attempted",
        "yellow_cards", "red_cards",
        "goals_assists_non_penalty_per_90"
    ]

    df[numeric_cols] = df[numeric_cols].apply(
        pd.to_numeric, errors="coerce"
    )

    df["season"] = SEASON

    df = df[[
        "player",
        "team",
        "season",
        "matches_played",
        "starts",
        "minutes",
        "minutes_90s",
        "goals",
        "assists",
        "goals_assists",
        "non_penalty_goals",
        "penalties_scored",
        "penalties_attempted",
        "yellow_cards",
        "red_cards",
        "goals_assists_non_penalty_per_90"
    ]]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Player stats transformados → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
