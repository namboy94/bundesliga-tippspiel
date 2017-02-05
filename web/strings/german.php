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

/**
 * Generates a german dictionary
 * @return array: the german dictionary
 */
function get_german() {
    return array(

        # HEADER TITLES
        'HOME_TITLE' => 'Bundesliga Tippspiel - Home',
        'CONTACT_TITLE' => 'Bundesliga Tippspiel - Kontakt',
        'ABOUT_TITLE' => 'Bundesliga Tippspiel - Impressum',
        'SIGNUP_TITLE' => 'Bundesliga Tippspiel - Anmelden und Registrieren',
        'BETS_TITLE' => 'Bundesliga Tippspiel - Wetten',
        'LEADERBOARD_TITLE' => 'Bundesliga Tippspiel - Rangliste',
        'PROFILE_TITLE' => 'Bundesliga Tippspiel - Profil',

        # NAVBAR TITLES
        'WEBSITE_NAME' => 'Bundesliga Tippspiel',
        'HOME_NAV_TITLE' => 'Home',
        'LOGIN_NAV_TITLE' => 'Anmelden',
        'LOGOUT_NAV_TITLE' => 'Abmelden',
        'BETS_NAV_TITLE' => 'Wetten',
        'LEADERBOARD_NAV_TITLE' => 'Rangliste',
        'PROFILE_NAV_TITLE' => 'Profil',
        'THEMES_NAV_TITLE' => 'Themen',
        'THEME_DEFAULT_NAV_TITLE' => 'Standard',
        'THEME_TERMINAL_NAV_TITLE' => 'Konsole',
        'LANGUAGES_NAV_TITLE' => 'Sprachen',
        'LANGUAGE_GERMAN_NAV_TITLE' => 'Deutsch',
        'LANGUAGE_ENGLISH_NAV_TITLE' => 'Englisch',
        'FOOTER_IMPRESSUM_TITLE' => 'Impressum',
        'FOOTER_COPYRIGHT_TEXT' => '© Hermann Krumrey 2017',
        'FOOTER_VERSION_TEXT' => file_get_contents(dirname(__FILE__) . '/../resources/version'),

        # index.php
        'HOME_JUMBO' => 'Bundesliga Tippspiel',
        'OR_SIGN_UP_TEXT' => 'Oder registriere dich <a href="signup.php">hier</a>!',
        'HOME_WELCOME_TEXT' => file_get_contents(dirname(__FILE__) . '/../resources/text/welcome-de.html'),
        'UNAUTHORIZED_MESSAGE_TITLE' => 'Zugriff verweigert',
        'UNAUTHORIZED_MESSAGE_BODY' => 'Melde dich an um auf diese Seite zuzugreifen',

        # contact.php
        'CONTACT_JUMBO' => 'Kontakt',
        'ADMIN_SECTION_TITLE' => 'Administrator',
        'SOURCE_CODE_SECTION_TITLE' => 'Quellcode',

        # about.php
        'ABOUT_JUMBO' => 'Impressum',

        # signup.php
        'SIGNUP_JUMBO' => 'Anmeldung',
        'REGISTER_SECTION_TITLE' => 'Registrieren',
        'REGISTER_EMAIL_TITLE' => 'Email Adresse',
        'REGISTER_EMAIL_PLACEHOLDER' => 'email@example.com',
        'REGISTER_USERNAME_TITLE' => 'Benutzername',
        'REGISTER_USERNAME_PLACEHOLDER' => 'Benutzername',
        'REGISTER_PASSWORD_TITLE' => 'Passwort',
        'REGISTER_PASSWORD_PLACEHOLDER' => '********',
        'REGISTER_PASSWORD_REPEAT_TITLE' => 'Passwort (Wiederholung)',
        'REGISTER_PASSWORD_REPEAT_PLACEHOLDER' => '********',
        'REGISTER_SUBMIT_TITLE' => 'Absenden',
        'LOGIN_SECTION_TITLE' => 'Anmelden',
        'LOGIN_EMAIL_TITLE' => 'Email Adresse',
        'LOGIN_EMAIL_PLACEHOLDER' => 'email@example.com',
        'LOGIN_PASSWORD_TITLE' => 'Passwort',
        'LOGIN_PASSWORD_PLACEHOLDER' => '********',
        'LOGIN_SUBMIT_TITLE' => 'Absenden',

        # bets.php
        'BETS_JUMBO' => 'Wetten',
        'BUNDESLIGA_MATCHDAY_BETS_TITLE' => 'Bundesliga Spieltag',
        'BET_SUBMIT_BUTTON_TEXT' => 'Bestätigen',
        'BETS_UPDATED_TITLE' => 'Tipps aktualisiert',
        'BETS_UPDATED_BODY' => '',
        'INVALID_BET_VALUE_NEGATIVE_NUMBER_TITLE' => 'Eingegebener Wert ist negativ',
        'INVALID_BET_VALUE_NEGATIVE_NUMBER_BODY' => 'Bitte gebe einen Wert zwischen 0 und 1000 ein',
        'INVALID_BET_VALUE_TOO_HIGH_TITLE' => 'Eingegebener Wert ist zu hoch',
        'INVALID_BET_VALUE_TOO_HIGH_BODY' => 'Bitte gebe einen Wert zwischen 0 und 1000 ein',

        # match.php
        'MATCH_EVENTS_MINUTE' => 'Minute',
        'MATCH_EVENTS_SCORER' => 'Torschütze',
        'MATCH_EVENTS_TEAM_ONE_SCORE' => 'Heim',
        'MATCH_EVENTS_TEAM_TWO_SCORE' => 'Auswärts',
        'MATCH_BETS_USERNAME' => 'Nutzer',
        'MATCH_BETS_TEAM_ONE' => 'Heim',
        'MATCH_BETS_TEAM_TWO' => 'Auswärts',
        'MATCH_BETS_POINTS' => 'Punkte',

        # leaderboard.php
        'LEADERBOARD_JUMBO' => 'Rangliste',
        'LEADERBOARD_TABLE_TITLE' => 'Rangliste',
        'LEADERBOARD_POSITION_HEADER' => '#',
        'LEADERBOARD_NAME_HEADER' => 'Name',
        'LEADERBOARD_POINTS_HEADER' => 'Punkte',

        # Registration & Confirmation
        'REGISTER_ERROR_USERNAME_TOO_LONG_TITLE' => 'Benutzername zu lang',
        'REGISTER_ERROR_USERNAME_TOO_LONG_BODY' => 'Nutzernamen dürfen höchstens 60 Zeichen lang sein',
        'REGISTER_ERROR_EMAIL_TOO_LONG_TITLE' => 'Email Adresse zu lang',
        'REGISTER_ERROR_EMAIL_TOO_LONG_BODY' => 'Email Adressen dürfen maximal 100 Zeichen lang sein',
        'REGISTER_ERROR_NO_EMAIL_TITLE' => 'Keine Email Adresse',
        'REGISTER_ERROR_NO_EMAIL_BODY' => 'Bitte geb eine Email Adresse an',
        'REGISTER_ERROR_NO_USERNAME_TITLE' => 'Keine Benutzername',
        'REGISTER_ERROR_NO_USERNAME_BODY' => 'Bitte geb einen Benutzernamen an',
        'REGISTER_ERROR_NO_PASSWORD_TITLE' => 'Kein Passwort',
        'REGISTER_ERROR_NO_PASSWORD_BODY' => 'Bitte geb ein Passwort ein',
        'REGISTER_ERROR_PASSWORD_MISMATCH_TITLE' => 'Passwörter stimmen nicht überein',
        'REGISTER_ERROR_PASSWORD_MISMATCH_BODY' => 'Bitte überprüfe die Eingabe',
        'REGISTER_ERROR_PASSWORD_TOO_SHORT_TITLE' => 'Paswort zu kurz',
        'REGISTER_ERROR_PASSWORD_TOO_SHORT_BODY' => 'Bitte geb ein Passwort mit mindestens 8 Zeichen an',
        'REGISTER_ERROR_USERNAME_EXISTS_TITLE' => 'Benutzer existiert',
        'REGISTER_ERROR_USERNAME_EXISTS_BODY' => 'Dieser Besutzer existiert schon. '.
                                                 'Bitte wähle einen anderen Benutzernamen',
        'REGISTER_ERROR_EMAIL_USED_TITLE' => 'Email bereits verwendet',
        'REGISTER_ERROR_EMAIL_USED_BODY' => 'Diese Email wird berets verwendet',
        'REGISTER_ERROR_NO_RECAPTCHA_TITLE' => 'ReCaptcha fehlgeschlagen',
        'REGISTER_ERROR_NO_RECAPTCHA_BODY' => 'Bitte clicke den ReCaptcha Knopf',
        'CONFIRMATION_EMAIL_SENDER' => 'Bundesliga Tippspiel',
        'CONFIRMATION_EMAIL_TITLE' => 'Registrierung - Bestatigung',
        'CONFIRMATION_EMAIL_BODY' => '<h2>Bestätigung</h2><p>Herzlich willkommen beim Bundesliga Tippspiel!</p>' .
                                     '<p>Um deine Registrierung abzuschließen, clicke bitte den folgenden link:</p>',
        'CONFIRMATION_EMAIL_LINK_NAME' => 'Bestätigen',
        'REGISTER_SUCCESS_TITLE' => 'Registrierung abgeschlossen',
        'REGISTER_SUCCESS_BODY' => 'Schau in deinem Email Postfach für die Bestätigungs-Email',
        'CONFIRMATION_ERROR_NO_CONFIRMATION_TITLE' => 'Keine Bestätigung vorhanden',
        'CONFIRMATION_ERROR_NO_CONFIRMATION_BODY' => 'Dieses Konto kann nicht aktiviert werden',
        'CONFIRMATION_ERROR_ALREADY_CONFIRMED_TITLE' => 'Bereits bestätigt',
        'CONFIRMATION_ERROR_ALREADY_CONFIRMED_BODY' => 'Dieses Konto wurde bereits bestätigt',
        'CONFIRMATION_ERROR_TOKEN_MISMATCH_TITLE' => 'Bestätigungs-Token nicht erkannt',
        'CONFIRMATION_ERROR_TOKEN_MISMATCH_BODY' => 'Schau nach ob der Link richtig funktioniert',
        'CONFIRMATION_SUCCESS_TITLE' => 'Bestätigung Abgeschlossen',
        'CONFIRMATION_SUCCESS_BODY' => 'Du kannst dich jetzt anmelden',
        'LOGIN_ERROR_NOT_CONFIRMED_TITLE' => 'Anmeldung fehlgeschlagen',
        'LOGIN_ERROR_NOT_CONFIRMED_BODY' => 'Dein Benutzerkonto wurde noch nicht aktiviert. ' .
                                            'Schau in deinem Email Postfach nach',

        # Login
        'LOGIN_ERROR_ALREADY_LOGGED_IN_TITLE' => 'Bereits angemeldet',
        'LOGIN_ERROR_ALREADY_LOGGED_IN_BODY' => 'Du bist bereits angemeldet',
        'LOGIN_ERROR_PASSWORD_MISMATCH_TITLE' => 'Anmeldung fehlgeschlagen',
        'LOGIN_ERROR_PASSWORD_MISMATCH_BODY' => 'Bitte überprüfe deine Angaben',
        'LOGIN_ERROR_USER_DOES_NOT_EXIST_TITLE' => 'Anmeldung fehlgeschlagen',
        'LOGIN_ERROR_USER_DOES_NOT_EXIST_BODY' => 'Bitte überprüfe deine Angaben',

        # Forgotten Password / Reset
        'PASSWORD_RESET_JUMBO' => 'Passwort Zurücksetzen',
        'PASSWORD_RESET_FORM_TITLE' => 'Passwort Zurücksetzen',
        'PASSWORD_RESET_EMAIL_TITLE' => 'Email',
        'PASSWORD_RESET_FORM_BUTTON' => 'Bestätigen',
        'FORGOT_PASSWORD_TEXT' => 'Passwort vergessen?',
        'PASSWORD_RESET_DISMISSABLE_TITLE' => 'Passwort wurde zurückgesetzt',
        'PASSWORD_RESET_DISMISSABLE_BODY' => 'Schau in deinem Email Postfach für mehr Informationen nach',
        'PASSWORD_RESET_EMAIL_SUBJECT' => 'Passwort Zurücksetzung',
        'PASSWORD_RESET_EMAIL_BODY' => '<h2>Passwort zurückgesetzt</h2>' .
            '<p>Dein Passwort wurde zurückgesetzt, bitte verwende das folgende Password um dich anzumelden:</p>' .
            '<p>@TEMPORARY_PASSWORD</p>' .
            '<p>Bitte ändere dieses Passwort zeitnah auf der Profilseite</p>',

        # Comments
        'COMMENT_ERROR_NOT_LOGGED_IN_TITLE' => 'Nicht angemeldet',
        'COMMENT_ERROR_NOT_LOGGED_IN_BODY' => 'Du musst angemeldet sein um kommentieren zu können',
        'COMMENT_ERROR_NO_CONTENT_BODY_TITLE' => 'Kein Inhalt',
        'COMMENT_ERROR_NO_CONTENT_BODY_BODY' => 'Es konnte kein Kommentar erstellt werden',
        'COMMENT_ERROR_EMPTY_TITLE' => 'Kommentar leer',
        'COMMENT_ERROR_EMPTY_BODY' => 'Es kann kein leeres Kommentar erstellt werden',
        'COMMENT_ERROR_TOO_LONG_TITLE' => 'Kommentar zu lang',
        'COMMENT_ERROR_TOO_LONG_BODY' => 'Das Limit für Kommentare ist 255 Zeichen',
        'COMMENT_ERROR_RECENT_ACTIVITY_TITLE' => 'Zu viele Kommentare',
        'COMMENT_ERROR_RECENT_ACTIVITY_BODY' => 'Bitte warte bis zu 10 Sekunden um wieder kommentieren zu können',
        'YOUR_COMMENT_HERE_TEXT' => 'Kommentar',
        'COMMENT_SUBMIT_BUTTON' => 'Schicken',
        'DELETE_COMMENT_BUTTON' => 'Löschen',
        'DELETED_COMMENT_USER' => 'Gelöscht',
        'DELETED_COMMENT_MESSAGE' => 'Gelöscht',

        # Profile Page
        'PROFILE_PASSWORD_CHANGE_TITLE' => 'Passwort ändern',
        'PROFILE_PASSWORD_CHANGE_CURRENT_LABEL' => 'Derzeitiges Passwort',
        'PROFILE_PASSWORD_CHANGE_NEW_LABEL' => 'Neues Passwort',
        'PROFILE_PASSWORD_RESET_CHANGE_REPEAT_LABEL' => 'Neues Passwort (Wiederholen)',
        'PROFILE_PASSWORD_CHANGE_SUBMIT' => 'Bestätigen',
        'PASSWORD_CHANGE_CURRENT_WRONG_TITLE' => 'Falsches Passwort',
        'PASSWORD_CHANGE_CURRENT_WRONG_BODY' => 'Bitte geb dein derzeitiges Passwort ein',
        'PASSWORD_CHANGE_TOO_SHORT_TITLE' => 'Passwort zu kurz',
        'PASSWORD_CHANGE_TOO_SHORT_BODY' => 'Geb bitte ein Passwort mit mindestens 8 Zeichen an',
        'PASSWORD_CHANGE_MISMATCH_TITLE' => 'Passwörter stimmen nicht überein',
        'PASSWORD_CHANGE_MISMATCH_BODY' => 'Bitte stell sicher dass die Passwörter dieselben sind',
        'PASSWORD_CHANGE_SUCCESS_TITLE' => 'Passwort geändert',
        'PASSWORD_CHANGE_SUCCESS_BODY' => 'Melde dich ab jetzt mit deinem neuen Passwort an.',
        'PROFILE_USERNAME_CHANGE_TITLE' => 'Benutzernamen ändern',
        'PROFILE_NEW_USERNAME_LABEL' => 'Neuer Benutzername',
        'PROFILE_USERNAME_CHANGE_SUBMIT' => 'Bestätigen',
        'USERNAME_CHANGE_NAME_TAKEN_TITLE' => 'Benutzername bereits vergeben',
        'USERNAME_CHANGE_NAME_TAKEN_BODY' => 'Bitte wähle einen anderen Nutzernamen',
        'USERNAME_CHANGE_EMPTY_TITLE' => 'Benutzername ist leer',
        'USERNAME_CHANGE_EMPTY_BODY' => 'Der Benutzername darf nicht leer sein',
        'USERNAME_CHANGE_TOO_LONG_TITLE' => "Benutzername zu lang",
        'USERNAME_CHANGE_TOO_LONG_BODY' => "Verwende bitte einen Nutzernamen mit weniger als 60 Zeichen",
        'USERNAME_CHANGE_SUCCESS_TITLE' => "Benutzername erfolgreich verändert",
        'USERNAME_CHANGE_SUCCESS_BODY' => ''
    );
}