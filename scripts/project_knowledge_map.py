from __future__ import annotations

import ast
import os
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "audit"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_MAP = OUTPUT_DIR / "SYSTEM_MAP.md"
ARCHITECTURE_GRAPH = OUTPUT_DIR / "ARCHITECTURE_GRAPH.md"
DEPENDENCY_TREE = OUTPUT_DIR / "DEPENDENCY_TREE.md"

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "node_modules",
    ".next",
    "dist",
    "build",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def iter_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            yield Path(root) / f


def iter_python_files():
    for f in iter_files():
        if f.suffix == ".py":
            yield f


def collect_sections():
    data = {
        "builders": [],
        "api": [],
        "ingestion": [],
        "simulation": [],
        "publishing": [],
        "database": [],
        "docs": [],
        "scripts": [],
        "tests": [],
        "apps": [],
    }

    for f in iter_files():
        r = rel(f)

        if r.startswith("scripts/builders/"):
            data["builders"].append(r)
        elif r.startswith("services/api/"):
            data["api"].append(r)
        elif r.startswith("services/ingestion_worker/"):
            data["ingestion"].append(r)
        elif r.startswith("services/simulation_worker/"):
            data["simulation"].append(r)
        elif r.startswith("services/publishing/"):
            data["publishing"].append(r)
        elif r.startswith("packages/db/"):
            data["database"].append(r)
        elif r.startswith("docs/"):
            data["docs"].append(r)
        elif r.startswith("scripts/"):
            data["scripts"].append(r)
        elif r.startswith("tests/"):
            data["tests"].append(r)
        elif r.startswith("apps/"):
            data["apps"].append(r)

    for key in data:
        data[key] = sorted(data[key])

    return data


def parse_imports(file_path: Path):
    imports = []

    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except Exception:
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(f"from {node.module}")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}")

    return sorted(set(imports))


def build_dependency_map():
    dependency_map = {}

    for py in iter_python_files():
        dependency_map[rel(py)] = parse_imports(py)

    return dependency_map


def render_system_map(sections):
    lines = []
    lines.append("# SYSTEM MAP")
    lines.append("")
    lines.append("This document summarizes the current NAACP Tournament platform structure.")
    lines.append("")

    ordered = [
        ("builders", "Builders"),
        ("database", "Database Layer"),
        ("ingestion", "Ingestion Layer"),
        ("simulation", "Simulation Layer"),
        ("publishing", "Publishing Layer"),
        ("api", "API Layer"),
        ("apps", "Apps / Dashboard"),
        ("scripts", "Scripts"),
        ("docs", "Documentation"),
        ("tests", "Tests"),
    ]

    for key, title in ordered:
        lines.append(f"## {title}")
        lines.append("")
        if not sections[key]:
            lines.append("None")
        else:
            for item in sections[key]:
                lines.append(f"- `{item}`")
        lines.append("")

    return "\n".join(lines) + "\n"


def render_architecture_graph(sections):
    lines = []
    lines.append("# ARCHITECTURE GRAPH")
    lines.append("")
    lines.append("```text")
    lines.append("DATA SOURCES")
    lines.append("    ↓")
    lines.append("services/ingestion_worker")
    lines.append("    ↓")
    lines.append("packages/db")
    lines.append("    ↓")
    lines.append("services/simulation_worker/features")
    lines.append("    ↓")
    lines.append("services/simulation_worker")
    lines.append("    ↓")
    lines.append("services/publishing")
    lines.append("    ↓")
    lines.append("services/api")
    lines.append("    ↓")
    lines.append("apps/dashboard")
    lines.append("```")
    lines.append("")
    lines.append("## Active Subsystems")
    lines.append("")
    lines.append(f"- Builders: {len(sections['builders'])}")
    lines.append(f"- Ingestion modules: {len(sections['ingestion'])}")
    lines.append(f"- Simulation modules: {len(sections['simulation'])}")
    lines.append(f"- Database modules: {len(sections['database'])}")
    lines.append(f"- Publishing modules: {len(sections['publishing'])}")
    lines.append(f"- API modules: {len(sections['api'])}")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_dependency_tree(dependency_map):
    lines = []
    lines.append("# DEPENDENCY TREE")
    lines.append("")
    lines.append("This document lists Python files and their direct imports.")
    lines.append("")

    for file_name in sorted(dependency_map.keys()):
        lines.append(f"## `{file_name}`")
        lines.append("")
        imports = dependency_map[file_name]
        if not imports:
            lines.append("No detected imports.")
        else:
            for imp in imports:
                lines.append(f"- {imp}")
        lines.append("")

    return "\n".join(lines) + "\n"


def write_reports():
    sections = collect_sections()
    dependency_map = build_dependency_map()

    SYSTEM_MAP.write_text(render_system_map(sections), encoding="utf-8")
    ARCHITECTURE_GRAPH.write_text(render_architecture_graph(sections), encoding="utf-8")
    DEPENDENCY_TREE.write_text(render_dependency_tree(dependency_map), encoding="utf-8")

    print("Knowledge map generated:")
    print(f" - {rel(SYSTEM_MAP)}")
    print(f" - {rel(ARCHITECTURE_GRAPH)}")
    print(f" - {rel(DEPENDENCY_TREE)}")


if __name__ == "__main__":
    write_reports()