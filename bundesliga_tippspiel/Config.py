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
from typing import Type, List, Dict, Optional
from puffotter.flask.Config import Config as BaseConfig


class Config(BaseConfig):
    """
    Configuration for the flask application
    """
    OPENLIGADB_SEASON: str
    """
    The openligadb season to use
    """

    OPENLIGADB_LEAGUE: str
    """
    The openligadb league to use
    """

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
    def season(cls) -> int:
        """
        :return: The current season
        """
        return int(Config.OPENLIGADB_SEASON)

    @classmethod
    def environment_variables(cls) -> Dict[str, List[str]]:
        """
        Specifies required and optional environment variables
        :return: The specified environment variables in two lists in
                 a dictionary, grouped by whether the variables are
                 required or optional
        """
        base = super().environment_variables()
        base["required"] += [
            "OPENLIGADB_SEASON"
        ]
        base["optional"] += [
            "OPENLIGADB_LEAGUE"
        ]
        return base

    @classmethod
    def _load_extras(cls, parent: Type[BaseConfig]):
        """
        Loads non-standard configuration variables
        :param parent: The base configuration
        :return: None
        """
        Config.OPENLIGADB_SEASON = os.environ.get("OPENLIGADB_SEASON", "2019")
        print(Config.OPENLIGADB_SEASON)
        Config.OPENLIGADB_LEAGUE = os.environ.get("OPENLIGADB_LEAGUE", "bl1")
        from bundesliga_tippspiel.template_extras import profile_extras
        parent.API_VERSION = "2"
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
