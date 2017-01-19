<?php

function get_english_dictionary() {

	return array(

		'@$ADMIN_CONTACT_TITLE' => 'Admin / Developer',
		'@$SOURCE_CODE_TITLE' => "Source Code",
        '@$WEBSITE_NAME' => "Bundesliga Betting Game",
		'@$HOME_TITLE' => "Bundesliga Betting Game - HOME",
		'@$ABOUT_TITLE' => "Bundesliga Betting Game - ABOUT",
		'@$CONTACT_TITLE' => "Bundesliga Betting Game - CONTACT",
        '@$SIGNUP_TITLE' => "Bundesliga Betting Game - Login",
		'@$NAVBAR_TITLE' => "Bundesliga Betting Game",
		'@$HOME_NAV' => "Home",
		'@$ABOUT_NAV' => "About",
		'@$CONTACT_NAV' => "Contact",
        '@$SIGNUP_NAV' => "Login",
		'@$THEMES_NAV' => "Themes",
		'@$GERMAN_LANG' => "German",
		'@$ENGLISH_LANG' => "English",
		'@$DEFAULT_THEME' => "Default",
		'@$TERMINAL_THEME' => "Terminal",
		'@$GITLAB_NAME' => "Gitlab",
		'@$ABOUT_TEXT' => file_get_contents("resources/impressum.en", true),
        '@$SIGNUP_HEADER' => "Signup",
        '@$LOGIN_HEADER' => "Log In",
        '@$EMAIL_TITLE' => "Email Address",
        '@$USERNAME_TITLE' => "Username",
        '@$PASSWORD_TITLE' => "Password",
        '@$SUBMIT_TITLE' => "Confirm",
        '@$PASSWORD_REPEAT' => "Password (Repeat)",
        '@$EMAIL_CONFIRMATION' => "Thank you for signing up for the Bundesliga Betting Game!\n\n" .
                                  "To finish your registration, click on the link below:\n\n",
        '@$CONFIRMATION_NAME' => "Confirmation"

	);

}

?>