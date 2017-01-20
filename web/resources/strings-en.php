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
        '@$CONFIRMATION_NAME' => "Confirmation",
        '@$PASSWORD_MISMATCH_TITLE' => "Password Mismatch",
        '@$PASSWORD_MISMATCH_BODY' => "Please enter your password again",
        '@$NO_EMAIL_TITLE' => "No email address entered",
        '@$NO_EMAIL_BODY' => "Please enter a valid email address",
        '@$NO_USERNAME_TITLE' => "No username provided",
        '@$NO_USERNAME_BODY' => "Please enter a username",
        '@$NO_PASSWORD_TITLE' => "No password entered",
        '@$NO_PASSWORD_BODY' => "Please enter a password",
        '@$USERNAME_EXISTS_TITLE' => "This username already exists",
        '@$USERNAME_EXISTST_BODY' => "Please use a different username",
        '@$EMAIL_USED_TITLE' => "This email address is was already used",
        '@$EMAIL_USED_BODY' => "Please use a different email address",
        '@$PASSWORD_TOO_SHORT_TITLE' => "This password is too short",
        '@$PASSWORD_TOO_SHORT_BODY' => "Please enter a password with at least 8 characters",
        '@$INVALID_CREDENTIALS_TITLE' => 'Login Failed',
        '@$INVALID_CREDENTIALS_BODY' => "Please check your login data",
        '@$REGISTRATION_INITIALIZED_TITLE' => "Registration Complete",
        '@$REGISTRATION_INITIALIZED_BODY' => "Check your inbox for the confirmation email",
        '@$ALREADY_CONFIRMED_TITLE' => 'Registration Already Complete',
        '@$ALREADY_CONFIRMED_BODY' => 'You can log in using your email address and password',
        '@$CONFIRMATION_NOT_MATCHING_TITLE' => 'Confirmation Link invalid',
        '@$CONFIRMATION_NOT_MATCHING_BODY' => 'Make sure you clicked the correct link',
        '@$NOT_EXISTING_USER_TITLE' => 'This username does not exist',
        '@$NOT_EXISTING_USER_BODY' => 'Make sure you clicked the correct link',
        '@$REGISTRATION_SUCCESS_TITLE' => "Account confirmed",
        '@$REGISTRATION_SUCCESS_BODY' => "You can now log in"


	);

}

?>