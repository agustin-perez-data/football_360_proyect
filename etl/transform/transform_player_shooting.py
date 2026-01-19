import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/fbref/epl_2011_2012_player_shooting.csv")
OUTPUT_PATH = Path("data/processed/shots/epl_2011_2012_player_shooting.csv")

SEASON = "2011-2012"


def main():
    df = pd.read_csv(
        INPUT_PATH,
        sep=";",
        encoding="utf-8"
    )

    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\ufeff", "", regex=False)
    )

    df = df.rename(columns={
        "Player": "player",
        "Squad": "team",
        "90s": "minutes_90s",
        "Gls": "goals",
        "Sh": "shots",
        "SoT": "shots_on_target",
        "SoT%": "shots_on_target_pct",
        "Sh/90": "shots_per_90",
        "SoT/90": "shots_on_target_per_90",
        "G/Sh": "goals_per_shot",
        "G/SoT": "goals_per_shot_on_target",
        "Dist": "avg_shot_distance",
        "PK": "penalties_scored",
        "PKatt": "penalties_attempted"
    })

    if "shots_on_target_pct" not in df.columns:
        raise ValueError(f"Columnas detectadas: {df.columns.tolist()}")

    # Limpiar %
    df["shots_on_target_pct"] = (
        df["shots_on_target_pct"]
        .astype(str)
        .str.replace("%", "")
    )

    numeric_cols = [
        "minutes_90s",
        "goals",
        "shots",
        "shots_on_target",
        "shots_on_target_pct",
        "shots_per_90",
        "shots_on_target_per_90",
        "goals_per_shot",
        "goals_per_shot_on_target",
        "avg_shot_distance",
        "penalties_scored",
        "penalties_attempted"
    ]

    df[numeric_cols] = df[numeric_cols].apply(
        pd.to_numeric, errors="coerce"
    )

    df["season"] = SEASON

    df = df[[
        "player",
        "team",
        "season",
        "minutes_90s",
        "goals",
        "shots",
        "shots_on_target",
        "shots_on_target_pct",
        "shots_per_90",
        "shots_on_target_per_90",
        "goals_per_shot",
        "goals_per_shot_on_target",
        "avg_shot_distance",
        "penalties_scored",
        "penalties_attempted"
    ]]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Shooting stats transformados → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
