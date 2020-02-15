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

from typing import Dict, Tuple, Callable
from bundesliga_tippspiel.flask import app
from bundesliga_tippspiel.utils.match_data_getter import update_db_data
from bundesliga_tippspiel.actions.SendDueEmailRemindersAction import \
    SendDueEmailRemindersAction


def _update_db_data():
    """
    Updates database data
    :return: None
    """
    with app.app_context():
        update_db_data()


def _send_due_email_reminders():
    """
    Sends out due email reminders
    :return: None
    """
    with app.app_context():
        SendDueEmailRemindersAction().execute()


bg_tasks: Dict[str, Tuple[int, Callable]] = {
    "update_db_data": (30, _update_db_data),
    "send_due_reminders": (60, _send_due_email_reminders)
}
"""
A dictionary containing background tasks for the flask application
"""
