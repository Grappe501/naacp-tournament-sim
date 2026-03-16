import sys

from services.ingestion_worker.pipelines.teams_pipeline import run_teams_pipeline
from services.ingestion_worker.pipelines.rosters_pipeline import run_roster_pipeline
from services.ingestion_worker.pipelines.schedules_pipeline import run_schedule_pipeline

def run_all():

    print("Running team ingestion...")
    run_teams_pipeline()

    print("Running roster ingestion...")
    # Example team id for testing
    run_roster_pipeline("1")

    print("Running schedule ingestion...")
    run_schedule_pipeline("1", 2024)

    print("Pipelines complete.")


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "all":
        run_all()
    else:
        print("Usage: python run_pipelines.py all")
