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

import os
from typing import Optional
from flask import render_template, request
from sqlalchemy.exc import SQLAlchemyError
from bundesliga_tippspiel.globals import db
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.exceptions import ActionException
from bundesliga_tippspiel.utils.email import send_email
from bundesliga_tippspiel.utils.recaptcha import verify_recaptcha
from bundesliga_tippspiel.utils.db import username_exists, email_exists
from bundesliga_tippspiel.utils.crypto import generate_hash, generate_random
from bundesliga_tippspiel.actions.Action import Action


class RegisterAction(Action):
    """
    Action that allows the registration of new users
    """

    def __init__(
            self, username: str, email: str, password: str,
            client_address: str, host_address: str,
            recaptcha_response: str,
            password_repeat: Optional[str] = None
    ):
        """
        Initializes the RegisterAction object
        :param username: The user's username
        :param email: The user's email address
        :param password: The user's password
        :param client_address: The client's address
        :param host_address: The host's address
        :param recaptcha_response: The recaptcha response
        :param password_repeat: If provided, makes sure that passwords match.
        :return: None
        :raises: ActionException if any problems occur
        """
        self.username = username
        self.email = email
        self.password = password
        self.client_address = client_address
        self.host_address = host_address
        self.recaptcha_response = recaptcha_response
        self.password_repeat = password_repeat

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """

        if len(self.username) > 12:
            raise ActionException(
                "Username too long",
                "Username zu lang: Der Username muss zwischen "
                "1 und 12 Zeichen lang sein."
            )

        elif len(self.username) < 1:
            raise ActionException(
                "Username too short",
                "Username zu kurz: Der Username muss zwischen "
                "1 und 12 Zeichen lang sein."
            )

        elif self.password_repeat is not None \
                and self.password_repeat != self.password:
            raise ActionException(
                "Password Mismatch",
                "Die angegebenen Passwörter stimmen nicht miteinander überein."
            )

        elif username_exists(self.username):
            raise ActionException(
                "Username already exists",
                "Der ausgewählte Username existiert bereits."
            )

        elif email_exists(self.email):
            raise ActionException(
                "Email already exists",
                "Die gewählte Email-Address wird bereits verwendet."
            )

        elif not verify_recaptcha(
                self.client_address, self.recaptcha_response
        ):
            raise ActionException(
                "Invalid ReCaptcha Response",
                "Bitte löse das ReCaptcha."
            )

    def _execute(self):
        """
        Registers a data
        :return: None
        :raises ActionException: if anything went wrong
        """
        confirmation_key = generate_random(32)
        confirmation_hash = generate_hash(confirmation_key)
        hashed = generate_hash(self.password)

        user = User(
            username=self.username,
            email=self.email,
            password_hash=hashed,
            confirmation_hash=confirmation_hash
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:  # pragma: no cover
            raise ActionException("Unknown SQL Error",
                                  "Ein unbekannter Fehler ist aufgetreten")

        confirm_url = os.path.join(self.host_address, "confirm")
        confirm_url += "?username={}&confirmation_key={}".format(
            self.username, confirmation_key.decode("utf-8")
        )

        email_message = render_template(
            "registration_email.html",
            username=self.username,
            confirm_url=confirm_url
        )
        send_email(
            self.email,
            "Tippspiel Registrierung",
            email_message
        )

    @classmethod
    def from_site_request(cls) -> Action:
        """
        Generates a RegisterAction object from a site request
        :return: The generated RegisterAction object
        """
        return cls(
            request.form["username"],
            request.form["email"],
            request.form["password"],
            request.remote_addr,
            request.host,
            request.form["g-recaptcha-response"],
            password_repeat=request.form["password-repeat"]
        )