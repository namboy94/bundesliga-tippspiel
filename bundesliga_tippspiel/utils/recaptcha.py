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

import requests
from bundesliga_tippspiel.config import recaptcha_secret_key


def verify_recaptcha(client_ip: str, recaptcha_response: str) -> bool:
    """
    Verifies a recaptcha response.
    If the recaptcha response originates from a local address,
    this method will always return True.
    :param client_ip: The IP Address of the client solving the captcha
    :param recaptcha_response: the recaptcha response to verify
    :return: True if the recaptcha response was correct, False otherwise
    """
    return client_ip in ["localhost", "127.0.0.1"] or requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": recaptcha_secret_key,
            "response": recaptcha_response,
            "remoteip": client_ip
        }
    ).json().get("success", False)
