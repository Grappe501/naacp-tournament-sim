from packages.db.connection import get_connection


def fetch_teams():

    sql = '''
    SELECT
        id,
        name
    FROM teams
    '''

    with get_connection() as conn:
        rows = conn.execute(sql).fetchall()

    return [
        {
            "team_id": r[0],
            "team_name": r[1]
        }
        for r in rows
    ]


def fetch_team_players(team_id):

    sql = '''
    SELECT
        id,
        full_name,
        position
    FROM players
    WHERE team_id = :team_id
    '''

    with get_connection() as conn:
        rows = conn.execute(sql, {"team_id": team_id}).fetchall()

    return [
        {
            "player_id": r[0],
            "player_name": r[1],
            "position": r[2]
        }
        for r in rows
    ]


def fetch_recent_games(team_id):

    sql = '''
    SELECT
        season,
        game_date
    FROM games
    WHERE home_team_id = :team_id
       OR away_team_id = :team_id
    ORDER BY game_date DESC
    LIMIT 10
    '''

    with get_connection() as conn:
        rows = conn.execute(sql, {"team_id": team_id}).fetchall()

    return rows
