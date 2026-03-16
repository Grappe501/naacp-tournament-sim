from utils.file_utils import ensure_dir

def build_repo():

    print("Building repository structure...")

    dirs = [
        "apps/dashboard",
        "services/api",
        "services/ingestion-worker",
        "services/simulation-worker",
        "packages/db",
        "packages/prompt-registry",
        "data",
        "experiments",
        "governance/protocols",
        "governance/drift",
        "docs",
        "tests"
    ]

    for d in dirs:
        ensure_dir(d)