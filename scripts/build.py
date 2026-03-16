from builders.repo_builder import build_repo
from builders.governance_builder import build_governance
from builders.database_builder import build_database
from builders.ingestion_builder import build_ingestion
from builders.simulation_builder import build_simulation
from builders.api_builder import build_api
from builders.dashboard_builder import build_dashboard
from builders.ai_builder import build_ai

def main():
    print("Starting full system build...")

    build_repo()
    build_governance()
    build_database()
    build_ingestion()
    build_simulation()
    build_api()
    build_dashboard()
    build_ai()

    print("System build complete.")

if __name__ == "__main__":
    main()