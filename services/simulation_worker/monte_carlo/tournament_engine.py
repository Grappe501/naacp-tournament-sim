from __future__ import annotations

from collections import Counter


def rank_top_brackets(bracket_results: list[dict], top_n: int = 10) -> list[dict]:
    counter = Counter()

    for bracket in bracket_results:
        key = tuple(bracket.get("picks", []))
        counter[key] += 1

    ranked = []
    total = max(1, sum(counter.values()))

    for picks, count in counter.most_common(top_n):
        ranked.append(
            {
                "picks": list(picks),
                "frequency": count,
                "probability_pct": round((count / total) * 100, 4),
            }
        )

    return ranked
