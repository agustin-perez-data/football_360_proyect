import pandas as pd
from pathlib import Path

URL = "https://www.football-data.co.uk/mmz4281/1112/E0.csv"
OUTPUT_PATH = Path("data/raw/football_data/epl_2011_2012.csv")

def main():
    df = pd.read_csv(URL)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print("Football-data descargado correctamente")

if __name__ == "__main__":
    main()
