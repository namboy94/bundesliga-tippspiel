import csv

def load_csv(path: str):
    with open(path) as f:
        lines = [x for x in csv.reader(f)]
        header = lines.pop(0)
        return {
            x[0]: {
                header[i]: x[i] for i in range(1, len(x))
            } for x in lines}


bets = load_csv("bl_tables/bets.csv")
users = load_csv("bl_tables/users.csv")
matches = load_csv("bl_tables/matches.csv")
teams = load_csv("bl_tables/teams.csv")

teamname_map = {
    "VFL": "WOB",
    "SVW": "BRE",
    "SCU": "FCU",
    "PAD": "SCP",
    "FCK": "KOE",
    "BIE": "DSC"
}

formatted_bets = []

for bet in bets.values():
    match = matches[bet["match_id"]]
    home_team = teams[match["home_team_id"]]
    home_team_abb = teamname_map.get(home_team["abbreviation"], home_team["abbreviation"])
    away_team = teams[match["away_team_id"]]
    away_team_abb = teamname_map.get(away_team["abbreviation"], away_team["abbreviation"])

    league = "bl1"
    season = match["season"]
    matchday = match["matchday"]
    home = home_team_abb
    away = away_team_abb
    user_id = bet["user_id"]
    home_score = bet["home_score"]
    away_score = bet["away_score"]

    item = (
        league, season, matchday, home, away, user_id, home_score, away_score, None
    )
    formatted_bets.append(item)

formatted_bets.sort(key=lambda x: x[2])
formatted_bets = [("league", "season", "matchday",
                   "home_team_abbreviation", "away_team_abbreviation",
                   "user_id", "home_score", "away_score", "points"
                   )] + formatted_bets
from pprint import pprint
pprint(formatted_bets[0:2])

with open("bets.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(formatted_bets)