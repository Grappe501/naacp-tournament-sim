from collections import Counter


def compute_advancement_probabilities(results):

    counter = Counter()

    for r in results:
        counter[r["projected_winner"]] += 1

    total = sum(counter.values())

    probabilities = {}

    for team, wins in counter.items():
        probabilities[team] = wins / total

    return probabilities
