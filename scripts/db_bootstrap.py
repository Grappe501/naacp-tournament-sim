import psycopg2

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True

cur = conn.cursor()

cur.execute("CREATE DATABASE naacp_tournament")

print("Database created.")