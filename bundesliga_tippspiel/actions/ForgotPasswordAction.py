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
from typing import Dict, Any
from flask import render_template, request
from bundesliga_tippspiel import db
from bundesliga_tippspiel.utils.email import send_email
from bundesliga_tippspiel.utils.crypto import generate_random, generate_hash
from bundesliga_tippspiel.utils.recaptcha import verify_recaptcha
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.types.exceptions import ActionException


class ForgotPasswordAction(Action):
    """
    Action class that allows a user to reset their forgotten password
    """

    def __init__(
            self,
            email: str,
            recaptcha_response: str,
            host_address: str,
            client_address: str
    ):
        """
        Initializes the ForgotPasswordAction object
        :param email: The email address of the user that forgot their password
        :param recaptcha_response: A recaptcha respnse to make sure that
                                   no bots are resetting passwords
        :param host_address: The host address of the server
        :param client_address: The client's address used
                               for verifying the recaptcha
        :raises: ActionException if any problems occur
        """
        self.email = str(email)
        self.recaptcha_response = str(recaptcha_response)
        self.host_address = str(host_address)
        self.client_address = str(client_address)

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        if len(User.query.filter_by(email=self.email).all()) < 1:
            raise ActionException(
                "Email not registered",
                "Diese Email Addresse wurde nicht registriert"
            )
        elif not verify_recaptcha(
                self.client_address, self.recaptcha_response
        ):
            raise ActionException(
                "Invalid ReCaptcha Response",
                "Bitte löse das ReCaptcha."
            )

    def _execute(self) -> Dict[str, Any]:
        """
        Executes the actual action
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        user = User.query.filter_by(email=self.email).first()  # type: User
        new_pass = generate_random(20)
        user.password_hash = generate_hash(new_pass)
        db.session.commit()

        email_message = render_template(
            "email/forgot_password_email.html",
            host=self.host_address,
            target=os.path.join(self.host_address, "login"),
            password=new_pass.decode("utf-8"),
            username=user.username
        )

        send_email(
            self.email,
            "Passwort Zurückgesetzt",
            email_message
        )

        return {}

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            data["email"],
            data["g-recaptcha-response"],
            request.host,
            request.remote_addr
        )
