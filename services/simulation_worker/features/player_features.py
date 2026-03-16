from packages.db.connection import get_connection


def calculate_player_features():

    sql = '''

    SELECT
        p.id,
        p.full_name,
        AVG(l.points) as avg_points,
        AVG(l.rebounds) as avg_rebounds,
        AVG(l.assists) as avg_assists
    FROM players p
    LEFT JOIN player_game_logs l
        ON l.player_id = p.id
    GROUP BY p.id, p.full_name

    '''

    with get_connection() as conn:
        rows = conn.execute(sql).fetchall()

    features = []

    for r in rows:

        features.append({
            "player_id": r[0],
            "player_name": r[1],
            "avg_points": float(r[2]) if r[2] else 0,
            "avg_rebounds": float(r[3]) if r[3] else 0,
            "avg_assists": float(r[4]) if r[4] else 0
        })

    return features
