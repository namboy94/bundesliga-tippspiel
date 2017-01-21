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

        # NAVBAR TITLES
        'WEBSITE_NAME' => 'Bundesliga Betting Game',
        'HOME_NAV_TITLE' => 'Home',
        'LOGIN_NAV_TITLE' => 'Login',
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
        'SOURCE_CODE_SECTION_TITLE' => 'Source Code'

    );
}
