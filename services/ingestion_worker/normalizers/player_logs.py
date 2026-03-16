from __future__ import annotations


def normalize_player_logs(payload: dict, player_external_id: str):

    games = []

    events = payload.get("events", [])

    for event in events:

        stats = event.get("stats", [])

        row = {
            "external_player_id": player_external_id,
            "game_id": event.get("eventId"),
            "minutes": stats[0] if len(stats) > 0 else None,
            "points": stats[1] if len(stats) > 1 else None,
            "rebounds": stats[2] if len(stats) > 2 else None,
            "assists": stats[3] if len(stats) > 3 else None,
            "steals": stats[4] if len(stats) > 4 else None,
            "blocks": stats[5] if len(stats) > 5 else None,
            "turnovers": stats[6] if len(stats) > 6 else None,
            "fouls": stats[7] if len(stats) > 7 else None,
        }

        games.append(row)

    return games
