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
from typing import Optional
from bundesliga_tippspiel import app


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
    using_sqlite = app.testing or app.config["ENV"] == "development"
    try:
        return _type(os.environ[env_key])
    except KeyError as e:
        if default is not None:
            return default
        elif using_sqlite and env_key.startswith("DB_"):
            return None
        else:
            raise e


def load_secrets(secrets_file: str):
    """
    Loads a JSON file filled with configuration details and secrets into
    os.environ
    :param secrets_file: The file to load
    :return: None
    """
    if os.path.isfile(secrets_file):
        with open(secrets_file, "r") as f:
            secrets = json.load(f)

        for secret, value in secrets.items():
            os.environ[secret] = str(value)
