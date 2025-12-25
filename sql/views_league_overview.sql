CREATE OR REPLACE VIEW vw_league_kpis AS
SELECT
    season,
    COUNT(*)                     AS total_matches,
    SUM(home_goals + away_goals) AS total_goals,
    ROUND(
        SUM(home_goals + away_goals)::numeric / COUNT(*),
        2
    ) AS avg_goals_per_match
FROM fact_matches
GROUP BY season;


CREATE OR REPLACE VIEW vw_match_results_distribution AS
SELECT
    season,
    result,
    COUNT(*) AS matches
FROM fact_matches
GROUP BY season, result;


CREATE OR REPLACE VIEW vw_goals_by_date AS
SELECT
    season,
    date,
    SUM(home_goals + away_goals) AS total_goals
FROM fact_matches
GROUP BY season, date
ORDER BY date;


CREATE OR REPLACE VIEW vw_team_goals AS
SELECT
    season,
    team,
    SUM(goals) AS total_goals
FROM (
    SELECT season, home_team AS team, home_goals AS goals
    FROM fact_matches
    UNION ALL
    SELECT season, away_team AS team, away_goals AS goals
    FROM fact_matches
) t
GROUP BY season, team;
