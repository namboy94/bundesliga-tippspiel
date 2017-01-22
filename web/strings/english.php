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

        # NAVBAR TITLES
        'WEBSITE_NAME' => 'Bundesliga Betting Game',
        'HOME_NAV_TITLE' => 'Home',
        'LOGIN_NAV_TITLE' => 'Login',
        'LOGOUT_NAV_TITLE' => 'Log Out',
        'THEMES_NAV_TITLE' => 'Themes',
        'THEME_DEFAULT_NAV_TITLE' => 'Default',
        'THEME_TERMINAL_NAV_TITLE' => 'Terminal',
        'LANGUAGES_NAV_TITLE' => 'Languages',
        'LANGUAGE_GERMAN_NAV_TITLE' => 'German',
        'LANGUAGE_ENGLISH_NAV_TITLE' => 'English',
        'FOOTER_IMPRESSUM_TITLE' => 'About',
        'FOOTER_COPYRIGHT_TEXT' => '© Hermann Krumrey 2017',
        'FOOTER_VERSION_TEXT' => '0.1.0',

        # contact.php
        'CONTACT_JUMBO' => 'Contact',
        'ADMIN_SECTION_TITLE' => 'Administrator',
        'SOURCE_CODE_SECTION_TITLE' => 'Source Code',

        # about.php
        'ABOUT_JUMBO' => 'About',

        # signup.php
        'SIGNUP_JUMBO' => '',
        'REGISTER_SECTION_TITLE' => '',
        'REGISTER_EMAIL_TITLE' => '',
        'REGISTER_EMAIL_PLACEHOLDER' => '',
        'REGISTER_USERNAME_TITLE' => '',
        'REGISTER_USERNAME_PLACEHOLDER' => '',
        'REGISTER_PASSWORD_TITLE' => '',
        'REGISTER_PASSWORD_PLACEHOLDER' => '',
        'REGISTER_PASSWORD_REPEAT_TITLE' => '',
        'REGISTER_PASSWORD_REPEAT_PLACEHOLDER' => '',
        'REGISTER_SUBMIT_TITLE' => '',
        'LOGIN_SECTION_TITLE' => '',
        'LOGIN_EMAIL_TITLE' => '',
        'LOGIN_EMAIL_PLACEHOLDER' => '',
        'LOGIN_PASSWORD_TITLE' => '',
        'LOGIN_PASSWORD_PLACEHOLDER' => '',
        'LOGIN_SUBMIT_TITLE' => '',

        # Registration & Confirmation
        'REGISTER_ERROR_NO_EMAIL_TITLE' => '',
        'REGISTER_ERROR_NO_EMAIL_BODY' => '',
        'REGISTER_ERROR_NO_USERNAME_TITLE' => '',
        'REGISTER_ERROR_NO_USERNAME_BODY' => '',
        'REGISTER_ERROR_NO_PASSWORD_TITLE' => '',
        'REGISTER_ERROR_NO_PASSWORD_BODY' => '',
        'REGISTER_ERROR_PASSWORD_MISMATCH_TITLE' => '',
        'REGISTER_ERROR_PASSWORD_MISMATCH_BODY' => '',
        'REGISTER_ERROR_PASSWORD_TOO_SHORT_TITLE' => '',
        'REGISTER_ERROR_PASSWORD_TOO_SHORT_BODY' => '',
        'REGISTER_ERROR_USERNAME_EXISTS_TITLE' => '',
        'REGISTER_ERROR_USERNAME_EXISTS_BODY' => '',
        'REGISTER_ERROR_EMAIL_USED_TITLE' => '',
        'REGISTER_ERROR_EMAIL_USED_BODY' => '',
        'CONFIRMATION_EMAIL_SENDER' => '',
        'CONFIRMATION_EMAIL_TITLE' => '',
        'CONFIRMATION_EMAIL_BODY' => '',
        'CONFIRMATION_EMAIL_LINK_NAME' => '',
        'REGISTER_SUCCESS_TITLE' => '',
        'REGISTER_SUCCESS_BODY' => '',
        'CONFIRMATION_ERROR_NO_CONFIRMATION_TITLE' => '',
        'CONFIRMATION_ERROR_NO_CONFIRMATION_BODY' => '',
        'CONFIRMATION_ERROR_ALREADY_CONFIRMED_TITLE' => '',
        'CONFIRMATION_ERROR_ALREADY_CONFIRMED_BODY' => '',
        'CONFIRMATION_ERROR_TOKEN_MISMATCH_TITLE' => '',
        'CONFIRMATION_ERROR_TOKEN_MISMATCH_BODY' => '',
        'CONFIRMATION_SUCCESS_TITLE' => '',
        'CONFIRMATION_SUCCESS_BODY' => '',

        # Login
        'LOGIN_ERROR_ALREADY_LOGGED_IN_TITLE' => '',
        'LOGIN_ERROR_ALREADY_LOGGED_IN_BODY' => '',
        'LOGIN_ERROR_PASSWORD_MISMATCH_TITLE' => '',
        'LOGIN_ERROR_PASSWORD_MISMATCH_BODY' => '',
        'LOGIN_ERROR_USER_DOES_NOT_EXIST_TITLE' => '',
        'LOGIN_ERROR_USER_DOES_NOT_EXIST_BODY' => '',

    );
}
