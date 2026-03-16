from __future__ import annotations

import ast
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "audit"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_FILE = OUTPUT_DIR / "project_audit_report.txt"


CRITICAL_FILES = [
    "scripts/build.py",
    "packages/db/engine.py",
    "packages/db/connection.py",
    "packages/db/run_migrations.py",
    "services/api/app.py",
    "services/ingestion_worker/run_pipelines.py",
]

CRITICAL_DIRECTORIES = [
    "scripts/builders",
    "services/ingestion_worker",
    "services/simulation_worker",
    "services/publishing",
    "packages/db",
    "apps/dashboard",
]

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".next",
    "dist",
    "build",
    ".venv",
}


REPORT: Dict[str, List[str] | Dict[str, List[str]]] = {
    "python_files": [],
    "builders": [],
    "services": [],
    "pipelines": [],
    "simulation_modules": [],
    "database_modules": [],
    "publishing_modules": [],
    "missing_imports": [],
    "parse_errors": [],
    "empty_directories": [],
    "duplicate_filenames": [],
    "missing_init_files": [],
    "dead_builders": [],
    "missing_critical_files": [],
    "missing_critical_directories": [],
    "summary_notes": [],
}


def iter_files() -> List[Path]:
    files: List[Path] = []

    for root, dirs, filenames in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for filename in filenames:
            files.append(Path(root) / filename)

    return files


def iter_python_files() -> List[Path]:
    return [f for f in iter_files() if f.suffix == ".py"]


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def list_empty_directories() -> List[str]:
    empty_dirs: List[str] = []

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        path = Path(root)

        if path == ROOT:
            continue

        visible_files = [f for f in files if f not in {".gitkeep"}]
        visible_dirs = [d for d in dirs if d not in IGNORE_DIRS]

        if not visible_files and not visible_dirs:
            empty_dirs.append(relative(path))

    return sorted(empty_dirs)


def find_duplicate_filenames(files: List[Path]) -> List[str]:
    buckets: Dict[str, List[str]] = defaultdict(list)

    for f in files:
        buckets[f.name].append(relative(f))

    duplicates: List[str] = []

    for name, paths in sorted(buckets.items()):
        if len(paths) > 1:
            duplicates.append(f"{name} -> {paths}")

    return duplicates


def find_missing_init_files() -> List[str]:
    missing: List[str] = []

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        path = Path(root)

        if path == ROOT:
            continue

        py_files = [f for f in files if f.endswith(".py")]
        if py_files and "__init__.py" not in files:
            missing.append(relative(path))

    return sorted(missing)


def module_candidates() -> Set[str]:
    candidates: Set[str] = set()

    for py in iter_python_files():
        rel = relative(py)
        if rel.endswith("/__init__.py"):
            mod = rel[:-12].replace("/", ".")
            candidates.add(mod)
        elif rel.endswith(".py"):
            mod = rel[:-3].replace("/", ".")
            candidates.add(mod)

    return candidates


def path_style_import_candidates(module: str) -> Set[str]:
    parts = module.split(".")
    variants = set()

    variants.add(module)
    variants.add(module.replace("-", "_"))
    variants.add(module.replace("_", "-"))
    variants.add("/".join(parts))
    variants.add("/".join(parts).replace("-", "_"))
    variants.add("/".join(parts).replace("_", "-"))

    return variants


def import_exists(module: str, all_py_files: List[Path], all_modules: Set[str]) -> bool:
    if module in all_modules:
        return True

    rel_paths = [relative(f) for f in all_py_files]

    for candidate in path_style_import_candidates(module):
        for rel in rel_paths:
            if candidate in rel:
                return True

    return False


def analyze_ast(file_path: Path, all_py_files: List[Path], all_modules: Set[str]) -> None:
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except Exception as exc:
        REPORT["parse_errors"].append(f"{relative(file_path)} -> {exc}")
        return

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module
            if not module:
                continue
            if not import_exists(module, all_py_files, all_modules):
                REPORT["missing_imports"].append(f"{relative(file_path)} -> from {module} import ...")

        elif isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name
                if module.startswith(("os", "sys", "json", "math", "pathlib", "typing", "collections", "ast", "traceback", "random", "concurrent", "dataclasses")):
                    continue
                if not import_exists(module, all_py_files, all_modules):
                    REPORT["missing_imports"].append(f"{relative(file_path)} -> import {module}")


