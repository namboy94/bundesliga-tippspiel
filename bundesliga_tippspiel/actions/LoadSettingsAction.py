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
from bundesliga_tippspiel.db.settings.DisplayBotsSettings import \
    DisplayBotsSettings


class LoadSettingsAction(Action):
    """
    Action that retrieves miscellaneous settings for the current user
    """

    def __init__(self):
        """
        Initializes the LoadSettingsAction object
        :raises: ActionException if any problems occur
        """
        pass

    def validate_data(self):
        """
        Validates data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        pass

    def _execute(self) -> Dict[str, Any]:
        """
        Retrieves the settings from the database
        (or initializes them with default values)
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        display_bots_setting = DisplayBotsSettings.query. \
            filter_by(user=current_user).first()
        if display_bots_setting is None:
            display_bots_setting = DisplayBotsSettings(
                user=current_user,
                display_bots=False
            )
            db.session.add(display_bots_setting)
        db.session.commit()
        return {
            "display_bots": display_bots_setting.display_bots
        }

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls()
