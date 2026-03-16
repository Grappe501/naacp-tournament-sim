from utils.file_utils import ensure_dir, write_file


def build_repo():
    print("Building repository structure...")

    dirs = [
        "apps/dashboard",
        "apps/dashboard/public",
        "apps/dashboard/public/data",
        "services/api",
        "services/ingestion_worker",
        "services/ingestion_worker/sources",
        "services/ingestion_worker/sources/espn",
        "services/ingestion_worker/sources/sports_reference",
        "services/ingestion_worker/sources/manual",
        "services/ingestion_worker/normalizers",
        "services/ingestion_worker/loaders",
        "services/ingestion_worker/pipelines",
        "services/ingestion_worker/registry",
        "services/ingestion_worker/models",
        "services/ingestion_worker/utils",
        "services/simulation_worker",
        "services/publishing",
        "packages/db",
        "packages/prompt-registry",
        "data",
        "data/raw",
        "data/raw/teams",
        "data/raw/rosters",
        "data/raw/schedules",
        "data/raw/boxscores",
        "data/raw/player_logs",
        "data/raw/injuries",
        "data/raw/metrics",
        "data/staged",
        "data/curated",
        "data/features",
        "data/simulation-inputs",
        "data/simulation-outputs",
        "data/published",
        "data/published/matchups",
        "data/published/players",
        "data/published/brackets",
        "data/published/dashboard",
        "experiments",
        "governance/protocols",
        "governance/drift",
        "docs",
        "tests",
    ]

    for d in dirs:
        ensure_dir(d)

    init_files = [
        "services/ingestion_worker/__init__.py",
        "services/ingestion_worker/sources/__init__.py",
        "services/ingestion_worker/sources/espn/__init__.py",
        "services/ingestion_worker/sources/sports_reference/__init__.py",
        "services/ingestion_worker/sources/manual/__init__.py",
        "services/ingestion_worker/normalizers/__init__.py",
        "services/ingestion_worker/loaders/__init__.py",
        "services/ingestion_worker/pipelines/__init__.py",
        "services/ingestion_worker/registry/__init__.py",
        "services/ingestion_worker/models/__init__.py",
        "services/ingestion_worker/utils/__init__.py",
        "services/publishing/__init__.py",
        "scripts/builders/__init__.py",
        "scripts/utils/__init__.py",
    ]

    for path in init_files:
        write_file(path, "")