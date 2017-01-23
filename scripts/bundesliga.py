import json
import MySQLdb
import requests

def load(season='2016', league='bl1'):

    base_url = "https://www.openligadb.de/api/getmatchdata/bl1/"
    matchdays = []
    data = json.loads(requests.get(base_url + season))

    for day in range(1, 35):
        matchday = []
        for match in data:
            if match["Group"]["GroupOrderId"] == day:
                matchday.append(match)
        matchdays.append(matchday)

    return matchdays

def update_db():

    data = load()
    db = connect_db()

    update_db_teams(data, db)
    update_db_matches(data, db)
    db.close()

def update_db_teams(data, db):

    current_data = get_current_teams(db)
    committed = False

    teams = []
    for match in data[0]:

        teams.append(match["Team1"])
        teams.append(match["Team2"])

    for team in teams:

        if not team["TeamId"] in current_data:

            stmt = db.cursor()
            stmt.execute("INSERT INTO teams (id, name, shortname, icon)"\
                         "VALUES (%s, %s, %s, %s);",
                         (team["TeamId"], team["TeamName"], team["ShortName"],
                            team["TeamIconUrl"]))
            committed = True

    if committed:
        db.commit()


def update_db_matches(data, db):

    committed = False
    current_data = get_current_matches(db)

    for i, day in enumerate(data):

        for match in day:

            matchday = i + 1
            match_id = match["MatchID"]
            match_location_city = match["Location"]["LocationCity"]
            match_location_stadium = match["Location"]["LocationStadium"]
            match_time = match["MatchDateTimeUTC"]
            match_finished = match["MatchIsFinished"]
            team_one = match["Team1"]["TeamId"]
            team_two = match["Team2"]["TeamId"]
            team_one_halftime_points = match["MatchResults"][0]["PointsTeam1"]
            team_two_halftime_points = match["MatchResults"][0]["PointsTeam2"]
            team_one_points = match["MatchResults"][1]["PointsTeam1"]
            team_two_points = match["MatchResults"][1]["PointsTeam2"]
            last_update = match["LastUpdateDateTime"]

            sql = ""
            variables = (match_id, matchday, match_location_city,
                         match_location_stadium, match_time, match_finished,
                         team_one, team_two, team_one_halftime_points,
                         team_two_halftime_points, team_one_points,
                         team_two_points, str(last_update))

            if match_id not in current_data:
                sql = "INSERT INTO matches (id, matchday, city, stadium, "\
                      "matchtime, finished, team_one, team_two, team_one_ht, "\
                      "team_two_ht, team_one_ft, team_two_ft, updated) "\
                      "VALUES (%s, %s, %s, %s, %s, "\
                      "%s, %s, %s, %s, %s, %s, %s, %s);"


            elif current_data[match_id] != last_update:
                sql = "UPDATE matches SET id=%s, matchday=%s, city=%s, "\
                      "stadium=%s, matchtime=%s, finished=%s, team_one=%s, "\
                      "team_two=%s, team_one_ht=%s, team_two_ht=%s, "\
                      "team_one_ft=%s, team_two_ft=%s, updated=%s WHERE id=%s"
                variables += (match_id,)

            if sql != "":

                stmt = db.cursor()
                stmt.execute(sql, variables)
                committed = True
    if committed:
        db.commit()

def get_current_matches(db):
    stmt = db.cursor()
    stmt.execute("SELECT id, updated FROM matches")
    current_data = stmt.fetchall()

    formatted_data = {}

    for match in current_data:
        formatted_data[match[0]] = match[1]

    return formatted_data

def get_current_teams(db):
    stmt = db.cursor()
    stmt.execute("SELECT id FROM teams")
    current_data = stmt.fetchall()

    team_ids = []
    for team in current_data:
        team_ids.append(team[0])

    return team_ids


def connect_db(username, password):

    db = MySQLdb.connect("localhost",
                         username,
                         password,
                         "bundesliga_tippspiel")

    return db


if __name__ == "__main__":
    update_db(sys.argv[1], sys.argv[2])
