from utils.file_utils import write_file, ensure_dir


def build_dashboard():

    print("Building dashboard shell...")

    ensure_dir("apps/dashboard/public")
    ensure_dir("apps/dashboard/public/data")

    readme = """
# Dashboard

This application will visualize simulation results, matchup stories,
player projections, bracket odds, and published tournament data.

Published JSON files are synced into:

- public/data/matchups
- public/data/players
- public/data/brackets
- public/data/dashboard
"""

    data_readme = """
This directory contains published JSON assets copied from data/published.

Netlify can serve these files directly from the dashboard app.
"""

    write_file("apps/dashboard/README.md", readme)
    write_file("apps/dashboard/public/data/README.md", data_readme)