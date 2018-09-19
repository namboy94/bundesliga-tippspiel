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

from typing import Dict, Any
from flask_login import current_user
from bundesliga_tippspiel import db
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.types.exceptions import ActionException
from bundesliga_tippspiel.models.user_generated.EmailReminder import \
    EmailReminder


class SetEmailReminderAction(Action):
    """
    Action that allows setting an email reminder
    """

    def __init__(self, hours: int, active: bool):
        """
        Initializes the SetEmailReminderAction object
        :param hours: How many hours before the match the user wants a reminder
        :param active: Defines whether or not the reminder is active or not
        """
        self.hours = int(hours)
        self.active = bool(active)

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        if not 0 < self.hours < 49:
            raise ActionException(
                "invalid reminder hours",
                "Ungültige Anzahl Stunden eingegeben"
            )

    def _execute(self) -> Dict[str, Any]:
        """
        Confirms a previously registered user
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        reminder = \
            EmailReminder.query.filter_by(user_id=current_user.id).first()

        if self.active:

            if reminder is None:
                reminder = EmailReminder(user=current_user)
                db.session.add(reminder)

            reminder.reminder_time = self.hours * 60 * 60

        else:
            if reminder is not None:
                db.session.delete(reminder)

        db.session.commit()

        return {}

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            hours=data["hours"],
            active=data.get("active") in ["on", True]
        )
