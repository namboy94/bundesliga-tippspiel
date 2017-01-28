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
import MySQLdb


def update_db(user, password):
    db = connect_db(user, password)
    matches = get_matches(db)
    bets = get_bets(db)

    for bet in bets:
        if bet[4] == -1:

            match = matches[bet[1]]
            if match[0]:
                points = calculate_points(bet[2], bet[3], match[2], match[3])

                stmt = db.cursor()
                stmt.execute("UPDATE bets SET points=%s "\
                    "WHERE user=%s AND match_id=%s", (points, bet[0], bet[1]))

    update_leaderboard(db)

    db.commit()
    db.close()

def calculate_points(bet_one, bet_two, actual_one, actual_two):

    points = 0
    if bet_one == actual_one:
        points += 1
    if bet_two == actual_two:
        points += 1
    if bet_one - bet_two == actual_one - actual_two:
        points += 1

    if bet_one > bet_two and actual_one > actual_two:
        points += 1
    elif bet_one == bet_two and actual_one == actual_two:
        points += 1
    elif bet_one < bet_two and actual_one < actual_two:
        points += 1

    if bet_one == actual_one and bet_two == actual_two:
        points += 1

    return points


def connect_db(username, password):

    db = MySQLdb.connect("localhost",
                         username,
                         password,
                         "bundesliga_tippspiel")

    return db

def get_matches(db):

    stmt = db.cursor()
    stmt.execute("SELECT id, finished, team_one_ft, team_two_ft FROM matches");
    raw = stmt.fetchall()

    matches = {}
    for match in raw:
        matches[match[0]] = match
    return matches

def get_bets(db):

    stmt = db.cursor()
    stmt.execute(
        "SELECT user, match_id, team_one, team_two, points FROM bets");
    return stmt.fetchall()

def update_leaderboard(db):

    stmt = db.cursor()
    stmt.execute("SELECT * FROM users")
    users = stmt.fetchall()

    for user in users:
        stmt = db.cursor()
        stmt.execute("SELECT SUM(points) FROM bets WHERE user=%s", (user[0],))
        points = stmt.fetchall()[0][0]

        if points is None:
            points = 0

        stmt = db.cursor()
        stmt.execute("SELECT * FROM leaderboard WHERE user_id=%s", (user[0],))
        user_exists = len(stmt.fetchall()) > 0

        stmt = db.cursor()
        if user_exists:
            stmt.execute("UPDATE leaderboard SET points=%s WHERE user_id=%s", 
                (points, user[0]))
        else:
            stmt.execute("INSERT INTO leaderboard VALUES (%s, %s)", 
                (user[0], points))


if __name__ == "__main__":
    update_db(sys.argv[1], sys.argv[2])
