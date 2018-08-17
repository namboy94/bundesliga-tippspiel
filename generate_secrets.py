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
import json


def generate_secrets():
    """
    Generates a secrets.json file out of environment variables
    :return: None
    """
    environment = os.environ["TIPPSPIEL_ENV"]
    secrets = {}

    db_prefix = "DEVEL_" if environment == "develop" else "PROD_"

    for key in [
        "DB_KEY",
        "DB_NAME",
        "DB_USER",
        "SMTP_SERVER",
        "SMTP_ADDRESS",
        "SMTP_PORT",
        "SMTP_PASSWORD",
        "RECAPTCHA_SECRET_KEY",
        "RECAPTCHA_SITE_KEY"
    ]:
        if key.startswith("DB_"):
            secrets[key] = os.environ[db_prefix + key]
        else:
            secrets[key] = os.environ[key]

    with open("secrets.json", "w") as f:
        f.write(json.dumps(secrets))


if __name__ == "__main__":
    generate_secrets()
