-- 1. Vista Base (Datos generales)
CREATE OR REPLACE VIEW vw_player_base AS
SELECT
    player,
    team,
    season,
    matches_played,
    starts,
    minutes,
    minutes_90s,
    goals,
    assists,
    goals_assists,
    non_penalty_goals,
    penalties_scored,
    penalties_attempted,
    yellow_cards,
    red_cards,
    goals_assists_non_penalty_per_90
FROM fact_player_season;

-- 2. Vista de Disparos (Shooting)
CREATE OR REPLACE VIEW vw_player_shooting AS
SELECT
    player,
    team,
    season,
    minutes_90s,
    goals                   AS shooting_goals,
    shots,
    shots_on_target,
    shots_on_target_pct,
    shots_per_90,
    shots_on_target_per_90,
    goals_per_shot,
    goals_per_shot_on_target,
    avg_shot_distance,
    penalties_scored        AS shooting_penalties_scored,
    penalties_attempted     AS shooting_penalties_attempted
FROM fact_player_shooting_season;

-- 3. Vista de Performance Completa (Join)

CREATE OR REPLACE VIEW vw_player_performance AS
SELECT
    b.player,
    b.team,
    b.season,

    -- Tiempo de juego
    b.matches_played,
    b.starts,
    b.minutes,
    b.minutes_90s,

    -- Producción
    b.goals,
    b.assists,
    b.goals_assists,
    b.non_penalty_goals,

    -- Métricas de Disparo (Shooting)
    s.shots,
    s.shots_on_target,
    s.shots_on_target_pct,
    s.shots_per_90,
    s.shots_on_target_per_90,
    s.goals_per_shot,
    s.goals_per_shot_on_target,
    s.avg_shot_distance,

    -- Disciplina
    b.yellow_cards,
    b.red_cards,

    -- Métricas Derivadas (Calculadas)
    ROUND(b.goals::numeric / NULLIF(b.matches_played, 0), 2) AS goals_per_match,
    ROUND(b.assists::numeric / NULLIF(b.matches_played, 0), 2) AS assists_per_match

FROM vw_player_base b
LEFT JOIN vw_player_shooting s
    ON b.player = s.player
    AND b.season = s.season
    AND b.team = s.team; 