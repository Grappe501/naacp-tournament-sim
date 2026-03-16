CREATE TABLE IF NOT EXISTS players (

    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(id),
    full_name TEXT,
    position TEXT

);
