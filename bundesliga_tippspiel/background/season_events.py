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
from puffotter.flask.base import db
from bundesliga_tippspiel.db.SeasonEvent import SeasonEvent, SeasonEventType


def handle_season_events():
    """
    Handles any events that happen once every season
    :return: None
    """
    for event in load_season_events():

        if event.executed:
            continue
        elif event.event_type == SeasonEventType.PRE_SEASON_MAIL:
            event.executed = handle_preseason_reminder()
        elif event.event_type == SeasonEventType.MID_SEASON_REMINDER:
            event.executed = handle_midseason_reminder()
        elif event.event_type == SeasonEventType.POST_SEASON_WRAPUP:
            event.executed = handle_post_season_wrapup()

        db.session.commit()


def load_season_events() -> List[SeasonEvent]:
    """
    Loads all event states from the database
    :return: The event states
    """
    existing = {x.event_type: x for x in SeasonEvent.query.all()}
    for event_type in SeasonEventType:
        if event_type not in existing:
            new = SeasonEvent(event_type=event_type, executed=False)
            db.session.add(new)
            existing[event_type] = new

    db.session.commit()
    return list(existing.values())


def handle_preseason_reminder() -> bool:
    """
    Sends a reminder to existing users a week before the start of the season
    :return: Whether or not the reminder was sent
    """
    return False


def handle_midseason_reminder() -> bool:
    """
    Handles sending out midseason reminders
    :return: Whether the reminder was sent or not
    """
    return False


def handle_post_season_wrapup() -> bool:
    """
    Handles the post-season wrapup
    :return: None
    """
    return False
