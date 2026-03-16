-- Core database schema

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT,
    conference TEXT
);

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT,
    team_id INT REFERENCES teams(id)
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    home_team INT REFERENCES teams(id),
    away_team INT REFERENCES teams(id),
    game_date DATE
);
