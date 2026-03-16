from sqlalchemy import text
from packages.db.engine import engine


def upsert_player_game_logs(records):

    sql = text(
        '''
        INSERT INTO player_game_logs (
            player_id,
            game_id,
            minutes,
            points,
            rebounds,
            assists,
            steals,
            blocks,
            turnovers,
            fouls
        )
        SELECT
            p.id,
            :game_id,
            :minutes,
            :points,
            :rebounds,
            :assists,
            :steals,
            :blocks,
            :turnovers,
            :fouls
        FROM players p
        WHERE p.external_id = :external_player_id
        ON CONFLICT DO NOTHING
        '''
    )

    with engine.begin() as conn:

        for record in records:

            conn.execute(sql, record)
