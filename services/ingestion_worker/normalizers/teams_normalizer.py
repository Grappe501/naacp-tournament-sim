from typing import List
from services.ingestion-worker.models.records import TeamRecord

def normalize_espn_teams(payload: dict) -> List[TeamRecord]:
    teams = []
    sports = payload.get("sports", [])
    if not sports:
        return teams

    leagues = sports[0].get("leagues", [])
    if not leagues:
        return teams

    raw_teams = leagues[0].get("teams", [])
    for row in raw_teams:
        team = row.get("team", {})
        teams.append(
            TeamRecord(
                external_id=str(team.get("id")),
                name=team.get("displayName", ""),
                short_name=team.get("shortDisplayName"),
                abbreviation=team.get("abbreviation"),
            )
        )
    return teams
