from utils.file_utils import write_file, ensure_dir


def build_tournament_data_harvester():

    print("Building NCAA tournament data harvester system...")

    ensure_dir("services/ingestion_worker/sources/espn")
    ensure_dir("services/ingestion_worker/sources/sports_reference")
    ensure_dir("services/ingestion_worker/normalizers")
    ensure_dir("services/ingestion_worker/loaders")
    ensure_dir("services/ingestion_worker/pipelines")
    ensure_dir("services/ingestion_worker/registry")
    ensure_dir("services/ingestion_worker/utils")

    source_registry = """
SOURCE_REGISTRY = {
    "teams": ["espn"],
    "rosters": ["espn"],
    "schedules": ["espn"],
    "boxscores": ["espn"],
    "player_logs": ["espn"],
    "injuries": ["manual"],
    "advanced_metrics": ["sports_reference", "manual"],
}
"""

    http_utils = """
from __future__ import annotations

import requests


def get_json(url: str, timeout: int = 30) -> dict:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def get_text(url: str, timeout: int = 30) -> str:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text
"""

    espn_teams = """
from services.ingestion_worker.utils.http import get_json


def fetch_espn_teams() -> dict:
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams"
    return get_json(url)
"""

    espn_rosters = """
from services.ingestion_worker.utils.http import get_json


def fetch_espn_roster(team_id: str) -> dict:
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/roster"
    return get_json(url)
"""

    espn_schedules = """
from services.ingestion_worker.utils.http import get_json


def fetch_espn_schedule(team_id: str, season: int) -> dict:
    url = (
        f"https://site.api.espn.com/apis/site/v2/sports/basketball/"
        f"mens-college-basketball/teams/{team_id}/schedule?season={season}"
    )
    return get_json(url)
"""

    espn_boxscores = """
from services.ingestion_worker.utils.http import get_json


def fetch_espn_summary(event_id: str) -> dict:
    url = (
        f"https://site.api.espn.com/apis/site/v2/sports/basketball/"
        f"mens-college-basketball/summary?event={event_id}"
    )
    return get_json(url)
"""

    normalizer_teams = """
from __future__ import annotations


def normalize_teams(payload: dict) -> list[dict]:
    teams = []

    sports = payload.get("sports", [])
    if not sports:
        return teams

    leagues = sports[0].get("leagues", [])
    if not leagues:
        return teams

    for row in leagues[0].get("teams", []):
        team = row.get("team", {})
        teams.append(
            {
                "external_source": "espn",
                "external_id": str(team.get("id")),
                "name": team.get("displayName", ""),
                "short_name": team.get("shortDisplayName"),
                "abbreviation": team.get("abbreviation"),
                "slug": f"espn-{team.get('id')}",
            }
        )

    return teams
"""

    normalizer_rosters = """
from __future__ import annotations


def normalize_roster(payload: dict, team_external_id: str) -> list[dict]:
    players = []

    for athlete_group in payload.get("athletes", []):
        for athlete in athlete_group.get("items", []):
            players.append(
                {
                    "external_source": "espn",
                    "external_id": str(athlete.get("id")),
                    "team_external_id": team_external_id,
                    "full_name": athlete.get("displayName", ""),
                    "position": (athlete.get("position") or {}).get("abbreviation"),
                    "class_year": (athlete.get("experience") or {}).get("name"),
                }
            )

    return players
"""

    normalizer_schedules = """
from __future__ import annotations


def normalize_schedule(payload: dict, season: int) -> list[dict]:
    games = []

    for event in payload.get("events", []):
        competitions = event.get("competitions", [])
        if not competitions:
            continue

        competition = competitions[0]
        competitors = competition.get("competitors", [])
        if len(competitors) != 2:
            continue

        home = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
        away = next((c for c in competitors if c.get("homeAway") == "away"), competitors[-1])

        games.append(
            {
                "external_source": "espn",
                "external_id": str(event.get("id")),
                "season": season,
                "game_date": event.get("date"),
                "home_team_external_id": str(home.get("team", {}).get("id")),
                "away_team_external_id": str(away.get("team", {}).get("id")),
                "neutral_site": bool(competition.get("neutralSite", False)),
                "location": (competition.get("venue") or {}).get("fullName"),
            }
        )

    return games
"""

    team_loader = """
from sqlalchemy import text
from packages.db.engine import engine


def upsert_teams(records: list[dict]) -> None:
    sql = text(
        '''
        INSERT INTO teams (name, slug)
        VALUES (:name, :slug)
        ON CONFLICT (slug)
        DO UPDATE SET name = EXCLUDED.name
        '''
    )

    with engine.begin() as conn:
        for record in records:
            conn.execute(
                sql,
                {
                    "name": record["name"],
                    "slug": record["slug"],
                },
            )
"""

    player_loader = """
from sqlalchemy import text
from packages.db.engine import engine


def upsert_players(records: list[dict]) -> None:
    sql = text(
        '''
        INSERT INTO players (team_id, full_name, position, class_year)
        SELECT t.id, :full_name, :position, :class_year
        FROM teams t
        WHERE t.slug = :team_slug
        ON CONFLICT DO NOTHING
        '''
    )

    with engine.begin() as conn:
        for record in records:
            conn.execute(
                sql,
                {
                    "team_slug": f"espn-{record['team_external_id']}",
                    "full_name": record["full_name"],
                    "position": record["position"],
                    "class_year": record["class_year"],
                },
            )
"""

    game_loader = """
from sqlalchemy import text
from packages.db.engine import engine


def upsert_games(records: list[dict]) -> None:
    sql = text(
        '''
        INSERT INTO games (
            season,
            game_date,
            home_team_id,
            away_team_id,
            neutral_site,
            location
        )
        SELECT
            :season,
            CAST(:game_date AS TIMESTAMP),
            ht.id,
            at.id,
            :neutral_site,
            :location
        FROM teams ht, teams at
        WHERE ht.slug = :home_slug
          AND at.slug = :away_slug
        ON CONFLICT DO NOTHING
        '''
    )

    with engine.begin() as conn:
        for record in records:
            conn.execute(
                sql,
                {
                    "season": record["season"],
                    "game_date": record["game_date"],
                    "home_slug": f"espn-{record['home_team_external_id']}",
                    "away_slug": f"espn-{record['away_team_external_id']}",
                    "neutral_site": record["neutral_site"],
                    "location": record["location"],
                },
            )
"""

    teams_pipeline = """
from services.ingestion_worker.sources.espn.teams import fetch_espn_teams
from services.ingestion_worker.normalizers.teams import normalize_teams
from services.ingestion_worker.loaders.team_loader import upsert_teams


def run_teams_pipeline() -> list[dict]:
    raw = fetch_espn_teams()
    records = normalize_teams(raw)
    upsert_teams(records)
    print(f"Teams pipeline complete: {len(records)} teams")
    return records
"""

    rosters_pipeline = """
from services.ingestion_worker.sources.espn.rosters import fetch_espn_roster
from services.ingestion_worker.normalizers.rosters import normalize_roster
from services.ingestion_worker.loaders.player_loader import upsert_players


def run_roster_pipeline(team_external_id: str) -> list[dict]:
    raw = fetch_espn_roster(team_external_id)
    records = normalize_roster(raw, team_external_id=team_external_id)
    upsert_players(records)
    print(f"Roster pipeline complete for team {team_external_id}: {len(records)} players")
    return records
"""

    schedules_pipeline = """
from services.ingestion_worker.sources.espn.schedules import fetch_espn_schedule
from services.ingestion_worker.normalizers.schedules import normalize_schedule
from services.ingestion_worker.loaders.game_loader import upsert_games


def run_schedule_pipeline(team_external_id: str, season: int) -> list[dict]:
    raw = fetch_espn_schedule(team_external_id, season)
    records = normalize_schedule(raw, season=season)
    upsert_games(records)
    print(f"Schedule pipeline complete for team {team_external_id}: {len(records)} games")
    return records
"""

    master_pipeline = """
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
"""

    write_file("services/ingestion_worker/registry/source_registry.py", source_registry)
    write_file("services/ingestion_worker/utils/http.py", http_utils)

    write_file("services/ingestion_worker/sources/espn/teams.py", espn_teams)
    write_file("services/ingestion_worker/sources/espn/rosters.py", espn_rosters)
    write_file("services/ingestion_worker/sources/espn/schedules.py", espn_schedules)
    write_file("services/ingestion_worker/sources/espn/boxscores.py", espn_boxscores)

    write_file("services/ingestion_worker/normalizers/teams.py", normalizer_teams)
    write_file("services/ingestion_worker/normalizers/rosters.py", normalizer_rosters)
    write_file("services/ingestion_worker/normalizers/schedules.py", normalizer_schedules)

    write_file("services/ingestion_worker/loaders/team_loader.py", team_loader)
    write_file("services/ingestion_worker/loaders/player_loader.py", player_loader)
    write_file("services/ingestion_worker/loaders/game_loader.py", game_loader)

    write_file("services/ingestion_worker/pipelines/teams_pipeline.py", teams_pipeline)
    write_file("services/ingestion_worker/pipelines/rosters_pipeline.py", rosters_pipeline)
    write_file("services/ingestion_worker/pipelines/schedules_pipeline.py", schedules_pipeline)
    write_file("services/ingestion_worker/pipelines/full_harvest.py", master_pipeline)