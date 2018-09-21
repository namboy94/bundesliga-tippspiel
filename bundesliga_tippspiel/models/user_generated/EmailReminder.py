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

from flask import render_template
from typing import Dict, Any, List
from datetime import timedelta, datetime
from bundesliga_tippspiel import app, db
from bundesliga_tippspiel.models.user_generated.Bet import Bet
from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.models.ModelMixin import ModelMixin
from bundesliga_tippspiel.utils.email import send_email


class EmailReminder(ModelMixin, db.Model):
    """
    Model that describes the 'email_reminders' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "email_reminders"
    """
    The name of the table
    """

    user_id = db.Column(
        db.Integer, db.ForeignKey(
            "users.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )
    """
    The ID of the user associated with this email reminder
    """

    user = db.relationship(
        "User",
        backref=db.backref("email_reminders", lazy=True, cascade="all,delete")
    )
    """
    The user associated with this email reminder
    """

    reminder_time = db.Column(db.Integer, nullable=False)
    """
    The time before the next unbet match when the reminder email
    will be sent.
    Unit: seconds
    """

    last_reminder = db.Column(db.String(19), nullable=False,
                              default="1970-01-01:01-01-01")
    """
    The time when the last reminder was sent. Format in the form
    %Y-%m-%d:%H-%M-%S
    """

    @property
    def reminder_time_delta(self) -> timedelta:
        """
        :return: The 'reminder_time' parameter as a datetime timedelta
        """
        return timedelta(seconds=self.reminder_time)

    @property
    def last_reminder_datetime(self) -> datetime:
        """
        :return: The 'last_reminder' parameter as a datetime object
        """
        return datetime.strptime(self.last_reminder, "%Y-%m-%d:%H-%M-%S")

    def __json__(self, include_children: bool = False) -> Dict[str, Any]:
        """
        Generates a dictionary containing the information of this model
        :param include_children: Specifies if children data models will be
                                 included or if they're limited to IDs
        :return: A dictionary representing the model's values
        """
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "reminder_time": self.reminder_time,
            "last_reminder": self.last_reminder
        }
        if include_children:
            data["user"] = self.user.__json__(True)
        return data

    def get_due_matches(self) -> List[Match]:
        """
        Checks if the reminder is due and returns a list of matches that the
        user still needs to bet on.
        :return: The matches for which the reminder is due
        """
        app.logger.info("Checking for due reminders for user {}."
                        .format(self.user.username))

        now = datetime.utcnow()
        start = max(now, self.last_reminder_datetime)
        start_str = start.strftime("%Y-%m-%d:%H-%M-%S")
        then = now + self.reminder_time_delta
        then_str = then.strftime("%Y-%m-%d:%H-%M-%S")

        due_matches = Match.query\
            .filter(start_str < Match.kickoff)\
            .filter(Match.kickoff < then_str)\
            .all()

        user_bets = Bet.query.filter_by(user_id=self.user_id).all()
        betted_matches = list(map(lambda x: x.match_id, user_bets))

        to_remind = list(filter(
            lambda x: x.id not in betted_matches,
            due_matches
        ))

        app.logger.debug("Matches to remind: {}.".format(to_remind))

        return to_remind

    def send_reminder(self):
        """
        Sends a reminder email if it's due
        :return: None
        """
        due = self.get_due_matches()
        if len(due) < 1:
            app.logger.info("No due reminders found")
            return
        else:
            app.logger.info("Sending reminder to {}.".format(self.user.email))
            message = render_template(
                "email/reminder.html",
                user=self.user,
                matches=due,
                hours=int(self.reminder_time / 3600)
            )
            send_email(self.user.email, "Tippspiel Erinnerung", message)
            last_match = max(due, key=lambda x: x.kickoff)
            self.last_reminder = last_match.kickoff
            db.session.commit()

    def set_reminder_time(self, reminder_time: int):
        """
        Sets the reminder time and resets the time stored as the last reminder
        :param reminder_time: the new reminder time
        :return: None
        """
        self.reminder_time = reminder_time
        self.last_reminder = "1970-01-01:01-01-01"
        db.session.commit()
