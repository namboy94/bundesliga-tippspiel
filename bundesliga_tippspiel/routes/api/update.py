"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

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
LICENSE"""

import time
import bundesliga_tippspiel.config as config
from bundesliga_tippspiel import app
from bundesliga_tippspiel.utils.routes import api
from bundesliga_tippspiel.utils.match_data_getter import update_db_data
from bundesliga_tippspiel.actions.SendDueEmailRemindersAction import \
    SendDueEmailRemindersAction


@app.route("/api/v2/update_match_data", methods=["GET"])
@api
def update_match_data():
    """
    Updates the match data. If the last update is less than 100 seconds in the
    past, do not update.
    :return: The JSON response
    """
    needs_update = time.time() - config.last_match_data_update > 100
    if needs_update:
        update_db_data()
        config.last_match_data_update = time.time()
    return {"updated": needs_update}


@app.route("/api/v2/send_due_reminders", methods=["GET"])
@api
def send_due_reminders():
    """
    Sends out all due reminders
    :return: The JSON response
    """
    needs_update = time.time() - config.last_reminder_sending > 1800
    if needs_update:
        SendDueEmailRemindersAction().execute()
        config.last_reminder_sending = time.time()
    return {"updated": needs_update}
