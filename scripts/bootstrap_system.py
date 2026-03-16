from pathlib import Path

root = Path(__file__).resolve().parent.parent

def write_file(path, content):
    file_path = root / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {

# -------------------------
# GOVERNANCE
# -------------------------

"governance/protocols/build-protocol.md": """
# Build Protocol

Defines construction rules for the platform.

Rules
- No direct schema edits without migrations
- Modules must include documentation
- Architecture layers must remain isolated
""",

"governance/protocols/ai-build-protocol.md": """
# AI Build Protocol

Defines how AI assists development.

AI may:
- generate code
- analyze architecture
- propose improvements

AI may not:
- deploy code
- modify production schema
""",

"governance/protocols/zip-delivery-protocol.md": """
# Zip Delivery Protocol

Defines how modular components are introduced into the system.

Modules must be delivered as complete packages.
""",

"governance/drift/drift-taxonomy.md": """
# Drift Taxonomy

Defines detectable system drift types.

- Architecture drift
- Schema drift
- Model drift
- Prompt drift
""",

# -------------------------
# ARCHITECTURE DOCS
# -------------------------

"docs/master-blueprint.md": """
# Master Blueprint

Defines system architecture.

Systems
- Data ingestion
- Simulation engine
- AI analysis
- Governance
- Dashboard delivery
""",

"docs/file-index.md": """
# File Index

Core directories

apps/
services/
packages/
data/
experiments/
governance/
docs/
scripts/
tests/
""",

# -------------------------
# DATABASE
# -------------------------

"packages/db/schema.sql": """
-- Core database schema

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT,
    conference TEXT
);

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT,
    team_id INT REFERENCES teams(id)
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    home_team INT REFERENCES teams(id),
    away_team INT REFERENCES teams(id),
    game_date DATE
);
""",

# -------------------------
# INGESTION
# -------------------------

"services/ingestion-worker/ingest.py": """
def run_ingestion():
    print("Data ingestion pipeline starting...")
""",

# -------------------------
# SIMULATION
# -------------------------

"services/simulation-worker/simulate.py": """
def run_simulation():
    print("Running tournament simulation...")
""",

# -------------------------
# API
# -------------------------

"services/api/app.py": """
from flask import Flask

app = Flask(__name__)

@app.route("/")
def status():
    return {"status": "NAACP tournament simulation API running"}
""",

# -------------------------
# DASHBOARD
# -------------------------

"apps/dashboard/README.md": """
# Dashboard

This application will visualize simulation results.
""",

# -------------------------
# PROMPT REGISTRY
# -------------------------

"packages/prompt-registry/prompts.md": """
# Prompt Registry

All AI prompts used by the system must be documented here.
""",

# -------------------------
# TESTS
# -------------------------

"tests/test_bootstrap.py": """
def test_bootstrap():
    assert True
""",

# -------------------------
# PLACEHOLDER FILES
# -------------------------

".cursor/.gitkeep": "",
".github/.gitkeep": "",
"apps/.gitkeep": "",
"data/.gitkeep": "",
"experiments/.gitkeep": "",
"scripts/.gitkeep": "",
"services/.gitkeep": "",
"packages/.gitkeep": "",
}

for path, content in files.items():
    write_file(path, content)

print("System bootstrap complete.")