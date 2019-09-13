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
import pkg_resources
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

app = Flask(__name__)
"""
The Flask App
"""

db = SQLAlchemy()
"""
The SQLAlchemy database connection
"""

login_manager = LoginManager(app)
"""
The Flask-Login Login Manager
"""

version = pkg_resources.get_distribution("bundesliga-tippspiel").version
"""
The current version of the application
"""

# Config
app.config["TRAP_HTTP_EXCEPTIONS"] = True
login_manager.session_protection = "strong"

sentry_sdk.init(
    "https://e91e468e84424758bd74e6908af2c565@sentry.namibsun.net/6",
    release="bundesliga-tippspiel-" + version,
    integrations=[FlaskIntegration()]
)


if "FLASK_TESTING" in os.environ:  # pragma: no cover
    app.testing = os.environ["FLASK_TESTING"] == "1"
