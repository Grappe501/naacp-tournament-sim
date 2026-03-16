from .connection import get_connection

def run_query(sql, params=None):

    with get_connection() as conn:
        result = conn.execute(sql, params or {})
        return result.fetchall()
