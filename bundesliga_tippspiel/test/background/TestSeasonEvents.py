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

from datetime import datetime, timedelta
from unittest.mock import patch
from jerrycan.base import db
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.TestFramework import _TestFramework
from bundesliga_tippspiel.db.SeasonEvent import SeasonEvent, SeasonEventType
from bundesliga_tippspiel.background.season_events import load_season_events, \
    handle_season_events, handle_midseason_reminder, \
    handle_postseason_wrapup, handle_preseason_reminder


class TestSeasonEvents(_TestFramework):
    """
    Class that tests the sending of due email reminders
    """

    def setUp(self):
        """
        Sets up a user for testing
        :return: None
        """
        super().setUp()
        self.user = self.generate_sample_user(True)[0]
        _, _, _, self.match, _ = self.generate_sample_match_data()

    def test_initializing(self):
        """
        Tests initializing the season-wide database entries
        :return: None
        """
        total = len([x for x in SeasonEventType])
        self.assertEqual(len(SeasonEvent.query.all()), 0)
        load_season_events()
        self.assertEqual(len(SeasonEvent.query.all()), total)
        load_season_events()
        self.assertEqual(len(SeasonEvent.query.all()), total)

    def test_executing(self):
        """
        Tests if the events are executed correctly, and only once.
        :return: None
        """
        base = "bundesliga_tippspiel.background.season_events."
        mocked = [
            base + "handle_preseason_reminder",
            base + "handle_midseason_reminder",
            base + "handle_postseason_wrapup"
        ]

        before = load_season_events()
        for event in before:
            self.assertFalse(event.executed)

        with patch(mocked[0], lambda: True):
            with patch(mocked[1], lambda: True):
                with patch(mocked[2], lambda: True):
                    handle_season_events()

        after = load_season_events()
        for event in after:
            self.assertTrue(event.executed)

        with patch(mocked[0], lambda: self.fail()):
            with patch(mocked[1], lambda: self.fail()):
                with patch(mocked[2], lambda: self.fail()):
                    handle_season_events()

    def test_preseason_reminder(self):
        """
        Tests sending the preseason reminder if it's due
        :return: None
        """
        base = "bundesliga_tippspiel.background.season_events."
        email = base + "send_email"
        load_season_events()
        now = datetime.utcnow()

        self.match.matchday = 1
        db.session.commit()

        with patch(email) as email_mock:
            self.assertEqual(email_mock.call_count, 0)

            self.match.kickoff_datetime = now + timedelta(weeks=2)
            db.session.commit()
            self.assertFalse(handle_preseason_reminder())
            self.assertEqual(email_mock.call_count, 0)

            self.match.kickoff_datetime = now + timedelta(days=5)
            db.session.commit()
            self.assertTrue(handle_preseason_reminder())
            self.assertEqual(email_mock.call_count, 1)

    def test_midseason_reminder(self):
        """
        Tests sending the midseason reminder
        :return: None
        """
        base = "bundesliga_tippspiel.background.season_events."
        email = base + "send_email"
        load_season_events()
        now = datetime.utcnow()

        self.match.matchday = 18
        db.session.commit()

        with patch(email) as email_mock:
            self.assertEqual(email_mock.call_count, 0)

            self.match.kickoff_datetime = now + timedelta(weeks=2)
            db.session.commit()
            self.assertFalse(handle_midseason_reminder())
            self.assertEqual(email_mock.call_count, 0)

            self.match.kickoff_datetime = now + timedelta(days=5)
            db.session.commit()
            self.assertTrue(handle_midseason_reminder())
            self.assertEqual(email_mock.call_count, 1)

    def test_postseason_wrapup(self):
        """
        Tests doing the postseason wrapup
        :return: None
        """
        base = "bundesliga_tippspiel.background.season_events."
        email = base + "send_email"
        load_season_events()
        now = datetime.utcnow()

        self.match.matchday = 34
        db.session.commit()

        with patch(email) as email_mock:
            self.assertEqual(email_mock.call_count, 0)

            self.match.kickoff_datetime = now
            db.session.commit()
            self.assertFalse(handle_postseason_wrapup())
            self.assertEqual(email_mock.call_count, 0)

            self.match.kickoff_datetime = now - timedelta(days=1, seconds=1)
            db.session.commit()
            self.assertTrue(handle_postseason_wrapup())
            self.assertEqual(email_mock.call_count, 1)
