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
from puffotter.flask.base import db
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.exceptions import ActionException
from bundesliga_tippspiel.enums import ReminderType
from bundesliga_tippspiel.db.settings.ReminderSettings import ReminderSettings


class SetReminderSettingsAction(Action):
    """
    Action that allows setting reminder settings
    """

    def __init__(self, hours: int, reminder_states: Dict[ReminderType, bool]):
        """
        Initializes the SetReminderSettingsAction object
        :param hours: How many hours before the match the user wants a reminder
        :param reminder_states: specifies the states for each of the reminder
                                types
        """
        self.hours = int(hours)
        self.reminder_states = reminder_states

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
        reminders = {
            x.reminder_type: x for x in
            ReminderSettings.query.filter_by(user_id=current_user.id).all()
        }

        seconds = self.hours * 60 * 60

        for reminder_type, active in self.reminder_states.items():
            reminder = reminders.get(reminder_type)
            if reminder is None:
                reminder = ReminderSettings(
                    user=current_user,
                    reminder_time=seconds,
                    reminder_type=reminder_type,
                    active=active
                )
                db.session.add(reminder)
            else:
                reminder.active = active
                reminder.reminder_time = seconds

        db.session.commit()
        return {}

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        reminder_states = {
            reminder_type: data.get(reminder_type.value) in ["on", True]
            for reminder_type in ReminderType
        }
        return cls(
            hours=data["hours"],
            reminder_states=reminder_states
        )
