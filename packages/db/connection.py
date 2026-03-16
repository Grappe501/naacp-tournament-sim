import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/naacp_tournament")

engine = create_engine(DATABASE_URL, future=True)

def get_connection():
    return engine.connect()
