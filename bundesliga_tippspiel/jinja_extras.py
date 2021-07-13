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

from typing import Dict, Any
from bundesliga_tippspiel.utils.matchday import get_matchday_info, \
    get_selected_league


def jinja_extras() -> Dict[str, Any]:
    """
    Makes sure that jinja has access to these variables
    :return: The variables to forward to jinja
    """
    return {
        "get_pill_class": get_pill_class,
        "get_matchday_total_pill_class": get_matchday_total_pill_class,
        "get_matchday_info": get_matchday_info,
        "get_selected_league": get_selected_league
    }


def get_pill_class(points: int) -> str:
    """
    Calculates the appropriate pill badge for an amount of points
    :param points: The points for which to get the pill class
    :return: The appropriate pill badge class
    """
    if points == 0:
        return "danger"
    elif points <= 3:
        return "warning"
    elif points <= 7:
        return "light"
    elif points <= 10:
        return "info"
    elif points <= 12:
        return "primary"
    elif points > 12:
        return "success"
    else:
        return "secondary"


def get_matchday_total_pill_class(points: int) -> str:
    """
    Calculates the appropriate pill badge for an amount of points on a matchday
    :param points: The points for which to get the pill class
    :return: The appropriate pill badge class
    """
    if points == 0:
        return "danger"
    elif points <= 20:
        return "warning"
    elif points <= 40:
        return "light"
    elif points <= 60:
        return "info"
    elif points <= 80:
        return "primary"
    elif points > 100:
        return "success"
    else:
        return "secondary"
