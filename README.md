# Football 360 Project

A lightweight end-to-end ETL + analytics stack for English Premier League 2011–2012 data. It loads processed CSVs into Postgres, creates analytical views, and lets you explore metrics in Metabase.

**Stack**
- Docker Compose: orchestrates `Postgres`, `Metabase`, and an `ETL` runner
- Python 3.11: ETL scripts with `pandas` + `sqlalchemy`
- Postgres 15: data warehouse (facts + dims + views)
- Metabase: fast, friendly BI UI

**Prerequisites**
- Docker Desktop (Windows/macOS/Linux) and Docker Compose
- Optional: Python 3.11 if you plan to run ETL locally instead of in the container

**Quick Start (Docker-first)**
- Starts the full stack, loads tables, creates views, and opens Metabase.

0) Configure environment
	   - Copy the example and set values:
		   ```bash
		   cp .env.example .env
		   # Edit .env to set secure values
		   ```
	 - Services:
		 - Postgres on `localhost:5432` (db: `football`, user/pass: `football`)
		 - Metabase on `http://localhost:3000`
		 - ETL runner container (`football_etl`) with Python + dependencies

2) Verify database connectivity (optional but recommended)
	 - Run the helper from the ETL container:
		1) Start services (local dev)
		   - In the project root, run:
			   ```bash
			   docker compose up -d
			   ```
		   - Services:
			   - Postgres on `localhost:5432` (db/user/password from `.env`)
			   - Metabase on `http://localhost:3000`
			   - ETL runner container (`football_etl`) with Python + dependencies

		2) Verify database connectivity (optional but recommended)
		   - Run the helper from the ETL container:
			   ```bash
			   docker exec football_etl python etl/load/test_db_connection.py
			   ```
			   - Expected output: `(1,)`
		 - [etl/load/load_dim_player.py](etl/load/load_dim_player.py)
		3) Load data into Postgres (run each)
		   - These read from `data/processed/**` and write to Postgres tables.
		   - Execute inside the ETL container:
			   ```bash
			   docker exec football_etl python etl/load/load_dim_team.py
			   docker exec football_etl python etl/load/load_dim_season.py
			   docker exec football_etl python etl/load/load_dim_player.py
			   docker exec football_etl python etl/load/load_fact_matches.py
			   docker exec football_etl python etl/load/load_fact_player_season.py
			   docker exec football_etl python etl/load/load_fact_player_shooting_season.py
			   ```
		   - Scripts:
			   - [etl/load/load_dim_team.py](etl/load/load_dim_team.py)
			   - [etl/load/load_dim_season.py](etl/load/load_dim_season.py)
			   - [etl/load/load_dim_player.py](etl/load/load_dim_player.py)
			   - [etl/load/load_fact_matches.py](etl/load/load_fact_matches.py)
			   - [etl/load/load_fact_player_season.py](etl/load/load_fact_player_season.py)
			   - [etl/load/load_fact_player_shooting_season.py](etl/load/load_fact_player_shooting_season.py)
		 - [etl/load/load_fact_player_season.py](etl/load/load_fact_player_season.py)
		4) Create analytical views
		   - From the Postgres container (the `sql` folder is mounted there):
			   ```bash
			   # Use the password from .env
			   docker exec football_db bash -lc "export PGPASSWORD=$POSTGRES_PASSWORD; psql -U $POSTGRES_USER -d $POSTGRES_DB -f /sql/views.sql"
			   ```
		   - Views file: [sql/views.sql](sql/views.sql)
		   - Additional view snippets are available:
			   - [sql/views_league_overview.sql](sql/views_league_overview.sql)
			   - [sql/views_player_stats.sql](sql/views_player_stats.sql)
			   - [sql/views_team_performance.sql](sql/views_team_performance.sql)
		 - [sql/views_league_overview.sql](sql/views_league_overview.sql)
		 - [sql/views_player_stats.sql](sql/views_player_stats.sql)
		 - [sql/views_team_performance.sql](sql/views_team_performance.sql)

