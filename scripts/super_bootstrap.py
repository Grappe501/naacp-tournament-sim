from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parent.parent


def write(path: str, content: str) -> None:
    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def touch(path: str) -> None:
    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        file_path.write_text("", encoding="utf-8")


FILES = {
    "README.md": """
    # NAACP Tournament Simulation Platform

    This repository contains the architecture and foundation for a modular NCAA-style
    tournament simulation system using:

    - Python for ingestion, simulation, and orchestration
    - PostgreSQL as the source-of-truth database
    - TypeScript/Next.js for dashboard and admin surfaces
    - Governance-first architecture to prevent drift

    ## Core Areas

    - `apps/` user-facing applications
    - `services/` runtime systems
    - `packages/` shared contracts, config, db, prompts
    - `governance/` protocols, rules, drift controls
    - `docs/` architecture and operating documents
    - `scripts/` bootstrap and operational scripts

    ## First Commands

    ```bash
    python scripts/super_bootstrap.py
    docker compose up -d
    ```

    ## Status

    Bootstrapped foundation.
    """,

    ".gitignore": """
    __pycache__/
    *.pyc
    .pytest_cache/
    .venv/
    node_modules/
    .next/
    dist/
    build/
    .env
    .DS_Store
    coverage/
    """,

    ".env.example": """
    POSTGRES_DB=naacp_tournament
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_PORT=5432
    DATABASE_URL=postgresql://postgres:postgres@localhost:5432/naacp_tournament

    OPENAI_API_KEY=
    APP_ENV=development
    API_PORT=8000
    DASHBOARD_PORT=3000
    """,

    "docker-compose.yml": """
    version: "3.9"

    services:
      postgres:
        image: postgres:16
        container_name: naacp-tournament-postgres
        restart: unless-stopped
        environment:
          POSTGRES_DB: naacp_tournament
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        ports:
          - "5432:5432"
        volumes:
          - postgres_data:/var/lib/postgresql/data
          - ./packages/db/schema.sql:/docker-entrypoint-initdb.d/001-schema.sql

    volumes:
      postgres_data:
    """,

    "package.json": """
    {
      "name": "naacp-tournament-sim",
      "private": true,
      "version": "0.1.0",
      "workspaces": [
        "apps/*",
        "packages/*"
      ],
      "scripts": {
        "bootstrap:python": "python scripts/super_bootstrap.py",
        "test:python": "pytest",
        "db:up": "docker compose up -d",
        "db:down": "docker compose down"
      }
    }
    """,

    "docs/file-index.md": """
    # Master File Index

    Status: Active

    Core directories:

    - apps/
    - services/
    - packages/
    - data/
    - experiments/
    - governance/
    - docs/
    - scripts/
    - tests/

    Core generated files:

    - governance/protocols/build-protocol.md
    - governance/protocols/ai-build-protocol.md
    - governance/protocols/zip-delivery-protocol.md
    - governance/drift/drift-taxonomy.md
    - docs/master-blueprint.md
    - packages/db/schema.sql
    - services/api/app.py
    - services/ingestion-worker/ingest.py
    - services/simulation-worker/simulate.py
    """,

    "docs/master-blueprint.md": """
    # Master Blueprint

    Status: Active

    ## Mission

    Build a world-class, modular tournament simulation platform that ingests sports data,
    models games at a possession-aware level, runs tournament simulations, and improves
    through governed experimentation.

    ## Core Machines

    - Data Machine
    - Simulation Machine
    - Intelligence Machine
    - Governance Machine
    - Delivery Machine

    ## Stack

    - Python: ingestion, simulation, orchestration
    - PostgreSQL: source of truth
    - TypeScript/Next.js: dashboard and UI
    - Docker: local database runtime

    ## Principle

    No code without structure.
    No structure without governance.
    No AI without review.
    """,

    "governance/protocols/build-protocol.md": """
    # Build Protocol

    Version: 1.0

    ## Rules

    - All modules must have a defined purpose.
    - New files must fit the approved architecture.
    - Database changes require migrations or schema updates.
    - Tests and documentation are required for production-ready modules.
    - Architecture layers must remain separated.
    """,

    "governance/protocols/ai-build-protocol.md": """
    # AI Build Protocol

    Version: 1.0

    ## AI May

    - generate code
    - draft documentation
    - review architecture
    - propose experiments

    ## AI May Not

    - modify production schema without process
    - deploy code
    - bypass governance
    - create hidden services
    """,

    "governance/protocols/zip-delivery-protocol.md": """
    # Zip Delivery Protocol

    Version: 1.0

    ## Purpose

    Controls how full file bundles are introduced into the repository.

    ## Rules

    - Deliver complete module groups, not fragments.
    - Every delivered bundle must align with the file index.
    - Replacements must be whole-file safe.
    - Each bundle must include a manifest and purpose statement.
    """,

    "governance/drift/drift-taxonomy.md": """
    # Drift Taxonomy

    Version: 1.0

    ## Drift Types

    - Architecture drift
    - Schema drift
    - Contract drift
    - Model drift
    - Prompt drift
    - Output drift
    """,

    "packages/db/schema.sql": """
    CREATE TABLE IF NOT EXISTS conferences (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS teams (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        slug TEXT UNIQUE,
        conference_id INT REFERENCES conferences(id),
        city TEXT,
        state TEXT,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        team_id INT REFERENCES teams(id) ON DELETE CASCADE,
        full_name TEXT NOT NULL,
        position TEXT,
        class_year TEXT,
        height TEXT,
        weight INT,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS games (
        id SERIAL PRIMARY KEY,
        season INT NOT NULL,
        game_date DATE NOT NULL,
        home_team_id INT REFERENCES teams(id),
        away_team_id INT REFERENCES teams(id),
        neutral_site BOOLEAN NOT NULL DEFAULT FALSE,
        location TEXT,
        home_score INT,
        away_score INT,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS player_game_stats (
        id SERIAL PRIMARY KEY,
        game_id INT REFERENCES games(id) ON DELETE CASCADE,
        player_id INT REFERENCES players(id) ON DELETE CASCADE,
        minutes NUMERIC(5,2),
        points INT,
        rebounds INT,
        assists INT,
        steals INT,
        blocks INT,
        turnovers INT,
        fouls INT,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        UNIQUE(game_id, player_id)
    );

    CREATE TABLE IF NOT EXISTS team_game_stats (
        id SERIAL PRIMARY KEY,
        game_id INT REFERENCES games(id) ON DELETE CASCADE,
        team_id INT REFERENCES teams(id) ON DELETE CASCADE,
        possessions NUMERIC(8,2),
        offensive_rating NUMERIC(8,2),
        defensive_rating NUMERIC(8,2),
        pace NUMERIC(8,2),
        fg_pct NUMERIC(6,3),
        three_pt_pct NUMERIC(6,3),
        ft_pct NUMERIC(6,3),
        turnovers INT,
        rebounds INT,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        UNIQUE(game_id, team_id)
    );

    CREATE TABLE IF NOT EXISTS tournament_games (
        id SERIAL PRIMARY KEY,
        season INT NOT NULL,
        round_name TEXT NOT NULL,
        region TEXT,
        seed_home INT,
        seed_away INT,
        game_id INT REFERENCES games(id),
        winner_team_id INT REFERENCES teams(id),
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS simulation_runs (
        id SERIAL PRIMARY KEY,
        run_name TEXT NOT NULL,
        season INT NOT NULL,
        iterations INT NOT NULL,
        model_version TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS simulation_team_results (
        id SERIAL PRIMARY KEY,
        simulation_run_id INT REFERENCES simulation_runs(id) ON DELETE CASCADE,
        team_id INT REFERENCES teams(id) ON DELETE CASCADE,
        championship_wins INT NOT NULL DEFAULT 0,
        final_four_count INT NOT NULL DEFAULT 0,
        elite_eight_count INT NOT NULL DEFAULT 0,
        sweet_sixteen_count INT NOT NULL DEFAULT 0,
        round_of_32_count INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        UNIQUE(simulation_run_id, team_id)
    );
    """,

    "services/api/app.py": """
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.get("/")
    def root():
        return jsonify({
            "status": "ok",
            "service": "naacp tournament simulation api"
        })

    @app.get("/health")
    def health():
        return jsonify({"healthy": True})

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8000, debug=True)
    """,

    "services/ingestion-worker/ingest.py": """
    def run_ingestion() -> None:
        print("Starting ingestion pipeline...")
        print("TODO: implement source adapters, normalization, and load steps.")


    if __name__ == "__main__":
        run_ingestion()
    """,

    "services/simulation-worker/simulate.py": """
    import random


    def simulate_game(team_a_rating: float, team_b_rating: float) -> str:
        total = team_a_rating + team_b_rating
        roll = random.random() * total
        return "team_a" if roll < team_a_rating else "team_b"


    def run_simulation() -> None:
        winner = simulate_game(80.0, 75.0)
        print(f"Simulation complete. Winner: {winner}")


    if __name__ == "__main__":
        run_simulation()
    """,

    "apps/dashboard/README.md": """
    # Dashboard

    Planned frontend surface for:

    - bracket views
    - simulation results
    - team comparisons
    - player analysis
    """,

    "packages/prompt-registry/README.md": """
    # Prompt Registry

    All prompts used by AI systems must be versioned and documented here.
    """,

    "tests/test_bootstrap.py": """
    def test_bootstrap_sanity():
        assert True
    """,

    "scripts/run_api.py": """
    import subprocess
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parent.parent
    app_file = ROOT / "services" / "api" / "app.py"

    subprocess.run([sys.executable, str(app_file)], check=True)
    """,
}

