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

from flask import Blueprint
from flask_login import login_required
from bundesliga_tippspiel.actions.ChangeSettingsAction import \
    ChangeSettingsAction


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/misc_settings", methods=["POST"])
    @login_required
    def misc_settings():
        """
        Allows the user to change their miscellaneous settings
        :return: The response
        """
        action = ChangeSettingsAction.from_site_request()
        return action.execute_with_redirects(
            "user_management.profile",
            "Einstellungen gespeichert",
            "user_management.profile"
        )

    return blueprint
