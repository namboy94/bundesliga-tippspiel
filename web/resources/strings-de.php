<?php
/*  Copyright Hermann Krumrey <hermann@krumreyh.com> 2017

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
*/

function get_german_dictionary() {

	return array(

		'@$ADMIN_CONTACT_TITLE' => 'Administrator',
		'@$SOURCE_CODE_TITLE' => "Quellcode",
        '@$WEBSITE_NAME' => "Bundesliga Tippspiel",
		'@$HOME_TITLE' => "Bundesliga Tippspiel - HOME",
		'@$ABOUT_TITLE' => "Bundesliga Tippspiel - IMPRESSUM",
		'@$CONTACT_TITLE' => "Bundesliga Tippspiel - KONTAKT",
        '@$SIGNUP_TITLE' => "Bundesliga Tippspiel - Login",
		'@$NAVBAR_TITLE' => "Bundesliga Tippspiel",
		'@$HOME_NAV' => "Home",
		'@$ABOUT_NAV' => "Impressum",
		'@$CONTACT_NAV' => "Kontakt",
        '@$SIGNUP_NAV' => "Login",
		'@$THEMES_NAV' => "Themen",
		'@$GERMAN_LANG' => "Deutsch",
		'@$ENGLISH_LANG' => "Englisch",
		'@$DEFAULT_THEME' => "Standard",
		'@$TERMINAL_THEME' => "Terminal",
		'@$GITLAB_NAME' => "Gitlab",
		'@$ABOUT_TEXT' => file_get_contents("resources/impressum.de", true),
        '@$SIGNUP_HEADER' => "Registrieren",
        '@$LOGIN_HEADER' => "Anmelden",
        '@$EMAIL_TITLE' => "Email Addresse",
        '@$USERNAME_TITLE' => "Benutzername",
        '@$PASSWORD_TITLE' => "Passwort",
        '@$SUBMIT_TITLE' => "Bestätigen",
        '@$PASSWORD_REPEAT' => "Passwort (Nochmals)",
        '@$EMAIL_CONFIRMATION' => "Vielen Dank für ihre Registrierung für das Bundesliga Tippspiel!\n\n" .
                                  "Um ihre Registrierung zu vervollständigen, clicken Sie den nachfolgenden Link:\n\n",
        '@$CONFIRMATION_NAME' => "Bestätigung",
        '@$PASSWORD_MISMATCH_TITLE' => "Passwörter stimmen nicht überein",
        '@$PASSWORD_MISMATCH_BODY' => "Bitte geb das Passwort noch einmal ein",
        '@$NO_EMAIL_TITLE' => "Keine Email Adresse",
        '@$NO_EMAIL_BODY' => "Bitte geb eine Email Adresse an",
        '@$NO_USERNAME_TITLE' => "Kein Nutzername angegeben",
        '@$NO_USERNAME_BODY' => "Bitte gebe einen Nutzernamen an",
        '@$NO_PASSWORD_TITLE' => "Kein Passwort eingegeben",
        '@$NO_PASSWORD_BODY' => "Bitte geb ein Passwort an",
        '@$USERNAME_EXISTS_TITLE' => "Nutzername existiert bereits",
        '@$USERNAME_EXISTST_BODY' => "Bitte wahle einen anderen Nutzernamen",
        '@$EMAIL_USED_TITLE' => "Email Adresse bereits verwendet",
        '@$EMAIL_USED_BODY' => "Bitte benutze eine andere Email Adresse",
        '@$PASSWORD_TOO_SHORT_TITLE' => 'Passwort zu kurz',
        '@$PASSWORD_TOO_SHORT_BODY' => "Bitte geb ein Passwort mit mindestens 8 Zeichen an",
        '@$INVALID_CREDENTIALS_TITLE' => 'Login Fehlgeschlagen',
        '@$INVALID_CREDENTIALS_BODY' => "Bitte überprüfe deine Login Daten",
        '@$REGISTRATION_INITIALIZED_TITLE' => "Registrierung abgeschlossen",
        '@$REGISTRATION_INITIALIZED_BODY' => "Schau in deinem Email Postfach nach der Bestätigungsemail",
        '@$ALREADY_CONFIRMED_TITLE' => 'Registrierung bereits abgeschlossen',
        '@$ALREADY_CONFIRMED_BODY' => 'Du kannst dich mit deiner Email Adresse und deinem Passwort anmelden',
        '@$CONFIRMATION_NOT_MATCHING_TITLE' => 'Bestätigung Ungültig',
        '@$CONFIRMATION_NOT_MATCHING_BODY' => 'Stelle sicher dass der richtige Link geclickt wurde',
        '@$NOT_EXISTING_USER_TITLE' => 'Dieser Nutzername existiert nicht',
        '@$NOT_EXISTING_USER_BODY' => 'Stelle sicher dass der richtige Link geclickt wurde',
        '@$REGISTRATION_SUCCESS_TITLE' => "Account bestätigt",
        '@$REGISTRATION_SUCCESS_BODY' => "Du kannst dich jetzt anmelden"

	);

}

?>