5) Explore in Metabase
	 - Open `http://localhost:3000` and complete the Metabase setup wizard.
	 - Add a new database in Metabase:
		 - Type: Postgres
		 - Host: `postgres` (container DNS) or `host.docker.internal` if preferred
		 - Port: `5432`
				$env:POSTGRES_DB = "<your_db>"
				$env:POSTGRES_USER = "<your_user>"
				$env:POSTGRES_PASSWORD = "<your_password>"
	 - Start creating questions and dashboards. You should see the tables `fact_*`, `dim_*`, and views like `vw_*`.

**Optional: Run ETL locally (without ETL container)**
- If you prefer running scripts on your host Python:
	1) Ensure Postgres from Docker is up (`docker compose up -d`).
	2) Install Python packages:
		 ```bash
		 python -m pip install -r requirements.txt
		 ```
	3) Set environment variables (Windows PowerShell example):
		```powershell
		$env:POSTGRES_DB = "<your_db>"
		$env:POSTGRES_USER = "<your_user>"
		$env:POSTGRES_PASSWORD = "<your_password>"
		$env:POSTGRES_HOST = "localhost"
		$env:POSTGRES_PORT = "5432"
		```
	4) Run the same scripts from your host:
		 ```bash
		 python etl/load/test_db_connection.py
		 python etl/load/load_dim_team.py
		 python etl/load/load_dim_season.py
		 python etl/load/load_dim_player.py
		 python etl/load/load_fact_matches.py
		 python etl/load/load_fact_player_season.py
		 python etl/load/load_fact_player_shooting_season.py
		 ```

**Project Layout**
- Data
	- [data/processed/matches/epl_2011_2012_matches.csv](data/processed/matches/epl_2011_2012_matches.csv)
	- [data/processed/players/epl_2011_2012_player_stats.csv](data/processed/players/epl_2011_2012_player_stats.csv)
	- [data/processed/shots/epl_2011_2012_player_shooting.csv](data/processed/shots/epl_2011_2012_player_shooting.csv)
- ETL
	- Load helpers: [etl/load/load_csv.py](etl/load/load_csv.py), [etl/load/db.py](etl/load/db.py)
	- Load scripts: see list above
	- Optional extract/transform stubs: [etl/extract/extract_fbref_matches.py](etl/extract/extract_fbref_matches.py), [etl/transform/](etl/transform)
- SQL views: [sql/](sql)

**Common Commands**
- Stop stack: `docker compose down`
- Restart stack: `docker compose down && docker compose up -d`
- Shell into ETL container: `docker exec -it football_etl bash`
- psql inside Postgres: `docker exec -it football_db bash -lc "psql -U $POSTGRES_USER -d $POSTGRES_DB"`

		**Production (secrets)**
		 - Use Docker secrets for passwords with an override file:
			1) Create secrets files (not committed):
				- `secrets/postgres_password.txt`
				- `secrets/metabase_db_pass.txt`
			2) Start with overrides:
				```bash
				docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
				```
			- In prod, Postgres reads `POSTGRES_PASSWORD_FILE`; Metabase will read `MB_DB_PASS` from the secret if present, otherwise from `.env`.
**Troubleshooting**
- Metabase can’t connect to Postgres:
	- Ensure Postgres is up: `docker ps` should list `football_db`.
	- Use host `postgres` from Metabase (containers share a network). If using host networking, try `localhost` or `host.docker.internal`.
- Permission or auth errors:
	- Confirm credentials from `.env` (user, password, db).
- Views not found:
	- Re-run: `docker exec football_db bash -lc "export PGPASSWORD=$POSTGRES_PASSWORD; psql -U $POSTGRES_USER -d $POSTGRES_DB -f /sql/views.sql"`
- Fresh start:
	- `docker compose down -v` to remove volumes, then `docker compose up -d`.

**License**
- Educational/demo use. Data belongs to original sources cited in the `data/raw/` folder.

