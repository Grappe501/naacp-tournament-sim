from packages.db.connection import get_connection


def insert_teams(teams):

    conn = get_connection()

    for t in teams:

        conn.execute(
            "INSERT INTO teams(name) VALUES (%s)",
            (t["name"],)
        )

    conn.commit()
