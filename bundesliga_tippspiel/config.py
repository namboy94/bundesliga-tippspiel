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
from bundesliga_tippspiel.globals import app

"""
This file contains environment specific configuration information
All of this information is found using environment variables
"""


def resolve_env_variable(
        env_key: str, _type: type = str, default: object = None
) -> Optional[object]:
    """
    Resolves an environment key.
    A non-existant environment key will lead to a KeyError unless the app
    is in testing mode, in which case database-related variables won't
    cause a KeyError.
    KeyErrors can also be provided using the 'default' argument
    :param env_key: The environment key to resolve
    :param _type: The type of the environment variable
    :param default: An optional default value
    :return: The resolved environment variable.
             None if the app is in testing mode and the variable is db-related
    """
    try:
        return type(os.environ[env_key])
    except KeyError as e:
        if default is not None:
            return default
        elif app.config["TESTING"] and env_key.startswith("DB_"):
            return None
        else:
            raise e


smtp_address = resolve_env_variable(
    "SMTP_ADDRESS", default="noreply@hk-tippspiel.com"
)
"""
The SMTP username used for sending emails
"""

smtp_server = resolve_env_variable("SMTP_SERVER", default="smtp.strato.de")
"""
The SMTP server used for sending emails
"""

smtp_port = resolve_env_variable("SMTP_PORT", int, default=465)
"""
The SMTP server port used for sending emails
"""

smtp_password = resolve_env_variable("SMTP_PASSWORD")
"""
The password of the SMTP account
"""

recaptcha_site_key = resolve_env_variable(
    "RECAPTCHA_SITE_KEY", default="6Le5xGkUAAAAABOfWC_-qAxU0vVCnHGHQPdpVv-_"
)
"""
The (public) recaptcha site key
"""

recaptcha_secret_key = resolve_env_variable("RECAPTCHA_SECRET_KEY")
"""
The secret recaptcha key used to validate the recaptcha result
"""

db_user = resolve_env_variable("DB_USER")
"""
The database user
"""

db_name = resolve_env_variable("DB_NAME")
"""
The database name
"""

db_key = resolve_env_variable("DB_KEY")
"""
The database key
"""
