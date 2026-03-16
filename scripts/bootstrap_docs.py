from pathlib import Path

root = Path(__file__).resolve().parent.parent

files = {
    "docs/master-blueprint.md": """
# Master Blueprint
Status: Draft

This document defines the architecture of the NAACP Tournament Simulation Platform.

Core systems:

- Data ingestion
- Simulation engine
- AI analysis
- Governance layer
- Dashboard delivery
""",

    "docs/file-index.md": """
# Master File Index

This document lists all core files used in the NAACP Tournament Simulation Platform.

Core directories:

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

    "governance/protocols/build-protocol.md": """
# Build Protocol

Purpose:
Define the rules for constructing the repository.

Rules:
- All modules must be documented.
- Database changes require migrations.
- Architecture layers must remain separated.
- Experiments cannot modify production code.
""",

    "governance/protocols/ai-build-protocol.md": """
# AI Build Protocol

Purpose:
Define how AI tools may assist development.

AI may:
- generate code
- suggest improvements
- analyze architecture
- document modules

AI may not:
- modify schema without migrations
- deploy code
- bypass governance rules
""",

    "governance/protocols/zip-delivery-protocol.md": """
# Zip Delivery Protocol

Purpose:
Define how modular file bundles are added to the repository.

Rules:
- Modules must arrive as complete zip packages.
- Zip packages must match the repository architecture.
- All files must be documented before merging.
""",

    "governance/drift/drift-taxonomy.md": """
# Drift Taxonomy

Defines types of drift detected in the system.

Types:
- Architecture drift
- Schema drift
- Model drift
- Prompt drift
- Output drift
"""
}

for path, content in files.items():
    file_path = root / path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print("Governance and architecture documents created.")