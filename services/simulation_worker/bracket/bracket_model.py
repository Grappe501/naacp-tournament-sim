from dataclasses import dataclass


@dataclass
class BracketGame:
    game_id: int
    round_name: str
    team_a_id: int
    team_b_id: int