def detect_categories(file_path: Path) -> None:
    rel = relative(file_path)

    REPORT["python_files"].append(rel)

    if "scripts/builders/" in rel:
        REPORT["builders"].append(rel)

    if rel.startswith("services/"):
        REPORT["services"].append(rel)

    if "pipeline" in rel.lower():
        REPORT["pipelines"].append(rel)

    if rel.startswith("services/simulation_worker/"):
        REPORT["simulation_modules"].append(rel)

    if rel.startswith("packages/db/"):
        REPORT["database_modules"].append(rel)

    if rel.startswith("services/publishing/"):
        REPORT["publishing_modules"].append(rel)


def detect_dead_builders() -> List[str]:
    build_path = ROOT / "scripts" / "build.py"
    if not build_path.exists():
        return ["scripts/build.py missing, cannot evaluate dead builders"]

    build_text = build_path.read_text(encoding="utf-8")

    dead: List[str] = []

    for builder in REPORT["builders"]:
        builder_name = Path(builder).stem
        if builder_name == "__init__":
            continue

        expected_symbol = f"build_{builder_name.replace('_builder', '')}"
        if expected_symbol not in build_text and builder_name not in build_text:
            dead.append(builder)

    return sorted(dead)


def check_criticals() -> None:
    for rel in CRITICAL_FILES:
        if not (ROOT / rel).exists():
            REPORT["missing_critical_files"].append(rel)

    for rel in CRITICAL_DIRECTORIES:
        if not (ROOT / rel).exists():
            REPORT["missing_critical_directories"].append(rel)


def compute_readiness() -> int:
    score = 100

    if REPORT["parse_errors"]:
        score -= min(25, 5 * len(REPORT["parse_errors"]))

    if REPORT["missing_imports"]:
        score -= min(25, 2 * len(REPORT["missing_imports"]))

    if REPORT["missing_critical_files"]:
        score -= min(20, 5 * len(REPORT["missing_critical_files"]))

    if REPORT["missing_critical_directories"]:
        score -= min(20, 5 * len(REPORT["missing_critical_directories"]))

    if len(REPORT["pipelines"]) < 4:
        score -= 10

    if len(REPORT["simulation_modules"]) < 8:
        score -= 10

    if len(REPORT["database_modules"]) < 4:
        score -= 10

    if score < 0:
        score = 0

    return score


def readiness_label(score: int) -> str:
    if score >= 90:
        return "Strong foundation"
    if score >= 75:
        return "Mostly ready, some gaps"
    if score >= 60:
        return "Partially ready, notable gaps"
    return "Not ready"


def generate_summary() -> None:
    REPORT["summary_notes"].append(f"Python files: {len(REPORT['python_files'])}")
    REPORT["summary_notes"].append(f"Builders: {len(REPORT['builders'])}")
    REPORT["summary_notes"].append(f"Services: {len(REPORT['services'])}")
    REPORT["summary_notes"].append(f"Pipelines: {len(REPORT['pipelines'])}")
    REPORT["summary_notes"].append(f"Simulation modules: {len(REPORT['simulation_modules'])}")
    REPORT["summary_notes"].append(f"Database modules: {len(REPORT['database_modules'])}")
    REPORT["summary_notes"].append(f"Publishing modules: {len(REPORT['publishing_modules'])}")


def render_section(title: str, items: List[str]) -> str:
    lines = []
    lines.append("=" * 80)
    lines.append(title)
    lines.append("=" * 80)

    if not items:
        lines.append("None")
    else:
        lines.extend(items)

    lines.append("")
    return "\n".join(lines)


