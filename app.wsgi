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
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from bundesliga_tippspiel.utils.env import load_secrets


secrets_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "secrets.json"
)
load_secrets(secrets_file)
os.environ["PROJECT_ROOT_PATH"] = os.path.abspath(os.path.dirname(__file__))

from bundesliga_tippspiel import version, sentry_dsn
from bundesliga_tippspiel.run import app as application

sentry_sdk.init(
    sentry_dsn,
    release="bundesliga-tippspiel-" + version,
    integrations=[FlaskIntegration()]
)
