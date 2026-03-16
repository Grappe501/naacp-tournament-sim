from packages.db.connection import get_connection


def calculate_team_features():

    sql = '''

    SELECT
        t.id,
        t.name,
        COUNT(g.id) as games_played
    FROM teams t
    LEFT JOIN games g
        ON g.home_team_id = t.id
        OR g.away_team_id = t.id
    GROUP BY t.id, t.name

    '''

    with get_connection() as conn:
        rows = conn.execute(sql).fetchall()

    features = []

    for r in rows:

        games_played = r[2] if r[2] else 1

        offense = 100 + (games_played * 0.1)
        defense = 100 - (games_played * 0.1)

        features.append({
            "team_id": r[0],
            "team_name": r[1],
            "offense_rating": offense,
            "defense_rating": defense,
            "net_rating": offense - defense
        })

    return features
