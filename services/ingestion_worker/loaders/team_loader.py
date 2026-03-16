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
