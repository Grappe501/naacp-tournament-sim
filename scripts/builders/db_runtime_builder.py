from utils.file_utils import write_file, ensure_dir

def build_db_runtime():

    print("Building database runtime layer...")

    ensure_dir("packages/db")

    engine_code = """
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/naacp_tournament"
)

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    future=True
)
"""

    connection_code = """
from contextlib import contextmanager
from .engine import engine

@contextmanager
def get_connection():

    conn = engine.connect()

    try:
        yield conn
    finally:
        conn.close()
"""

    transaction_code = """
from contextlib import contextmanager
from .engine import engine

@contextmanager
def transaction():

    with engine.begin() as conn:
        yield conn
"""

    queries_code = """
from .connection import get_connection

def run_query(sql, params=None):

    with get_connection() as conn:
        result = conn.execute(sql, params or {})
        return result.fetchall()
"""

    write_file("packages/db/engine.py", engine_code)
    write_file("packages/db/connection.py", connection_code)
    write_file("packages/db/transactions.py", transaction_code)
    write_file("packages/db/queries.py", queries_code)