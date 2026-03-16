from utils.file_utils import write_file

def build_schema():

    teams = """

CREATE TABLE IF NOT EXISTS teams (

    id SERIAL PRIMARY KEY,
    name TEXT,
    slug TEXT UNIQUE,
    conference TEXT

);

"""

    players = """

CREATE TABLE IF NOT EXISTS players (

    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(id),
    full_name TEXT,
    position TEXT

);

"""

    games = """

CREATE TABLE IF NOT EXISTS games (

    id SERIAL PRIMARY KEY,
    season INT,
    game_date TIMESTAMP,
    home_team_id INT REFERENCES teams(id),
    away_team_id INT REFERENCES teams(id),
    neutral_site BOOLEAN

);

"""

    write_file("packages/db/migrations/001_teams.sql", teams)
    write_file("packages/db/migrations/002_players.sql", players)
    write_file("packages/db/migrations/003_games.sql", games)