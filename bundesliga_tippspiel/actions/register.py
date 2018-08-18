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
from sqlalchemy.exc import SQLAlchemyError
from bundesliga_tippspiel.globals import db
from bundesliga_tippspiel.models.auth.User import User
from bundesliga_tippspiel.exceptions import ActionException
from bundesliga_tippspiel.utils.email import send_email
from bundesliga_tippspiel.utils.recaptcha import verify_recaptcha
from bundesliga_tippspiel.utils.db import username_exists, email_exists
from bundesliga_tippspiel.utils.crypto import generate_hash, generate_random


def register(
        username: str, email: str, password: str,
        client_address: str, recaptcha_response: str,
):
    """
    Registers a user on the website
    :param username: The user's username
    :param email: The user's email address
    :param password: The user's password
    :param client_address: The client's address
    :param recaptcha_response: The recaptcha
    :return: None
    :raises: ActionException if any problems occur
    """

    # Data Validation
    if len(username) > 12:
        raise ActionException("Username too long")
    elif len(username) < 1:
        raise ActionException("Username too short")
    elif username_exists(username):
        raise ActionException("Username already exists")
    elif email_exists(email):
        raise ActionException("Email already exists")
    elif not verify_recaptcha(client_address, recaptcha_response):
        raise ActionException("Invalid ReCaptcha Response")

    confirmation_key = generate_random(32)
    confirmation_hash = generate_hash(confirmation_key)
    hashed = generate_hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=hashed,
        confirmation_hash=confirmation_hash
    )

    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError:
        raise ActionException("Unknown SQL Error")

    email_message = str(render_template("registration_email.html"))
    send_email(client_address, "Tippspiel Registrierung", email_message)
