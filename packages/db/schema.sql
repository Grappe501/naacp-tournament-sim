CREATE TABLE IF NOT EXISTS conferences (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE,
    conference_id INT REFERENCES conferences(id),
    city TEXT,
    state TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    position TEXT,
    class_year TEXT,
    height TEXT,
    weight INT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    season INT NOT NULL,
    game_date DATE NOT NULL,
    home_team_id INT REFERENCES teams(id),
    away_team_id INT REFERENCES teams(id),
    neutral_site BOOLEAN NOT NULL DEFAULT FALSE,
    location TEXT,
    home_score INT,
    away_score INT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS player_game_stats (
    id SERIAL PRIMARY KEY,
    game_id INT REFERENCES games(id) ON DELETE CASCADE,
    player_id INT REFERENCES players(id) ON DELETE CASCADE,
    minutes NUMERIC(5,2),
    points INT,
    rebounds INT,
    assists INT,
    steals INT,
    blocks INT,
    turnovers INT,
    fouls INT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(game_id, player_id)
);

CREATE TABLE IF NOT EXISTS team_game_stats (
    id SERIAL PRIMARY KEY,
    game_id INT REFERENCES games(id) ON DELETE CASCADE,
    team_id INT REFERENCES teams(id) ON DELETE CASCADE,
    possessions NUMERIC(8,2),
    offensive_rating NUMERIC(8,2),
    defensive_rating NUMERIC(8,2),
    pace NUMERIC(8,2),
    fg_pct NUMERIC(6,3),
    three_pt_pct NUMERIC(6,3),
    ft_pct NUMERIC(6,3),
    turnovers INT,
    rebounds INT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(game_id, team_id)
);

CREATE TABLE IF NOT EXISTS tournament_games (
    id SERIAL PRIMARY KEY,
    season INT NOT NULL,
    round_name TEXT NOT NULL,
    region TEXT,
    seed_home INT,
    seed_away INT,
    game_id INT REFERENCES games(id),
    winner_team_id INT REFERENCES teams(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS simulation_runs (
    id SERIAL PRIMARY KEY,
    run_name TEXT NOT NULL,
    season INT NOT NULL,
    iterations INT NOT NULL,
    model_version TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS simulation_team_results (
    id SERIAL PRIMARY KEY,
    simulation_run_id INT REFERENCES simulation_runs(id) ON DELETE CASCADE,
    team_id INT REFERENCES teams(id) ON DELETE CASCADE,
    championship_wins INT NOT NULL DEFAULT 0,
    final_four_count INT NOT NULL DEFAULT 0,
    elite_eight_count INT NOT NULL DEFAULT 0,
    sweet_sixteen_count INT NOT NULL DEFAULT 0,
    round_of_32_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(simulation_run_id, team_id)
);
