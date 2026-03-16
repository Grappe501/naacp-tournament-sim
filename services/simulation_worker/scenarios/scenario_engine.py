def build_scenarios(base_record: dict) -> list[dict]:
    return [
        {
            "scenario_key": "baseline",
            "label": "Baseline",
            "injury_multiplier": 1.0,
            "variance_multiplier": 1.0,
        },
        {
            "scenario_key": "high_variance",
            "label": "High Variance",
            "injury_multiplier": 1.0,
            "variance_multiplier": 1.25,
        },
        {
            "scenario_key": "injury_stress",
            "label": "Injury Stress",
            "injury_multiplier": 1.5,
            "variance_multiplier": 1.0,
        },
        {
            "scenario_key": "chaos_mode",
            "label": "Chaos Mode",
            "injury_multiplier": 1.35,
            "variance_multiplier": 1.35,
        },
    ]
