from services.ingestion_worker.pipelines.teams_pipeline import run_teams_pipeline
from services.ingestion_worker.pipelines.rosters_pipeline import run_roster_pipeline
from services.ingestion_worker.pipelines.schedules_pipeline import run_schedule_pipeline


def run_full_harvest(season: int = 2026, max_teams: int | None = 10) -> None:
    teams = run_teams_pipeline()

    subset = teams if max_teams is None else teams[:max_teams]

    for team in subset:
        external_id = team["external_id"]
        run_roster_pipeline(external_id)
        run_schedule_pipeline(external_id, season)

    print("Full tournament data harvest complete.")


if __name__ == "__main__":
    run_full_harvest()
