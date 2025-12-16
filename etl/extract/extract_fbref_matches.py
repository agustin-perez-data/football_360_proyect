import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://fbref.com/en/comps/9/2011-2012/2011-2012-Premier-League-Stats"
OUTPUT_PATH = Path("data/raw/fbref/epl_2011_2012_team_stats.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def main():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    # Tabla de stats por equipo (incluye posesión)
    table = soup.find("table", {"id": "stats_squads_standard_for"})

    df = pd.read_html(str(table))[0]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"FBref team stats guardados en {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
