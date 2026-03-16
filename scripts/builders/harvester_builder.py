from utils.file_utils import write_file

def build_harvester():
    print("Building harvester architecture...")

    source_base = """
from abc import ABC, abstractmethod
from typing import Any

class BaseSourceAdapter(ABC):
    source_name: str = "base"

    @abstractmethod
    def fetch(self, **kwargs) -> Any:
        raise NotImplementedError
"""

    models = """
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
"""

    registry = """
PIPELINE_REGISTRY = {
    "teams": "services/ingestion-worker/pipelines/teams_pipeline.py",
    "rosters": "services/ingestion-worker/pipelines/rosters_pipeline.py",
    "schedules": "services/ingestion-worker/pipelines/schedules_pipeline.py",
    "boxscores": "services/ingestion-worker/pipelines/boxscores_pipeline.py",
    "metrics": "services/ingestion-worker/pipelines/metrics_pipeline.py",
}
"""

    write_file("services/ingestion-worker/sources/base.py", source_base)
    write_file("services/ingestion-worker/models/records.py", models)
    write_file("services/ingestion-worker/registry/pipelines.py", registry)