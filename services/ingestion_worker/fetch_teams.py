import requests

def fetch_teams():

    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams"

    r = requests.get(url)

    data = r.json()

    teams = []

    for t in data.get("sports", [])[0].get("leagues", [])[0].get("teams", []):

        team = t["team"]

        teams.append({
            "id": team["id"],
            "name": team["displayName"],
            "abbrev": team["abbreviation"]
        })

    return teams


if __name__ == "__main__":

    teams = fetch_teams()

    print("Teams fetched:", len(teams))
