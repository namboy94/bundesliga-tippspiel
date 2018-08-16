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

"""
This file contains environment specific configuration information
All of this information is found using environment variables
"""


smtp_address = os.environ["SMTP_ADDRESS"]
"""
The SMTP username used for sending emails
"""

smtp_server = os.environ["SMTP_SERVER"]
"""
The SMTP server used for sending emails
"""

smtp_port = int(os.environ["SMTP_PORT"])
"""
The SMTP server port used for sending emails
"""

smtp_password = os.environ["SMTP_PASSWORD"]
"""
The password of the SMTP account
"""

recaptcha_site_key = os.environ["RECAPTCHA_SITE_KEY"]
"""
The (public) recaptcha site key
"""

recaptcha_secret_key = os.environ["RECAPTCHA_SECRET_KEY"]
"""
The secret recaptcha key used to validate the recaptcha result
"""
