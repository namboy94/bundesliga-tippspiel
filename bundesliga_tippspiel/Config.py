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
from typing import Type, List, Dict, Optional, Tuple
from jerrycan.Config import Config as BaseConfig


class Config(BaseConfig):
    """
    Configuration for the flask application
    """
    OPENLIGADB_SEASON: str
    """
    The default openligadb season to use
    """

    OPENLIGADB_LEAGUE: str
    """
    The default openligadb league to use
    """

    OPENLIGADB_EXTRA_LEAGUES: List[Tuple[str, int]]
    """
    Extra openligadb seasons and leagues
    """

    @classmethod
    def league_name(cls, league: Optional[str] = None) -> str:
        """
        Generates a name for the openligadb league
        :param league: The league string (like 'bl1')
        :return: The league name (like 'Bundesliga')
        """
        if league is None:
            league = cls.OPENLIGADB_LEAGUE
        return {
            "bl1": "Bundesliga",
            "bl2": "2. Bundesliga",
            "bl3": "3. Liga"
        }.get(league, league)

    @classmethod
    def season_string(cls, year: Optional[int] = None) -> str:
        """
        :return: The season string, e.g. 2020/21 for 2020
        """
        if year is None:
            year = int(cls.OPENLIGADB_SEASON)
        second = str(year + 1)[-2:]
        return f"{year}/{second}"

    @classmethod
    def league_string(cls, league: str, season: int) -> str:
        """
        Creates a league string, like "Bundesliga 2020/21"
        :param league: The league for which to generate the string
        :param season: The season for which to generate the string
        :return: The generated string
        """
        season_string = cls.season_string(season)
        league_name = cls.league_name(league)
        return f"{league_name} {season_string}"

    @classmethod
    def season(cls) -> int:
        """
        :return: The current season
        """
        return int(Config.OPENLIGADB_SEASON)

    @classmethod
    def all_leagues(cls) -> List[Tuple[str, int]]:
        """
        :return: A list of all leagues
        """
        leagues = [(cls.OPENLIGADB_LEAGUE, cls.season())] + \
            cls.OPENLIGADB_EXTRA_LEAGUES
        leagues.sort(key=lambda x: x[0])
        leagues.sort(key=lambda x: x[1])
        return leagues

    @classmethod
    def environment_variables(cls) -> Dict[str, List[str]]:
        """
        Specifies required and optional environment variables
        :return: The specified environment variables in two lists in
                 a dictionary, grouped by whether the variables are
                 required or optional
        """
        base = super().environment_variables()
        base["optional"] += [
            "OPENLIGADB_LEAGUE",
            "OPENLIGADB_SEASON",
            "OPENLIGADB_EXTRA_LEAGUES"
        ]
        return base

    @classmethod
    def _load_extras(cls, parent: Type[BaseConfig]):
        """
        Loads non-standard configuration variables
        :param parent: The base configuration
        :return: None
        """
        Config.OPENLIGADB_SEASON = os.environ.get("OPENLIGADB_SEASON", "2021")
        Config.OPENLIGADB_LEAGUE = os.environ.get("OPENLIGADB_LEAGUE", "bl1")
        Config.OPENLIGADB_EXTRA_LEAGUES = []
        openligdb_extras = \
            os.environ.get("OPENLIGADB_EXTRA_LEAGUES", "").strip().split(",")
        for entry in openligdb_extras:
            try:
                league, _season = entry.split(":")
                season = int(_season)
                Config.OPENLIGADB_EXTRA_LEAGUES.append((league, season))
            except ValueError:
                pass
        from bundesliga_tippspiel.template_extras import profile_extras
        parent.API_VERSION = "3"
        parent.STRINGS.update({
            "401_message": "Du bist nicht angemeldet. Bitte melde dich an.",
            "500_message": "The server encountered an internal error and "
                           "was unable to complete your request. "
                           "Either the server is overloaded or there "
                           "is an error in the application.",
            "user_does_not_exist": "Dieser Nutzer existiert nicht",
            "user_already_logged_in": "Du bist bereits angemeldet.",
            "user_already_confirmed": "Dieser Nutzer ist bereits "
                                      "bestätigt worden.",
            "user_is_not_confirmed": "Dieser Nutzer wurde "
                                     "noch nicht bestätigt",
            "invalid_password": "Das angegebene Passwort ist inkorrekt.",
            "logged_in": "Du hast dich erfolgreich angemeldet",
            "logged_out": "Erfolgreich ausgeloggt",
            "username_length": "Username zu lang: Der Username muss zwischen "
                               "{} und {} Zeichen lang sein.",
            "passwords_do_not_match": "Die angegebenen Passwörter stimmen "
                                      "nicht miteinander überein.",
            "email_already_in_use": "Die gewählte Email-Address wird bereits "
                                    "verwendet.",
            "username_already_exists": "Der ausgewählte Username existiert "
                                       "bereits.",
            "recaptcha_incorrect": "Bitte löse das ReCaptcha.",
            "registration_successful": "Siehe in deiner Email-Inbox nach, "
                                       "um die Registrierung abzuschließen.",
            "registration_email_title": "Tippspiel Registrierung",
            "confirmation_key_invalid": "Der angegebene Bestätigungsschlüssel "
                                        "ist inkorrekt.",
            "user_confirmed_successfully": "Benutzer wurde erfolgreich "
                                           "registriert. "
                                           "Du kannst dich jetzt anmelden.",
            "password_reset_email_title": "Password Zurücksetzen",
            "password_was_reset": "Passwort erfolgreich zurückgesetzt. "
                                  "Sehe in deinem Email-Postfach nach.",
            "password_changed": "Dein Passwort wurde erfolgreich geändert.",
            "user_was_deleted": "Dein Account wurde erfolgreich gelöscht",
            "telegram_chat_id_set": "Telegram Chat ID wurde erfolgreich "
                                    "gesetzt"
        })
        parent.TEMPLATE_EXTRAS.update({
            "profile": profile_extras
        })
