CREATE OR REPLACE VIEW vw_team_performance AS
SELECT
    season,
    team,
    COUNT(*) AS matches_played,
    SUM(wins) AS wins,
    SUM(draws) AS draws,
    SUM(losses) AS losses,
    SUM(goals_for) AS goals_for,
    SUM(goals_against) AS goals_against,
    SUM(goals_for - goals_against) AS goal_difference,
    SUM(points) AS points
FROM (
    -- Home matches
    SELECT
        season,
        home_team AS team,
        1 AS matches,
        CASE WHEN home_goals > away_goals THEN 1 ELSE 0 END AS wins,
        CASE WHEN home_goals = away_goals THEN 1 ELSE 0 END AS draws,
        CASE WHEN home_goals < away_goals THEN 1 ELSE 0 END AS losses,
        home_goals AS goals_for,
        away_goals AS goals_against,
        CASE
            WHEN home_goals > away_goals THEN 3
            WHEN home_goals = away_goals THEN 1
            ELSE 0
        END AS points
    FROM fact_matches

    UNION ALL

    -- Away matches
    SELECT
        season,
        away_team AS team,
        1 AS matches,
        CASE WHEN away_goals > home_goals THEN 1 ELSE 0 END AS wins,
        CASE WHEN away_goals = home_goals THEN 1 ELSE 0 END AS draws,
        CASE WHEN away_goals < home_goals THEN 1 ELSE 0 END AS losses,
        away_goals AS goals_for,
        home_goals AS goals_against,
        CASE
            WHEN away_goals > home_goals THEN 3
            WHEN away_goals = home_goals THEN 1
            ELSE 0
        END AS points
    FROM fact_matches
) t
GROUP BY season, team;
