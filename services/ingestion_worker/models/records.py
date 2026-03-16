from dataclasses import dataclass
from typing import Optional

@dataclass
class TeamRecord:
    external_id: str
    name: str
    short_name: Optional[str] = None
    abbreviation: Optional[str] = None
    conference: Optional[str] = None

@dataclass
class PlayerRecord:
    external_id: str
    team_external_id: str
    full_name: str
    position: Optional[str] = None
    class_year: Optional[str] = None

@dataclass
class GameRecord:
    external_id: str
    season: int
    game_date: str
    home_team_external_id: str
    away_team_external_id: str
    neutral_site: bool = False
