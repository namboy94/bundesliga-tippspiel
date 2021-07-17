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
from bundesliga_tippspiel.db import Team, UserProfile
from bundesliga_tippspiel.db.settings.DisplayBotsSettings import \
    DisplayBotsSettings
from bundesliga_tippspiel.db.settings.ReminderSettings import ReminderSettings


def profile_extras() -> Dict[str, Any]:
    """
    Makes sure that the profile page has access to information on email
    reminders.
    :return: The variables to forward to the template
    """
    teams = Team.query.all()
    teams.sort(key=lambda x: x.name)
    user_profile = UserProfile.query.filter_by(user=current_user).first()
    reminder_settings = {
        x.reminder_type: x for x in
        ReminderSettings.query.filter_by(user=current_user).all()
    }
    reminder_time = None
    for reminder in reminder_settings.values():
        if reminder is not None:
            reminder_time = reminder.reminder_time
            break
    return {
        "teams": teams,
        "user_profile": user_profile,
        "reminder_settings": reminder_settings,
        "reminder_time": reminder_time,
        "display_bots_setting":
            DisplayBotsSettings.query.filter_by(user=current_user).first()
    }
