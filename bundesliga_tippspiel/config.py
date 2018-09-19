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
from bundesliga_tippspiel.utils.env import resolve_env_variable

"""
This file contains environment specific configuration information
All of this information is found using environment variables
"""


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

smtp_port = resolve_env_variable("SMTP_PORT", int, default=587)
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

openligadb_season = resolve_env_variable("OPENLIGADB_SEASON", default="2018")
"""
The openligadb.de season to populate the data with
"""

openligadb_league = resolve_env_variable("OPENLIGADB_LEAGUE", default="bl1")
"""
The openligadb.de league to populate the data with
"""

last_match_data_update = 0
"""
Keeps track of when the match data was updated last
"""

last_reminder_sending = 0
"""
Keeps track of when reminders were last sent out
"""

logging_path = os.path.join(
    str(resolve_env_variable("PROJECT_ROOT_PATH", default="/tmp")),
    "tippspiel.log"
)
