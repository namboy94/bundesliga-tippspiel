"""
Copyright 2017-2018 Hermann Krumrey

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

import json
import requests
import sqlite3
from typing import Dict


def initialize_database(database: sqlite3.Connection):
    """
    Initializes the Database Table for the bundesliga-tippspiel
    reminder service
    :param database: The database connection to use
    :return: None
    """
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection
    database.execute("CREATE TABLE IF NOT EXISTS "
                     "bundesliga_tippspiel_reminder ("
                     "    id INTEGER CONSTRAINT constraint_name PRIMARY KEY,"
                     "    user_id INTEGER NOT NULL,"
                     "    username VARCHAR(255) NOT NULL,"
                     "    address VARCHAR(255),"
                     "    key_hash VARCHAR(255) NOT NULL,"
                     "    verified BOOLEAN NOT NULL,"
                     "    warning_time INTEGER NOT NULL,"
                     "    last_match INTEGER NOT NULL"
                     ")")
    database.commit()


# noinspection SqlNoDataSourceInspection,SqlResolve
def verify(database: sqlite3.Connection, keystring: str, address: str) -> bool:
    """
    Verifies the keystring provided by the user's message
    :param database: The database to use
    :param keystring: The key string to verify
    :param address: The address of the person to verify
    :return: True if the verification was completed, False otherwise
    """

    user_id, key = keystring.split(":", 1)
    user_id = int(user_id)

    query = database.execute(
        "SELECT * FROM bundesliga_tippspiel_reminder "
        "WHERE user_id=?", (user_id,)).fetchall()

    if len(query) != 1:
        return False
    else:
        key_hash = query[0][4]

        if verify_hash(key_hash, key):
            database.execute("UPDATE bundesliga_tippspiel_reminder "
                             "    SET verified=1, address=? "
                             "    WHERE user_id=?",
                             (address, user_id))
            return True
        else:
            return False


def verify_hash(key_hash: str, key: str)-> bool:
    """
    Verifies the key using the key hash
    :param key_hash: The key hash to use
    :param key: The key to check
    :return: True if the key matches, False otherwise
    """
    return True  # TODO Implement


# noinspection SqlResolve,SqlNoDataSourceInspection
def get_subscriptions(database: sqlite3.Connection) \
        -> Dict[int, Dict[str, str or int]]:
    """
    Retrieves all verified subscriptions
    :return: Dictionary of form
             {user_id: {username, address, warning_time, last_match}}
    """
    query = database.execute(
        "SELECT * FROM bundesliga_tippspiel WHERE verified=0"
    ).fetchall()

    subscriptions = {}
    for row in query:
        subscriptions[int(row[1])] = {
            "username": str(row[2]),
            "address": str(row[3]),
            "warning_time": int(row[6]),
            "last_match": int(row[7])
        }

    return subscriptions


def get_next_match(user_id: int) -> Dict[str, str or int]:
    """
    Retrieves the next match that a user HAS NOT YET BET ON
    :param user_id: The ID of the user
    :return: The match data
    """

    response = requests.get(
        "https://hk-tippspiel.com/api/v1/get_next_match.php?user="
        + str(user_id)
    ).text
    return json.loads(response)


def notification_required(database: sqlite3.Connection,
                          user_id: int,
                          next_match: Dict[str, str or int]):

    last_match = database.execute(
        "SELECT last_match "
        "FROM bundesliga_tippspiel_reminder "
        "WHERE user_id=?",
        (user_id,)).fetchall()[0][0]

    if next_match["id"] == last_match:
        return False
    else:
        x = datetime.strptime("2018-05-12T13:30:00Z", "%Y-%m-%dT%H:%M:%SZ")



def acknowledge(database: sqlite3.Connection,
                user_id: int,
                match_id: Dict[str, str or int]):
    """
    Acknowledges that the user was reminded of the match
    :param database: The database connection to use
    :param user_id: The user's ID
    :param match_id: The match to acknowledge
    :return: None
    """
    database.execute("UPDATE bundesliga_tippspiel_reminder "
                     "SET last_match=? "
                     "WHERE user_id=?",
                     (match_id, user_id))
