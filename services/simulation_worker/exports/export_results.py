import json
from pathlib import Path


def export_matchup_result(payload: dict, slug: str) -> None:
    output_dir = Path("data/simulation-outputs/matchups")
    output_dir.mkdir(parents=True, exist_ok=True)

    target = output_dir / f"{slug}.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def export_bracket_top_10(payload: dict) -> None:
    output_dir = Path("data/simulation-outputs/brackets")
    output_dir.mkdir(parents=True, exist_ok=True)

    target = output_dir / "top_10_brackets.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
