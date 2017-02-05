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
 * Generates an english dictionary
 * @return array: the english dictionary
 */
function get_english() {
    return array(

        # HEADER TITLES
        'HOME_TITLE' => 'Bundesliga Betting Game - Home',
        'CONTACT_TITLE' => 'Bundesliga Betting Game - Contact',
        'ABOUT_TITLE' => 'Bundesliga Betting Game - About',
        'SIGNUP_TITLE' => 'Bundesliga Betting Game - Login and Register',
        'BETS_TITLE' => 'Bundesliga Betting Game - Bets',
        'LEADERBOARD_TITLE' => 'Bundesliga Betting Game - Leaderboard',
        'PROFILE_TITLE' => 'Bundesliga Betting Game - Profile',

        # NAVBAR TITLES
        'WEBSITE_NAME' => 'Bundesliga Betting Game',
        'HOME_NAV_TITLE' => 'Home',
        'LOGIN_NAV_TITLE' => 'Login',
        'LOGOUT_NAV_TITLE' => 'Log Out',
        'BETS_NAV_TITLE' => 'Bets',
        'LEADERBOARD_NAV_TITLE' => 'Rankings',
        'PROFILE_NAV_TITLE' => 'Profile',
        'THEMES_NAV_TITLE' => 'Themes',
        'THEME_DEFAULT_NAV_TITLE' => 'Default',
        'THEME_TERMINAL_NAV_TITLE' => 'Terminal',
        'LANGUAGES_NAV_TITLE' => 'Languages',
        'LANGUAGE_GERMAN_NAV_TITLE' => 'German',
        'LANGUAGE_ENGLISH_NAV_TITLE' => 'English',
        'FOOTER_IMPRESSUM_TITLE' => 'About',
        'FOOTER_COPYRIGHT_TEXT' => '© Hermann Krumrey 2017',
        'FOOTER_VERSION_TEXT' => file_get_contents(dirname(__FILE__) . '/../resources/version'),

        # index.php
        'HOME_JUMBO' => 'Bundesliga Betting Game',
        'OR_SIGN_UP_TEXT' => 'Or sign up <a href="signup.php">here</a>!',
        'HOME_WELCOME_TEXT' => file_get_contents(dirname(__FILE__) . '/../resources/text/welcome-en.html'),
        'UNAUTHORIZED_MESSAGE_TITLE' => 'Unauthorized',
        'UNAUTHORIZED_MESSAGE_BODY' => 'You are not logged in',

        # contact.php
        'CONTACT_JUMBO' => 'Contact',
        'ADMIN_SECTION_TITLE' => 'Administrator',
        'SOURCE_CODE_SECTION_TITLE' => 'Source Code',

        # about.php
        'ABOUT_JUMBO' => 'About',

        # signup.php
        'SIGNUP_JUMBO' => 'Sign Up',
        'REGISTER_SECTION_TITLE' => 'Register',
        'REGISTER_EMAIL_TITLE' => 'Email Address',
        'REGISTER_EMAIL_PLACEHOLDER' => 'email@example.com',
        'REGISTER_USERNAME_TITLE' => 'Username',
        'REGISTER_USERNAME_PLACEHOLDER' => 'Username',
        'REGISTER_PASSWORD_TITLE' => 'Password',
        'REGISTER_PASSWORD_PLACEHOLDER' => '********',
        'REGISTER_PASSWORD_REPEAT_TITLE' => 'Password (Repeat)',
        'REGISTER_PASSWORD_REPEAT_PLACEHOLDER' => '********',
        'REGISTER_SUBMIT_TITLE' => 'Submit',
        'LOGIN_SECTION_TITLE' => 'Login',
        'LOGIN_EMAIL_TITLE' => 'Email Address',
        'LOGIN_EMAIL_PLACEHOLDER' => 'email@example.com',
        'LOGIN_PASSWORD_TITLE' => 'Password',
        'LOGIN_PASSWORD_PLACEHOLDER' => '********',
        'LOGIN_SUBMIT_TITLE' => 'Submit',

        # bets.php
        'BETS_JUMBO' => 'Bets',
        'BUNDESLIGA_MATCHDAY_BETS_TITLE' => 'Bundesliga Matchday',
        'BET_SUBMIT_BUTTON_TEXT' => 'Confirm',
        'BETS_UPDATED_TITLE' => 'Bets updated',
        'BETS_UPDATED_BODY' => '',
        'INVALID_BET_VALUE_NEGATIVE_NUMBER_TITLE' => 'Input value is negative',
        'INVALID_BET_VALUE_NEGATIVE_NUMBER_BODY' => 'Please enter a value between 0 and 1000',
        'INVALID_BET_VALUE_TOO_HIGH_TITLE' => 'Input value too high',
        'INVALID_BET_VALUE_TOO_HIGH_BODY' => 'Please enter a value between 0 and 1000',

        # match.php
        'MATCH_EVENTS_MINUTE' => 'Minute',
        'MATCH_EVENTS_SCORER' => 'Scorer',
        'MATCH_EVENTS_TEAM_ONE_SCORE' => 'Home',
        'MATCH_EVENTS_TEAM_TWO_SCORE' => 'Away',
        'MATCH_BETS_USERNAME' => 'User',
        'MATCH_BETS_TEAM_ONE' => 'Home',
        'MATCH_BETS_TEAM_TWO' => 'Away',
        'MATCH_BETS_POINTS' => 'Points',

        # leaderboard.php
        'LEADERBOARD_JUMBO' => 'Leaderboard',
        'LEADERBOARD_TABLE_TITLE' => 'Leaderboard',
        'LEADERBOARD_POSITION_HEADER' => '#',
        'LEADERBOARD_NAME_HEADER' => 'Name',
        'LEADERBOARD_POINTS_HEADER' => 'Points',

        # Registration & Confirmation
        'REGISTER_ERROR_USERNAME_TOO_LONG_TITLE' => 'Username too long',
        'REGISTER_ERROR_USERNAME_TOO_LONG_BODY' => 'Please limit your username to a maximum of 60 characters',
        'REGISTER_ERROR_EMAIL_TOO_LONG_TITLE' => 'Email address too long',
        'REGISTER_ERROR_EMAIL_TOO_LONG_BODY' => 'Email addresses with more than 100 characters are not supported',
        'REGISTER_ERROR_NO_EMAIL_TITLE' => 'No Email Address Provided',
        'REGISTER_ERROR_NO_EMAIL_BODY' => 'Please enter a valid email address',
        'REGISTER_ERROR_NO_USERNAME_TITLE' => 'No username provided',
        'REGISTER_ERROR_NO_USERNAME_BODY' => 'Please enter a username',
        'REGISTER_ERROR_NO_PASSWORD_TITLE' => 'No password provided',
        'REGISTER_ERROR_NO_PASSWORD_BODY' => 'Please enter a password',
        'REGISTER_ERROR_PASSWORD_MISMATCH_TITLE' => 'Passwords do not match',
        'REGISTER_ERROR_PASSWORD_MISMATCH_BODY' => 'Please make sure that the two passwords are the same',
        'REGISTER_ERROR_PASSWORD_TOO_SHORT_TITLE' => 'Password too short',
        'REGISTER_ERROR_PASSWORD_TOO_SHORT_BODY' => 'Please enter a password with 8 or more characters',
        'REGISTER_ERROR_USERNAME_EXISTS_TITLE' => 'Username exists',
        'REGISTER_ERROR_USERNAME_EXISTS_BODY' => 'Please choose a different username',
        'REGISTER_ERROR_EMAIL_USED_TITLE' => 'Email already in use',
        'REGISTER_ERROR_EMAIL_USED_BODY' => 'This email is already bound to an account',
        'REGISTER_ERROR_NO_RECAPTCHA_TITLE' => 'ReCaptcha Failed',
        'REGISTER_ERROR_NO_RECAPTCHA_BODY' => 'Please press the ReCaptcha button again',
        'CONFIRMATION_EMAIL_SENDER' => 'Bundesliga Betting Game',
        'CONFIRMATION_EMAIL_TITLE' => 'Registration Confirmation',
        'CONFIRMATION_EMAIL_BODY' => '<h2>Confirmation</h2><p>Welcome to the Bundesliga Betting Game!</p>' .
                                     '<p>To complete your registration please click on the following link:</p>',
        'CONFIRMATION_EMAIL_LINK_NAME' => 'Confirm',
        'REGISTER_SUCCESS_TITLE' => 'Registration Successul',
        'REGISTER_SUCCESS_BODY' => 'Check your inbox for the confirmation email',
        'CONFIRMATION_ERROR_NO_CONFIRMATION_TITLE' => 'No confirmation available',
        'CONFIRMATION_ERROR_NO_CONFIRMATION_BODY' => 'This account can not be activated',
        'CONFIRMATION_ERROR_ALREADY_CONFIRMED_TITLE' => 'Already confirmed',
        'CONFIRMATION_ERROR_ALREADY_CONFIRMED_BODY' => 'This account is already confirmed',
        'CONFIRMATION_ERROR_TOKEN_MISMATCH_TITLE' => 'Confirmation token not recognized',
        'CONFIRMATION_ERROR_TOKEN_MISMATCH_BODY' => 'Please check if the link is correct',
        'CONFIRMATION_SUCCESS_TITLE' => 'Confirmation successful',
        'CONFIRMATION_SUCCESS_BODY' => 'You can now log in',
        'LOGIN_ERROR_NOT_CONFIRMED_TITLE' => 'Login failed',
        'LOGIN_ERROR_NOT_CONFIRMED_BODY' => 'Your account has not been activated. Please check your inbox',

        # Login
        'LOGIN_ERROR_ALREADY_LOGGED_IN_TITLE' => 'Already logged in',
        'LOGIN_ERROR_ALREADY_LOGGED_IN_BODY' => 'You are already logged in',
        'LOGIN_ERROR_PASSWORD_MISMATCH_TITLE' => 'Authentication Error',
        'LOGIN_ERROR_PASSWORD_MISMATCH_BODY' => 'Please check your credentials',
        'LOGIN_ERROR_USER_DOES_NOT_EXIST_TITLE' => 'Authentication Error',
        'LOGIN_ERROR_USER_DOES_NOT_EXIST_BODY' => 'Please check your credentials',

        # Forgotten Password / Reset
        'PASSWORD_RESET_JUMBO' => 'Password Reset',
        'PASSWORD_RESET_FORM_TITLE' => 'Password Reset',
        'PASSWORD_RESET_EMAIL_TITLE' => 'Email',
        'PASSWORD_RESET_FORM_BUTTON' => 'Submit',
        'FORGOT_PASSWORD_TEXT' => 'Forgot Password?',
        'PASSWORD_RESET_DISMISSABLE_TITLE' => 'Password was reset',
        'PASSWORD_RESET_DISMISSABLE_BODY' => 'Check your inbox for further information',
        'PASSWORD_RESET_EMAIL_SUBJECT' => 'Password Reset',
        'PASSWORD_RESET_EMAIL_BODY' => '<h2>Password Reset</h2>' .
                                       '<p>Your password was reset. Please use the following password to log in:</p>' .
                                       '<p>@TEMPORARY_PASSWORD</p>' .
                                       '<p>Please change the password as soon as possible using the profile page</p>',

        # Comments
        'COMMENT_ERROR_NOT_LOGGED_IN_TITLE' => 'Not logged in',
        'COMMENT_ERROR_NOT_LOGGED_IN_BODY' => 'You need to be logged in to comment',
        'COMMENT_ERROR_NO_CONTENT_BODY_TITLE' => 'No Content',
        'COMMENT_ERROR_NO_CONTENT_BODY_BODY' => 'Could not create a new comment',
        'COMMENT_ERROR_EMPTY_TITLE' => 'Comment field empty',
        'COMMENT_ERROR_EMPTY_BODY' => 'You can not leave an empty comment',
        'COMMENT_ERROR_TOO_LONG_TITLE' => 'Comment too long',
        'COMMENT_ERROR_TOO_LONG_BODY' => 'The comment limit is 255 characters',
        'YOUR_COMMENT_HERE_TEXT' => 'Your comment here',
        'COMMENT_SUBMIT_BUTTON' => 'Submit',

        # Profile Page
        'PROFILE_PASSWORD_CHANGE_TITLE' => 'Change Password',
        'PROFILE_PASSWORD_CHANGE_CURRENT_LABEL' => 'Current Password',
        'PROFILE_PASSWORD_CHANGE_NEW_LABEL' => 'New Password',
        'PROFILE_PASSWORD_RESET_CHANGE_REPEAT_LABEL' => 'New Password (Repeat)',
        'PROFILE_PASSWORD_CHANGE_SUBMIT' => 'Confirm',
        'PASSWORD_CHANGE_CURRENT_WRONG_TITLE' => 'Wrong Password',
        'PASSWORD_CHANGE_CURRENT_WRONG_BODY' => 'Please enter your current password',
        'PASSWORD_CHANGE_TOO_SHORT_TITLE' => 'Password too short',
        'PASSWORD_CHANGE_TOO_SHORT_BODY' => 'Please enter a password with at least 8 characters',
        'PASSWORD_CHANGE_MISMATCH_TITLE' => 'Passwords do not match',
        'PASSWORD_CHANGE_MISMATCH_BODY' => 'Please make sure that your entry is correct',
        'PASSWORD_CHANGE_SUCCESS_TITLE' => 'Password changed',
        'PASSWORD_CHANGE_SUCCESS_BODY' => 'Please log in using your new password in the future',
        'PROFILE_USERNAME_CHANGE_TITLE' => 'Change Username',
        'PROFILE_NEW_USERNAME_LABEL' => 'New Username',
        'PROFILE_USERNAME_CHANGE_SUBMIT' => 'Confirm',
        'USERNAME_CHANGE_NAME_TAKEN_TITLE' => 'Username already taken',
        'USERNAME_CHANGE_NAME_TAKEN_BODY' => 'Please choose a different username',
        'USERNAME_CHANGE_EMPTY_TITLE' => 'Username is empty',
        'USERNAME_CHANGE_EMPTY_BODY' => 'The username can not be empty',
        'USERNAME_CHANGE_TOO_LONG_TITLE' => "Username too long",
        'USERNAME_CHANGE_TOO_LONG_BODY' => "Please enter a username with less than 60 characters",
        'USERNAME_CHANGE_SUCCESS_TITLE' => "Username successfully changed",
        'USERNAME_CHANGE_SUCCESS_BODY' => ''

);
}
