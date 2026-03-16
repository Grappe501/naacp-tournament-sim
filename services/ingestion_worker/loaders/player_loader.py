from sqlalchemy import text
from packages.db.engine import engine


def upsert_players(records: list[dict]) -> None:
    sql = text(
        '''
        INSERT INTO players (team_id, full_name, position, class_year)
        SELECT t.id, :full_name, :position, :class_year
        FROM teams t
        WHERE t.slug = :team_slug
        ON CONFLICT DO NOTHING
        '''
    )

    with engine.begin() as conn:
        for record in records:
            conn.execute(
                sql,
                {
                    "team_slug": f"espn-{record['team_external_id']}",
                    "full_name": record["full_name"],
                    "position": record["position"],
                    "class_year": record["class_year"],
                },
            )
