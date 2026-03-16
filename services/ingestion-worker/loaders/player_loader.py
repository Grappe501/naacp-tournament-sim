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
