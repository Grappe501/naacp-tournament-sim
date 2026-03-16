import json
from pathlib import Path


def export_matchup_story(slug, narrative_payload):

    path = Path("data/simulation-outputs/narratives")

    path.mkdir(parents=True, exist_ok=True)

    file_path = path / f"{slug}.json"

    file_path.write_text(
        json.dumps(narrative_payload, indent=2),
        encoding="utf-8"
    )
