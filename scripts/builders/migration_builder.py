from utils.file_utils import write_file, ensure_dir

def build_migrations():

    print("Building migration system...")

    ensure_dir("packages/db/migrations")

    registry = """
{
    "applied_migrations": []
}
"""

    migration_runner = """

import os
import json
import psycopg2

MIGRATION_DIR = "packages/db/migrations"
REGISTRY_FILE = "packages/db/migration_registry.json"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/naacp_tournament"
)

def load_registry():

    if not os.path.exists(REGISTRY_FILE):
        return {"applied_migrations": []}

    with open(REGISTRY_FILE) as f:
        return json.load(f)

def save_registry(reg):

    with open(REGISTRY_FILE, "w") as f:
        json.dump(reg, f, indent=2)

def run_migrations():

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    registry = load_registry()

    migrations = sorted(os.listdir(MIGRATION_DIR))

    for m in migrations:

        if m in registry["applied_migrations"]:
            continue

        path = os.path.join(MIGRATION_DIR, m)

        with open(path) as f:
            sql = f.read()

        print("Applying migration:", m)

        cur.execute(sql)

        registry["applied_migrations"].append(m)

    conn.commit()

    save_registry(registry)

    print("All migrations applied.")


if __name__ == "__main__":

    run_migrations()

"""

    write_file("packages/db/run_migrations.py", migration_runner)
    write_file("packages/db/migration_registry.json", registry)