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


class ActionException(Exception):
    """
    An exception that gets raised whenever an action method fails for whatever
    reason. The reason should be provided as a parameter
    """

    def __init__(self, reason: str):
        """
        Initializes the Exception while adding the 'reason' variable
        :param reason: The reason for the exception
        """
        super().__init__(reason)
        self.reason = reason
