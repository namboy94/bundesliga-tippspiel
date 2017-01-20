<?php

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
        '@$INVALID_CREDENTIALS_BODY' => "Bitte überprüfe deine Login Daten"

	);

}

?>