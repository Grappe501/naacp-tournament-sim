from utils.file_utils import write_file, ensure_dir


def build_publishing():

    print("Building publishing engine...")

    ensure_dir("services/publishing")
    ensure_dir("data/published")
    ensure_dir("data/published/matchups")
    ensure_dir("data/published/players")
    ensure_dir("data/published/brackets")
    ensure_dir("data/published/dashboard")

    write_file("services/publishing/__init__.py", "")

    export_matchup_page = """
import json
from pathlib import Path


def publish_matchup_page(slug: str, matchup_payload: dict, narrative_payload: dict) -> None:
    output_dir = Path("data/published/matchups")
    output_dir.mkdir(parents=True, exist_ok=True)

    page_payload = {
        "slug": slug,
        "matchup": matchup_payload,
        "narrative": narrative_payload,
    }

    target = output_dir / f"{slug}.json"
    target.write_text(json.dumps(page_payload, indent=2), encoding="utf-8")
"""

    export_player_projection = """
import json
from pathlib import Path


def publish_player_projections(slug: str, player_payload: dict) -> None:
    output_dir = Path("data/published/players")
    output_dir.mkdir(parents=True, exist_ok=True)

    target = output_dir / f"{slug}.json"
    target.write_text(json.dumps(player_payload, indent=2), encoding="utf-8")
"""

    export_bracket_probabilities = """
import json
from pathlib import Path


def publish_bracket_probabilities(payload: dict) -> None:
    output_dir = Path("data/published/brackets")
    output_dir.mkdir(parents=True, exist_ok=True)

    target = output_dir / "tournament_probabilities.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
"""

    export_dashboard_data = """
import json
from pathlib import Path


def publish_dashboard_data(payload: dict) -> None:
    output_dir = Path("data/published/dashboard")
    output_dir.mkdir(parents=True, exist_ok=True)

    target = output_dir / "dashboard_data.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
"""

    netlify_sync = """
from pathlib import Path
import shutil


def sync_published_data_to_dashboard() -> None:
    source = Path("data/published")
    target = Path("apps/dashboard/public/data")

    target.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        print("No published data found to sync.")
        return

    for item in source.rglob("*"):
        if item.is_dir():
            continue

        relative = item.relative_to(source)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, destination)

    print("Published data synced to dashboard public/data")
"""

    publishing_runner = """
from services.publishing.export_matchup_page import publish_matchup_page
from services.publishing.export_player_projection import publish_player_projections
from services.publishing.export_bracket_probabilities import publish_bracket_probabilities
from services.publishing.export_dashboard_data import publish_dashboard_data
from services.publishing.netlify_sync import sync_published_data_to_dashboard


def run_publishing_demo():
    slug = "play-in-team-a-vs-play-in-team-b"

    matchup_payload = {
        "team_a": "Play-In Team A",
        "team_b": "Play-In Team B",
        "team_a_win_pct": 61.3,
        "team_b_win_pct": 38.7,
        "avg_team_a_score": 74.2,
        "avg_team_b_score": 69.1,
        "avg_margin": 5.1,
        "projected_winner": "Play-In Team A",
    }

    narrative_payload = {
        "summary": "Play-In Team A holds a moderate edge due to stronger offense and better recent form.",
        "details": [
            "Play-In Team A offense rating: 112.4",
            "Play-In Team B offense rating: 108.1",
            "Projected score: 74.2 - 69.1",
            "Simulation variance still leaves room for an upset.",
        ],
    }

    player_payload = {
        "players": [
            {
                "player_name": "Player One",
                "points": 18.4,
                "rebounds": 6.2,
                "assists": 3.7,
            },
            {
                "player_name": "Player Two",
                "points": 14.1,
                "rebounds": 7.0,
                "assists": 2.4,
            },
        ]
    }

    bracket_payload = {
        "championship_odds": [
            {"team": "Play-In Team A", "probability_pct": 4.2},
            {"team": "Play-In Team B", "probability_pct": 2.7},
        ],
        "final_four_odds": [
            {"team": "Play-In Team A", "probability_pct": 13.1},
            {"team": "Play-In Team B", "probability_pct": 9.8},
        ],
    }

    dashboard_payload = {
        "featured_matchup_slug": slug,
        "top_bracket_summary": bracket_payload,
        "headline": "Latest Tournament Simulation Results",
    }

    publish_matchup_page(slug, matchup_payload, narrative_payload)
    publish_player_projections(slug, player_payload)
    publish_bracket_probabilities(bracket_payload)
    publish_dashboard_data(dashboard_payload)
    sync_published_data_to_dashboard()

    print("Publishing demo complete.")


if __name__ == "__main__":
    run_publishing_demo()
"""

    write_file("services/publishing/export_matchup_page.py", export_matchup_page)
    write_file("services/publishing/export_player_projection.py", export_player_projection)
    write_file("services/publishing/export_bracket_probabilities.py", export_bracket_probabilities)
    write_file("services/publishing/export_dashboard_data.py", export_dashboard_data)
    write_file("services/publishing/netlify_sync.py", netlify_sync)
    write_file("services/publishing/run_publishing_demo.py", publishing_runner)