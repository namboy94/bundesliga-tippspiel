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

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bundesliga_tippspiel.config import smtp_address, smtp_password, \
    smtp_port, smtp_server


def send_email(address: str, title: str, message: str):
    """
    Sends an HTML email message
    :param address: The address to send to
    :param title: The email's title
    :param message: The message to send
    :return: None
    """
    connection = smtplib.SMTP(smtp_server, smtp_port)
    connection.ehlo()
    connection.starttls()
    connection.ehlo()
    connection.login(smtp_address, smtp_password)

    msg = MIMEMultipart("alternative")
    msg["subject"] = title
    msg["From"] = smtp_address
    msg["To"] = address
    msg.attach(MIMEText(message, "html"))

    connection.sendmail(smtp_address, address, msg.as_string())
