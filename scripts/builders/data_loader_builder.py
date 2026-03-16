from utils.file_utils import write_file

def build_data_loader():
    print("Building data loaders...")

    team_loader = """
from sqlalchemy import text
from packages.db.connection import engine

def upsert_teams(teams):
    with engine.begin() as conn:
        for team in teams:
            conn.execute(
                text(
                    '''
                    INSERT INTO teams (name, slug)
                    VALUES (:name, :slug)
                    ON CONFLICT (slug)
                    DO UPDATE SET name = EXCLUDED.name
                    '''
                ),
                {
                    "name": team.name,
                    "slug": f"espn-{team.external_id}",
                }
            )
"""

    player_loader = """
from sqlalchemy import text
from packages.db.connection import engine

def upsert_players(players):
    with engine.begin() as conn:
        for player in players:
            conn.execute(
                text(
                    '''
                    INSERT INTO players (team_id, full_name, position)
                    SELECT t.id, :full_name, :position
                    FROM teams t
                    WHERE t.slug = :team_slug
                    ON CONFLICT DO NOTHING
                    '''
                ),
                {
                    "team_slug": f"espn-{player.team_external_id}",
                    "full_name": player.full_name,
                    "position": player.position,
                }
            )
"""

    game_loader = """
from sqlalchemy import text
from packages.db.connection import engine

def upsert_games(games):
    with engine.begin() as conn:
        for game in games:
            conn.execute(
                text(
                    '''
                    INSERT INTO games (
                        season,
                        game_date,
                        home_team_id,
                        away_team_id,
                        neutral_site
                    )
                    SELECT
                        :season,
                        CAST(:game_date AS TIMESTAMP),
                        ht.id,
                        at.id,
                        :neutral_site
                    FROM teams ht, teams at
                    WHERE ht.slug = :home_slug
                      AND at.slug = :away_slug
                    ON CONFLICT DO NOTHING
                    '''
                ),
                {
                    "season": game.season,
                    "game_date": game.game_date,
                    "home_slug": f"espn-{game.home_team_external_id}",
                    "away_slug": f"espn-{game.away_team_external_id}",
                    "neutral_site": game.neutral_site,
                }
            )
"""

    write_file("services/ingestion-worker/loaders/team_loader.py", team_loader)
    write_file("services/ingestion-worker/loaders/player_loader.py", player_loader)
    write_file("services/ingestion-worker/loaders/game_loader.py", game_loader)