def build_text_report() -> str:
    score = compute_readiness()
    label = readiness_label(score)

    sections = [
        "=" * 80,
        "NAACP TOURNAMENT PROJECT AUDIT REPORT",
        "=" * 80,
        "",
        f"Estimated readiness: {score}%",
        f"Readiness label: {label}",
        "",
    ]

    sections.extend(REPORT["summary_notes"])
    sections.append("")

    sections.append(render_section("BUILDERS", sorted(REPORT["builders"])))
    sections.append(render_section("SERVICES", sorted(REPORT["services"])))
    sections.append(render_section("PIPELINES", sorted(REPORT["pipelines"])))
    sections.append(render_section("SIMULATION MODULES", sorted(REPORT["simulation_modules"])))
    sections.append(render_section("DATABASE MODULES", sorted(REPORT["database_modules"])))
    sections.append(render_section("PUBLISHING MODULES", sorted(REPORT["publishing_modules"])))
    sections.append(render_section("MISSING IMPORTS", sorted(set(REPORT["missing_imports"]))))
    sections.append(render_section("PARSE ERRORS", sorted(REPORT["parse_errors"])))
    sections.append(render_section("EMPTY DIRECTORIES", REPORT["empty_directories"]))
    sections.append(render_section("DUPLICATE FILENAMES", REPORT["duplicate_filenames"]))
    sections.append(render_section("MISSING __init__.py", REPORT["missing_init_files"]))
    sections.append(render_section("LIKELY DEAD BUILDERS", REPORT["dead_builders"]))
    sections.append(render_section("MISSING CRITICAL FILES", REPORT["missing_critical_files"]))
    sections.append(render_section("MISSING CRITICAL DIRECTORIES", REPORT["missing_critical_directories"]))

    sections.append("=" * 80)
    sections.append("WHAT WORKS")
    sections.append("=" * 80)

    works = []

    if REPORT["builders"]:
        works.append("Builder layer exists.")
    if REPORT["database_modules"]:
        works.append("Database layer exists.")
    if REPORT["pipelines"]:
        works.append("Pipeline layer exists.")
    if REPORT["simulation_modules"]:
        works.append("Simulation layer exists.")
    if REPORT["publishing_modules"]:
        works.append("Publishing layer exists.")
    if not REPORT["missing_critical_files"]:
        works.append("Critical files appear present.")

    if not works:
        works.append("No major working layers detected yet.")

    sections.extend(works)
    sections.append("")

    sections.append("=" * 80)
    sections.append("WHAT IS NOT READY")
    sections.append("=" * 80)

    not_ready = []

    if REPORT["missing_imports"]:
        not_ready.append("There are unresolved imports.")
    if REPORT["parse_errors"]:
        not_ready.append("Some Python files do not parse.")
    if REPORT["missing_init_files"]:
        not_ready.append("Some Python package directories are missing __init__.py.")
    if REPORT["dead_builders"]:
        not_ready.append("Some builders may exist but are not wired into scripts/build.py.")
    if REPORT["empty_directories"]:
        not_ready.append("Some directories are present but still empty.")
    if REPORT["missing_critical_files"] or REPORT["missing_critical_directories"]:
        not_ready.append("Some critical files or directories are missing.")

    if not not_ready:
        not_ready.append("No obvious structural blockers detected by this auditor.")

    sections.extend(not_ready)
    sections.append("")

    sections.append("=" * 80)
    sections.append("WHAT TO BUILD NEXT")
    sections.append("=" * 80)

    next_steps = []

    if REPORT["missing_imports"]:
        next_steps.append("Fix missing imports first.")
    if REPORT["parse_errors"]:
        next_steps.append("Fix Python syntax/parse errors.")
    if REPORT["missing_init_files"]:
        next_steps.append("Add missing __init__.py files to Python package directories.")
    if REPORT["dead_builders"]:
        next_steps.append("Wire unused builders into scripts/build.py or remove them.")
    if not REPORT["missing_imports"] and not REPORT["parse_errors"]:
        next_steps.append("Move to feature completeness: player logs, injuries, advanced metrics, tournament runtime.")
        next_steps.append("Build runtime execution layer: database migrations, full harvest, simulation run, publishing sync.")
        next_steps.append("Build dashboard readers for published JSON.")
        next_steps.append("Build comments/blog/discussion layer for public matchup pages.")

    sections.extend(next_steps)
    sections.append("")

    return "\n".join(sections)


def print_console_summary() -> None:
    score = compute_readiness()
    label = readiness_label(score)

    print("\n" + "=" * 80)
    print("PROJECT AUDIT COMPLETE")
    print("=" * 80)
    print(f"Estimated readiness: {score}%")
    print(f"Readiness label: {label}")
    print(f"Builders found: {len(REPORT['builders'])}")
    print(f"Pipelines found: {len(REPORT['pipelines'])}")
    print(f"Missing imports: {len(set(REPORT['missing_imports']))}")
    print(f"Parse errors: {len(REPORT['parse_errors'])}")
    print(f"Likely dead builders: {len(REPORT['dead_builders'])}")
    print(f"Report written to: {relative(REPORT_FILE)}")
    print("=" * 80 + "\n")


def run_audit() -> None:
    print("Running full project audit...")

    all_py = iter_python_files()
    all_mods = module_candidates()

    for py in all_py:
        detect_categories(py)
        analyze_ast(py, all_py, all_mods)

    REPORT["empty_directories"] = list_empty_directories()
    REPORT["duplicate_filenames"] = find_duplicate_filenames(iter_files())
    REPORT["missing_init_files"] = find_missing_init_files()
    REPORT["dead_builders"] = detect_dead_builders()
    check_criticals()
    generate_summary()

    report_text = build_text_report()
    REPORT_FILE.write_text(report_text, encoding="utf-8")

    print_console_summary()


if __name__ == "__main__":
    run_audit()