DIRECTORIES = [
    ".cursor",
    ".github",
    "apps",
    "apps/dashboard",
    "services",
    "services/api",
    "services/ingestion-worker",
    "services/simulation-worker",
    "packages",
    "packages/db",
    "packages/prompt-registry",
    "data",
    "experiments",
    "governance",
    "governance/protocols",
    "governance/drift",
    "governance/architecture",
    "governance/rules",
    "docs",
    "docs/01-product",
    "docs/02-architecture",
    "docs/03-database",
    "docs/04-ingestion",
    "docs/05-simulation",
    "docs/06-ai",
    "docs/07-api",
    "docs/08-ui",
    "docs/09-testing",
    "docs/10-deployment",
    "docs/11-operations",
    "docs/12-roadmap",
    "scripts",
    "tests",
]

for directory in DIRECTORIES:
    (ROOT / directory).mkdir(parents=True, exist_ok=True)

for path, content in FILES.items():
    write(path, content)

# keep empty dirs trackable
for keep in [
    ".cursor/.gitkeep",
    ".github/.gitkeep",
    "apps/.gitkeep",
    "services/.gitkeep",
    "packages/.gitkeep",
    "data/.gitkeep",
    "experiments/.gitkeep",
    "governance/architecture/.gitkeep",
    "governance/rules/.gitkeep",
    "docs/01-product/.gitkeep",
    "docs/02-architecture/.gitkeep",
    "docs/03-database/.gitkeep",
    "docs/04-ingestion/.gitkeep",
    "docs/05-simulation/.gitkeep",
    "docs/06-ai/.gitkeep",
    "docs/07-api/.gitkeep",
    "docs/08-ui/.gitkeep",
    "docs/09-testing/.gitkeep",
    "docs/10-deployment/.gitkeep",
    "docs/11-operations/.gitkeep",
    "docs/12-roadmap/.gitkeep",
]:
    touch(keep)

print("Super bootstrap complete.")