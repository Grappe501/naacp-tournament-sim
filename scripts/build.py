"""
Master Build Engine
NAACP Tournament Simulation Platform

This script orchestrates full and partial system construction using
modular builder scripts.

Usage:
    python scripts/build.py all
    python scripts/build.py core
    python scripts/build.py database
    python scripts/build.py ingestion
    python scripts/build.py application
    python scripts/build.py simulation
    python scripts/build.py api
    python scripts/build.py dashboard
    python scripts/build.py ai
    python scripts/build.py list
"""

from __future__ import annotations

import sys
import traceback
from typing import Callable, Dict, Iterable, List, Tuple

# Core builders
from builders.repo_builder import build_repo
from builders.governance_builder import build_governance
from builders.env_builder import build_environment
from builders.database_builder import build_database
from builders.db_runtime_builder import build_db_runtime
from builders.migration_builder import build_migrations
from builders.schema_builder import build_schema

# Ingestion builders
from builders.ingestion_builder import build_ingestion
from builders.harvester_builder import build_harvester
from builders.ncaa_data_builder import build_ncaa_data
from builders.roster_builder import build_roster_ingestion
from builders.schedule_builder import build_schedule_ingestion
from builders.boxscore_builder import build_boxscore_ingestion
from builders.metrics_builder import build_metrics_ingestion
from builders.data_loader_builder import build_data_loader
from builders.pipeline_runner_builder import build_pipeline_runner

# Application builders
from builders.simulation_data_builder import build_simulation_data
from builders.feature_engineering_builder import build_feature_engineering
from builders.simulation_builder import build_simulation
from builders.bracket_simulation_builder import build_bracket_simulation
from builders.monte_carlo_builder import build_monte_carlo
from builders.simulation_narrative_builder import build_simulation_narrative
from builders.api_builder import build_api
from builders.dashboard_builder import build_dashboard
from builders.ai_builder import build_ai


BuilderFn = Callable[[], None]
BuilderSpec = Tuple[str, BuilderFn]


# -----------------------------------------------------
# Builder Groups
# -----------------------------------------------------

CORE_BUILDERS: List[BuilderSpec] = [
    ("repo_builder", build_repo),
    ("governance_builder", build_governance),
    ("env_builder", build_environment),
]

DATABASE_BUILDERS: List[BuilderSpec] = [
    ("database_builder", build_database),
    ("db_runtime_builder", build_db_runtime),
    ("migration_builder", build_migrations),
    ("schema_builder", build_schema),
]

INGESTION_BUILDERS: List[BuilderSpec] = [
    ("ingestion_builder", build_ingestion),
    ("harvester_builder", build_harvester),
    ("teams_source_builder", build_ncaa_data),
    ("roster_builder", build_roster_ingestion),
    ("schedule_builder", build_schedule_ingestion),
    ("boxscore_builder", build_boxscore_ingestion),
    ("metrics_builder", build_metrics_ingestion),
    ("data_loader_builder", build_data_loader),
    ("pipeline_runner_builder", build_pipeline_runner),
]

APPLICATION_BUILDERS: List[BuilderSpec] = [
    ("simulation_data_builder", build_simulation_data),
    ("feature_engineering_builder", build_feature_engineering),
    ("simulation_builder", build_simulation),
    ("bracket_simulation_builder", build_bracket_simulation),
    ("monte_carlo_builder", build_monte_carlo),
    ("simulation_narrative_builder", build_simulation_narrative),
    ("api_builder", build_api),
    ("dashboard_builder", build_dashboard),
    ("ai_builder", build_ai),
]


# -----------------------------------------------------
# Utility
# -----------------------------------------------------

def banner(title: str) -> None:
    line = "=" * 56
    print(f"\n{line}\n {title}\n{line}\n")


def run_builder(name: str, fn: BuilderFn) -> None:
    """Safely execute a builder and halt on failure."""
    print(f"--- Running builder: {name} ---")
    try:
        fn()
        print(f"✓ {name} complete\n")
    except Exception:
        print(f"✗ {name} failed\n")
        traceback.print_exc()
        sys.exit(1)


def run_builders(builders: Iterable[BuilderSpec], group_name: str) -> None:
    """Run a named collection of builders in sequence."""
    banner(f"BUILD GROUP: {group_name}")
    for name, fn in builders:
        run_builder(name, fn)


def available_modes() -> Dict[str, Callable[[], None]]:
    """Return CLI modes mapped to callable build functions."""
    return {
        "all": build_all,
        "core": build_core,
        "database": build_database_layer,
        "ingestion": build_ingestion_layer,
        "application": build_application_layer,
        "simulation": build_simulation_only,
        "api": build_api_only,
        "dashboard": build_dashboard_only,
        "ai": build_ai_only,
        "list": print_modes,
    }


def print_modes() -> None:
    print(
        """
Available commands:

    python scripts/build.py all
    python scripts/build.py core
    python scripts/build.py database
    python scripts/build.py ingestion
    python scripts/build.py application
    python scripts/build.py simulation
    python scripts/build.py api
    python scripts/build.py dashboard
    python scripts/build.py ai
    python scripts/build.py list
""".strip()
    )


# -----------------------------------------------------
# Build Phases
# -----------------------------------------------------

def build_core() -> None:
    run_builders(CORE_BUILDERS, "CORE")


def build_database_layer() -> None:
    run_builders(DATABASE_BUILDERS, "DATABASE")


def build_ingestion_layer() -> None:
    run_builders(INGESTION_BUILDERS, "INGESTION")


def build_application_layer() -> None:
    run_builders(APPLICATION_BUILDERS, "APPLICATION")


def build_simulation_only() -> None:
    run_builders(
        [
            ("simulation_data_builder", build_simulation_data),
            ("feature_engineering_builder", build_feature_engineering),
            ("simulation_builder", build_simulation),
            ("bracket_simulation_builder", build_bracket_simulation),
            ("monte_carlo_builder", build_monte_carlo),
            ("simulation_narrative_builder", build_simulation_narrative),
        ],
        "SIMULATION ONLY",
    )


def build_api_only() -> None:
    run_builders([("api_builder", build_api)], "API ONLY")


def build_dashboard_only() -> None:
    run_builders([("dashboard_builder", build_dashboard)], "DASHBOARD ONLY")


def build_ai_only() -> None:
    run_builders([("ai_builder", build_ai)], "AI ONLY")


# -----------------------------------------------------
# Master Build Controller
# -----------------------------------------------------

def build_all() -> None:
    banner("NAACP TOURNAMENT SYSTEM BUILD STARTED")
    build_core()
    build_database_layer()
    build_ingestion_layer()
    build_application_layer()
    banner("SYSTEM BUILD COMPLETE")


# -----------------------------------------------------
# CLI Interface
# -----------------------------------------------------

def main() -> None:
    mode = sys.argv[1].strip().lower() if len(sys.argv) > 1 else "all"
    modes = available_modes()

    if mode not in modes:
        print(f"\nUnknown build command: {mode}\n")
        print_modes()
        sys.exit(1)

    modes[mode]()


if __name__ == "__main__":
    main()