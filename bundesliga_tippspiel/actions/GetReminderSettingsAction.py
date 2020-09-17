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
from bundesliga_tippspiel.enums import ReminderType
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.db.settings.ReminderSettings import ReminderSettings


class GetReminderSettingsAction(Action):
    """
    Action that allows retrieving the user's reminder settings
    """

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        pass

    def _execute(self) -> Dict[str, Any]:
        """
        Retrieves reminder settings
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        reminders = {
            x.reminder_type: x for x in
            ReminderSettings.query.filter_by(user_id=current_user.id).all()
        }
        return {
            "settings": {
                reminder_type: reminders.get(reminder_type)
                for reminder_type in ReminderType
            }
        }

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls()
