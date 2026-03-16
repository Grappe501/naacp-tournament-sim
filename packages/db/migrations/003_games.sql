CREATE TABLE IF NOT EXISTS games (

    id SERIAL PRIMARY KEY,
    season INT,
    game_date TIMESTAMP,
    home_team_id INT REFERENCES teams(id),
    away_team_id INT REFERENCES teams(id),
    neutral_site BOOLEAN

);
