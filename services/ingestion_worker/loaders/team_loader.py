from sqlalchemy import text
from packages.db.engine import engine


def upsert_teams(records: list[dict]) -> None:
    sql = text(
        '''
        INSERT INTO teams (name, slug)
        VALUES (:name, :slug)
        ON CONFLICT (slug)
        DO UPDATE SET name = EXCLUDED.name
        '''
    )

    with engine.begin() as conn:
        for record in records:
            conn.execute(
                sql,
                {
                    "name": record["name"],
                    "slug": record["slug"],
                },
            )
