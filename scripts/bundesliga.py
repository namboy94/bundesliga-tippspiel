#!/usr/bin/env python

""" Copyright Hermann Krumrey <hermann@krumreyh.com> 2017

    This file is part of bundesliga-tippspiel.

    bundesliga-tippspiel is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    bundesliga-tippspiel is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import time
import json
import MySQLdb
import requests

def load(season='2016', league='bl1'):

    base_url = "https://www.openligadb.de/api/getmatchdata/bl1/"
    matchdays = []
    data = json.loads(requests.get(base_url + season).text)

    for day in range(1, 35):
        matchday = []
        for match in data:
            if match["Group"]["GroupOrderID"] == day:
                matchday.append(match)
        matchdays.append(matchday)

    return matchdays

def update_db(username, password):

    data = load()
    db = connect_db(username, password)

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

            if match["Location"] is not None:
                match_location_city = match["Location"]["LocationCity"]
                match_location_stadium = match["Location"]["LocationStadium"]
            else:
                match_location_city = "Unknown"
                match_location_stadium = "Unknown"

            match_time = match["MatchDateTimeUTC"]
            match_finished = match["MatchIsFinished"]
            team_one = match["Team1"]["TeamId"]
            team_two = match["Team2"]["TeamId"]

            if len(match["MatchResults"]) > 0:
                team_one_halftime_points = \
                    match["MatchResults"][0]["PointsTeam1"]
                team_two_halftime_points = \
                    match["MatchResults"][0]["PointsTeam2"]
            else:
                team_one_halftime_points = -1
                team_two_halftime_points = -1

            if len(match["MatchResults"]) > 1:
                team_one_points = match["MatchResults"][1]["PointsTeam1"]
                team_two_points = match["MatchResults"][1]["PointsTeam2"]
            else:
                team_one_points = -1
                team_two_points = -1

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
    print("Update: " + str(time.time()))
