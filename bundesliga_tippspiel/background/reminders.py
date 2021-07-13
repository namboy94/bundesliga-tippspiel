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

from jerrycan.base import app, db
from jerrycan.db.User import User
from bundesliga_tippspiel.enums import ReminderType
from bundesliga_tippspiel.db.settings.ReminderSettings import ReminderSettings


def send_due_reminders():
    """
    Sends all email reminders that are due
    :return: None
    """
    app.logger.info("Checking for new email reminders")
    reminders = ReminderSettings.query.join(ReminderSettings.user).all()

    all_users = User.query.filter_by(confirmed=True).all()
    for reminder_type in ReminderType:
        reminder_users = [
            reminder.user_id
            for reminder in reminders
            if reminder.reminder_type == reminder_type
        ]

        for user in all_users:
            if user.id not in reminder_users and user.confirmed:
                reminder = ReminderSettings(
                    user=user, reminder_type=reminder_type
                )
                db.session.add(reminder)
                reminders.append(reminder)
    db.session.commit()

    for reminder in reminders:
        reminder.send_reminder()
