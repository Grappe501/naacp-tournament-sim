from utils.file_utils import ensure_dir, write_file

def build_repo():
    print("Building repository structure...")

    dirs = [
        "apps/dashboard",
        "services/api",
        "services/ingestion-worker",
        "services/ingestion-worker/sources",
        "services/ingestion-worker/sources/espn",
        "services/ingestion-worker/sources/manual",
        "services/ingestion-worker/normalizers",
        "services/ingestion-worker/loaders",
        "services/ingestion-worker/pipelines",
        "services/ingestion-worker/registry",
        "services/ingestion-worker/models",
        "services/simulation-worker",
        "packages/db",
        "packages/prompt-registry",
        "data/raw",
        "data/staged",
        "data/curated",
        "data/features",
        "data/simulation-inputs",
        "data/simulation-outputs",
        "experiments",
        "governance/protocols",
        "governance/drift",
        "docs",
        "tests",
    ]

    for d in dirs:
        ensure_dir(d)

    init_files = [
        "services/ingestion-worker/__init__.py",
        "services/ingestion-worker/sources/__init__.py",
        "services/ingestion-worker/sources/espn/__init__.py",
        "services/ingestion-worker/sources/manual/__init__.py",
        "services/ingestion-worker/normalizers/__init__.py",
        "services/ingestion-worker/loaders/__init__.py",
        "services/ingestion-worker/pipelines/__init__.py",
        "services/ingestion-worker/registry/__init__.py",
        "services/ingestion-worker/models/__init__.py",
        "scripts/builders/__init__.py",
        "scripts/utils/__init__.py",
    ]

    for path in init_files:
        write_file(path, "")