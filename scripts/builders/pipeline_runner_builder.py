from utils.file_utils import write_file


def build_pipeline_runner():

    print("Building pipeline runners...")

    code = """
import sys

from services.ingestion_worker.pipelines.teams_pipeline import run_teams_pipeline
from services.ingestion_worker.pipelines.rosters_pipeline import run_roster_pipeline
from services.ingestion_worker.pipelines.schedules_pipeline import run_schedule_pipeline
from services.ingestion_worker.pipelines.full_harvest import run_full_harvest


def run_all():
    print("Running teams pipeline...")
    teams = run_teams_pipeline()

    if teams:
        sample_team_id = teams[0]["external_id"]

        print("Running roster pipeline...")
        run_roster_pipeline(sample_team_id)

        print("Running schedule pipeline...")
        run_schedule_pipeline(sample_team_id, 2026)

    print("Pipelines complete.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        run_all()
    elif len(sys.argv) > 1 and sys.argv[1] == "harvest":
        run_full_harvest()
    else:
        print("Usage:")
        print("  python services/ingestion_worker/run_pipelines.py all")
        print("  python services/ingestion_worker/run_pipelines.py harvest")
"""

    write_file("services/ingestion_worker/run_pipelines.py", code)