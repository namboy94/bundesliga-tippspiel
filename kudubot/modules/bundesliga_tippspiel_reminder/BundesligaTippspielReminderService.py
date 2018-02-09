"""
Copyright 2017-2018 Hermann Krumrey

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
"""

import re
import time
from kudubot.entities.Message import Message
from kudubot.services.BaseService import BaseService
from bundesliga_tippspiel_reminder.database import \
    initialize_database, verify, get_subscriptions, get_next_match, \
    notification_required, acknowledge


class BundesligaTippspielReminderService(BaseService):
    """
    Kudubot Service that handles reminders for hk-tippspiel.com

    How it works:

    On the website/app, the user may request to receive reminders on their
    messaging apps like Whatsapp or Telegram. To do so, they must send a
    generated key to the bot using a message like:

    /register [KEY]

    Once successfully registered, the settings (hours before match etc)
    can be adjusted using the Web UI.
    """

    def init(self):
        """
        Initializes the database and background loop
        :return: None
        """
        self.initialize_database_table(initializer=initialize_database)
        self.start_daemon_thread(target=self.background_loop)

    @staticmethod
    def define_identifier() -> str:
        """
        Defines the identifier for this service
        :return: the service's identifier
        """
        return "bundesliga-tippspiel-reminder"

    def is_applicable_to(self, message: Message) -> bool:
        """
        Only checks for applicable messages that include an authentication key
        :param message: the message to check
        :return: True if the message is syntactically correct, False otherwise
        """
        return bool(re.search(r"^/register [0-9]+:", message.message_body))

    def handle_message(self, message: Message):
        """
        Handles the register message
        :param message: the message to handle
        :return: None
        """
        key = message.message_body.split(" ")[1].strip()

        if verify(self.connection.db, key, message.sender):
            self.reply(
                "Registration Successful",
                "Successfully registered for bundesliga-tippspiel reminders",
                message
            )

        else:
            self.reply(
                "Registration Failed",
                "The registration for bundesliga-tippspiel reminders failed.\n"
                "Please make sure that the provided key is correct",
                message
            )

    def background_loop(self):
        """
        Runs in the background and checks the subscriptions for messages that
        need to be sent
        :return: None
        """

        db = self.connection.get_database_connection_copy()
        while True:

            subscriptions = get_subscriptions(db)
            print(subscriptions)

            for user_id in subscriptions:

                subscription = subscriptions[user_id]
                username = subscription["username"]
                contact = subscription["contact"]
                warning_time = subscription["warning_time"]

                next_match = get_next_match(user_id)

                notification_message = "Reminder: " + username
                notification_message += ", you still need to bet on the " \
                                        "next match!\n Go to " \
                                        "https://hk-tippspiel.com/bets.php " \
                                        "to place your bets."

                if notification_required(
                        db, user_id, next_match, warning_time
                ):
                    self.connection.send_message(Message(
                        "Bundesliga-Tippspiel",
                        notification_message,
                        contact,
                        self.connection.user_contact
                    ))

                    acknowledge(db, user_id, next_match["id"])

                self.connection.send_message(Message("Hi", "Hello", contact, self.connection.user_contact))

            time.sleep(60)
