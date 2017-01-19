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
        '@$CONFIRMATION_NAME' => "Confirmation"

	);

}

?>