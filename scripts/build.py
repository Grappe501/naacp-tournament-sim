from builders.repo_builder import build_repo
from builders.governance_builder import build_governance
from builders.database_builder import build_database
from builders.ingestion_builder import build_ingestion
from builders.simulation_builder import build_simulation
from builders.api_builder import build_api
from builders.dashboard_builder import build_dashboard
from builders.ai_builder import build_ai
from builders.env_builder import build_environment
from builders.db_runtime_builder import build_db_runtime
from builders.ncaa_data_builder import build_ncaa_data
from builders.data_loader_builder import build_data_loader

# new
from builders.harvester_builder import build_harvester
from builders.roster_builder import build_roster_ingestion
from builders.schedule_builder import build_schedule_ingestion
from builders.boxscore_builder import build_boxscore_ingestion
from builders.metrics_builder import build_metrics_ingestion


def main():
    print("Starting full system build...")

    build_repo()
    build_governance()
    build_environment()
    build_database()
    build_db_runtime()

    build_ingestion()
    build_harvester()
    build_ncaa_data()
    build_roster_ingestion()
    build_schedule_ingestion()
    build_boxscore_ingestion()
    build_metrics_ingestion()
    build_data_loader()

    build_simulation()
    build_api()
    build_dashboard()
    build_ai()

    print("System build complete.")


if __name__ == "__main__":
    main()