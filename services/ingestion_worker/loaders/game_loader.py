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
