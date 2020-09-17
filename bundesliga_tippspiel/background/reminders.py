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

from puffotter.flask.base import app, db
from puffotter.flask.db.User import User
from bundesliga_tippspiel.db.user_generated.EmailReminder import EmailReminder


def send_due_reminders():
    """
    Sends all email reminders that are due
    :return: None
    """
    app.logger.info("Checking for new email reminders")
    reminders = EmailReminder.query.all()
    reminder_users = [reminder.user_id for reminder in reminders]
    for user in User.query.all():
        if user.id not in reminder_users and user.confirmed:
            reminder = EmailReminder(user=user, reminder_time=86400)
            db.session.add(reminder)
            reminders.append(reminder)
    db.session.commit()

    for reminder in EmailReminder.query.all():
        reminder.send_reminder()
