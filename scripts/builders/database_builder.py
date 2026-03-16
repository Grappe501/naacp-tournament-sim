from utils.file_utils import write_file

def build_database():

    print("Building database schema...")

    schema = """

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT,
    conference TEXT
);

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(id),
    name TEXT
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    home_team INT,
    away_team INT,
    game_date DATE
);

"""

    write_file("packages/db/schema.sql", schema)