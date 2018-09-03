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

from enum import Enum


class AlertSeverity(Enum):
    """
    Enumeration that defines the various levels of severity an alert can have
    """

    SUCCESS = "success"
    """
    Translates to a green alert
    """

    INFO = "info"
    """
    Translates to a blue alert
    """

    WARNING = "warning"
    """
    Translates to a yellow alert
    """

    DANGER = "danger"
    """
    Translates to a red alert
    """
