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

from datetime import datetime
from flask import render_template
from typing import Dict, Any, List, Tuple
from bundesliga_tippspiel import db
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.utils.email import send_email
from bundesliga_tippspiel.models.user_generated.Bet import Bet
from bundesliga_tippspiel.models.match_data.Match import Match
from bundesliga_tippspiel.models.user_generated.EmailReminder import \
    EmailReminder


class GetDueEmailReminderAction(Action):
    """
    Action that allows getting all due reminders
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
        Confirms a previously registered user
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        pending = self.find_pending_reminders()

        for reminder, match in pending:
            email_message = render_template("email/reminder.html", match=match)
            send_email(
                reminder.user.email, "Tippspiel Erinnerung", email_message
            )
            reminder.last_match_id = match.id
            reminder.last_match = match
        db.session.commit()

        return {"sent": len(pending)}

    @staticmethod
    def find_pending_reminders() -> List[Tuple[EmailReminder, Match]]:
        """
        Finds all pending reminders and returns them including the data
        of th ematch to remind the user of.
        :return: The List of pending reminders
        """
        now = datetime.utcnow()
        reminders = EmailReminder.query.all()

        unstarted_matches = Match.query.filter_by(started=False).all()
        next_match = min(unstarted_matches, key=lambda x: x.kickoff)
        next_matchday = next_match.matchday
        unstarted_matches.filter(key=lambda x: x.matchday == next_matchday)

        pending_reminders = []

        for reminder in reminders:

            reminder_threshold = now + reminder.before_time_delta

            bets = Bet.query. \
                filter_by(user_id=reminder.user_id). \
                filter(Bet.match.has(matchday=next_matchday)) \
                .all()

            match_bet_map = {}
            for match in unstarted_matches:
                match_bet_map[match.id] = (match, None)
                for bet in bets:
                    if bet.match.id == match.id:
                        match_bet_map[match.id] = (match, bet)

            reminder_needed = []

            for match_id, (match, bet) in match_bet_map:
                if bet is None:
                    if match.kickoff_datetime < reminder_threshold:
                        reminder_needed.append(match)

            if len(reminder_needed) < 1:
                continue
            else:
                to_remind = min(reminder_needed, key=lambda x: x.kickoff)
                pending_reminders.append((reminder, to_remind))

        return pending_reminders

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls()
