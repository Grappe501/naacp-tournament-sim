from sqlalchemy import text
from packages.db.engine import engine


def upsert_games(records: list[dict]) -> None:
    sql = text(
        '''
        INSERT INTO games (
            season,
            game_date,
            home_team_id,
            away_team_id,
            neutral_site,
            location
        )
        SELECT
            :season,
            CAST(:game_date AS TIMESTAMP),
            ht.id,
            at.id,
            :neutral_site,
            :location
        FROM teams ht, teams at
        WHERE ht.slug = :home_slug
          AND at.slug = :away_slug
        ON CONFLICT DO NOTHING
        '''
    )

    with engine.begin() as conn:
        for record in records:
            conn.execute(
                sql,
                {
                    "season": record["season"],
                    "game_date": record["game_date"],
                    "home_slug": f"espn-{record['home_team_external_id']}",
                    "away_slug": f"espn-{record['away_team_external_id']}",
                    "neutral_site": record["neutral_site"],
                    "location": record["location"],
                },
            )
