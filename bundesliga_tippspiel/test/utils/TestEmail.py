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

import time
import imaplib
from bundesliga_tippspiel.utils.email import send_email
from bundesliga_tippspiel.test.TestFramework import TestFramework, \
    online_required
from bundesliga_tippspiel.config import smtp_address, smtp_password, \
    smtp_server


class TestEmail(TestFramework):
    """
    Tests email functionality
    """

    @staticmethod
    def get_inbox_count() -> int:
        """
        Checks the amount of emails in the IMAP inbox of the SMTP mail account
        :return: The amount of emails
        """
        server = imaplib.IMAP4_SSL(smtp_server.replace("smtp", "imap"), 993)
        server.login(smtp_address, smtp_password)
        return int(server.select("Inbox")[1][0])

    @online_required
    def test_emailing(self):
        """
        Tests sending an email message
        :return: None
        """
        before = self.get_inbox_count()
        send_email(smtp_address, "TEST", "<h1>Test</h1>")
        time.sleep(1)
        after = self.get_inbox_count()
        self.assertEqual(before + 1, after)
