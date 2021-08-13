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

from flask import Blueprint, request, flash, redirect, url_for, \
    make_response, abort
from flask_login import login_required, current_user
from jerrycan.base import db, app
from jerrycan.enums import AlertSeverity
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.db import Team, UserProfile
from bundesliga_tippspiel.db.settings.DisplayBotsSettings import \
    DisplayBotsSettings
from bundesliga_tippspiel.db.settings.ReminderSettings import \
    ReminderSettings
from bundesliga_tippspiel.enums import ReminderType


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
        setting = DisplayBotsSettings(
            user_id=current_user.id,
            display_bots=request.form.get("display_bots", "off") == "on"
        )
        db.session.merge(setting)
        db.session.commit()

        flash("Einstellungen gespeichert", AlertSeverity.SUCCESS.value)
        return redirect(url_for("user_management.profile"))

    @blueprint.route("/set_reminder", methods=["POST"])
    @login_required
    def set_reminder():
        """
        Allows the user to set an email reminder
        :return: The response
        """
        hours = int(request.form["hours"])
        reminder_states = {
            reminder_type:
                request.form.get(reminder_type.value) in ["on", True]
            for reminder_type in ReminderType
        }

        if not 0 < hours < 49:
            flash("Ungültige Anzahl Stunden eingegeben", "danger")
        else:
            for reminder_type, reminder_state in reminder_states.items():
                setting = ReminderSettings(
                    user_id=current_user.id,
                    reminder_type=reminder_type,
                    active=reminder_state,
                    reminder_time=hours
                )
                db.session.merge(setting)
            db.session.commit()
            flash("Erinnerungseinstellungen gespeichert", "success")

        return redirect(url_for("user_management.profile"))

    @blueprint.route("/change_league", methods=["GET"])
    @login_required
    def change_league():
        """
        Changes the user's currently displayed league by storing these
        values in a cookie
        :return: None
        """
        try:
            league = request.args.get("league", Config.OPENLIGADB_LEAGUE)
            season = request.args.get("season", Config.OPENLIGADB_SEASON)
            int(season)
        except ValueError:
            return abort(400)
        app.logger.info(request.referrer)
        response = make_response(redirect(url_for("betting.get_current_bets")))
        response.set_cookie("league", league)
        response.set_cookie("season", season)
        return response

    @blueprint.route("/set_profile_info", methods=["POST"])
    @login_required
    def set_profile_info():
        """
        Sets the profile info for a user
        :return: The response
        """
        team_names = [x.abbreviation for x in Team.query.all()]

        description = request.form.get("about_me")
        favourite_team = request.form.get("favourite_team")
        if not description:
            description = None
        if favourite_team not in team_names:
            favourite_team = None
        country = None

        profile_info = UserProfile(
            user_id=current_user.id,
            description=description,
            favourite_team_abbreviation=favourite_team,
            country=country
        )
        db.session.merge(profile_info)
        db.session.commit()
        return redirect(url_for("user_management.profile"))

    return blueprint
