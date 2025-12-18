CREATE OR REPLACE VIEW vw_top_scorers AS
SELECT
    season,
    player,
    team,
    goals
FROM fact_player_season
ORDER BY season, goals DESC;

CREATE OR REPLACE VIEW vw_goals_per_90 AS
SELECT
    season,
    player,
    team,
    ROUND(
        (goals::numeric / NULLIF(minutes_90s, 0)::numeric),
        2
    ) AS goals_per_90,
    matches_played
FROM fact_player_season
WHERE matches_played >= 10;

CREATE OR REPLACE VIEW vw_shooting_efficiency AS
SELECT
    season,
    player,
    team,
    ROUND(goals_per_shot_on_target::numeric, 2) AS goals_per_shot_on_target,
    shots_on_target_per_90
FROM fact_player_shooting_season
WHERE minutes_90s >= 10;

CREATE OR REPLACE VIEW vw_goal_contributions AS
SELECT
    season,
    player,
    team,
    goals,
    assists,
    goals_assists
FROM fact_player_season
ORDER BY goals_assists DESC;

CREATE OR REPLACE VIEW vw_discipline AS
SELECT
    season,
    player,
    team,
    yellow_cards,
    red_cards,
    (yellow_cards + red_cards * 3) AS discipline_score
FROM fact_player_season;


CREATE OR REPLACE VIEW vw_league_table AS
WITH points AS (
    SELECT
        season,
        home_team AS team,
        CASE
            WHEN result = 'H' THEN 3
            WHEN result = 'D' THEN 1
            ELSE 0
        END AS pts
    FROM fact_matches

    UNION ALL

    SELECT
        season,
        away_team AS team,
        CASE
            WHEN result = 'A' THEN 3
            WHEN result = 'D' THEN 1
            ELSE 0
        END AS pts
    FROM fact_matches
)
SELECT
    season,
    team,
    SUM(pts) AS points
FROM points
GROUP BY season, team
ORDER BY season, points DESC;
