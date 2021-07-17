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

from typing import List
from flask import render_template
from bs4 import BeautifulSoup
from smtplib import SMTPAuthenticationError
from datetime import datetime, timedelta
from puffotter.smtp import send_email
from jerrycan.base import db, app
from jerrycan.db.User import User
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.db.SeasonEvent import SeasonEvent, SeasonEventType
from bundesliga_tippspiel.db.match_data.Match import Match


def handle_season_events():
    """
    Handles any events that happen once every season
    :return: None
    """
    for event in load_season_events():

        try:
            if event.executed:
                continue
            elif event.event_type == SeasonEventType.PRE_SEASON_MAIL:
                event.executed = handle_preseason_reminder()
            elif event.event_type == SeasonEventType.MID_SEASON_REMINDER:
                event.executed = handle_midseason_reminder()
            elif event.event_type == SeasonEventType.POST_SEASON_WRAPUP:
                event.executed = handle_postseason_wrapup()
            else:  # pragma: no cover
                pass

            db.session.commit()
        except SMTPAuthenticationError:
            app.logger.error("Failed to send email (Authentication failed)")


def load_season_events() -> List[SeasonEvent]:
    """
    Loads all event states from the database
    :return: The event states
    """
    existing = {
        x.event_type: x
        for x in SeasonEvent.query.filter_by(
            season=Config.season(),
            league=Config.OPENLIGADB_LEAGUE
        ).all()
    }
    for event_type in SeasonEventType:
        if event_type not in existing:
            new = SeasonEvent(
                event_type=event_type,
                executed=False,
                season=Config.season(),
                league=Config.OPENLIGADB_LEAGUE
            )
            db.session.add(new)
            existing[event_type] = new

    db.session.commit()
    return list(existing.values())


def handle_preseason_reminder() -> bool:
    """
    Sends a reminder to existing users a week before the start of the season
    :return: Whether or not the reminder was sent
    """
    return __handle_reminder(
        1,
        timedelta(days=7),
        "email/preseason.html",
        True
    )


def handle_midseason_reminder() -> bool:
    """
    Handles sending out midseason reminders
    :return: Whether the reminder was sent or not
    """
    return __handle_reminder(
        18,
        timedelta(days=7),
        "email/midseason.html",
        True
    )


def handle_postseason_wrapup() -> bool:
    """
    Handles the post-season wrapup
    :return: None
    """
    return __handle_reminder(
        34,
        timedelta(days=1),
        "email/postseason.html",
        False
    )


def __handle_reminder(
        matchday: int,
        delta: timedelta,
        message_file: str,
        before: bool
) -> bool:
    """
    Handles sending out a reminder after/before a specified time
    :param matchday: The matchday that acts as an anchor
    :param delta: The time delta relative to the matchday
    :param message_file: The HTML template containing the message
    :param before: Whether or not the email should be sent before the event
    :return: True if the message was sent, False if it was not yet due
    """
    kickoff_times = [
        x.kickoff_datetime
        for x in Match.query.filter_by(
            matchday=matchday,
            season=Config.season(),
            league=Config.OPENLIGADB_LEAGUE
        ).all()
    ]

    if len(kickoff_times) == 0:
        return False
    elif before:
        kickoff = min(kickoff_times)
    else:
        kickoff = max(kickoff_times)

    now = datetime.utcnow()

    if before and kickoff - delta > now:
        return False
    elif not before and kickoff + delta > now:
        return False
    else:
        for user in User.query.filter_by(confirmed=True).all():

            message = render_template(
                message_file,
                user=user
            )

            send_email(
                user.email,
                f"Fußball Tippspiel Saison {Config.season_string()}",
                message,
                Config.SMTP_HOST,
                Config.SMTP_ADDRESS,
                Config.SMTP_PASSWORD,
                Config.SMTP_PORT
            )

            telegram = user.telegram_chat_id
            if telegram is not None:
                message = BeautifulSoup(message, "html.parser").text
                message = "\n".join([x.strip() for x in message.split("\n")])
                telegram.send_message(message)
        return True
