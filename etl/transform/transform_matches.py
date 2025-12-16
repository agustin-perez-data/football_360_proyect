import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/football_data/epl_2011_2012.csv")
OUTPUT_PATH = Path("data/processed/matches/epl_2011_2012_matches.csv")

SEASON = "2011-2012"


def main():
    df = pd.read_csv(INPUT_PATH)

    df = df[[
        "Date",
        "HomeTeam",
        "AwayTeam",
        "FTHG",
        "FTAG",
        "FTR"
    ]]

    df = df.rename(columns={
        "Date": "date",
        "HomeTeam": "home_team",
        "AwayTeam": "away_team",
        "FTHG": "home_goals",
        "FTAG": "away_goals",
        "FTR": "result"
    })

    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["season"] = SEASON

    df["match_id"] = (
        df["date"].dt.strftime("%Y%m%d") + "_" +
        df["home_team"].str.replace(" ", "_") + "_" +
        df["away_team"].str.replace(" ", "_")
    )

    df = df[[
        "match_id",
        "date",
        "season",
        "home_team",
        "away_team",
        "home_goals",
        "away_goals",
        "result"
    ]]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Matches transformados → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
