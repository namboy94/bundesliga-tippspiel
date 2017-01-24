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

include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

/**
 * Process GET requests that act the same on every page (e.g. switching the theme)
 */
function processGlobalGets() {

    if (isset($_GET['theme'])) {
        $_SESSION['theme'] = $_GET['theme'];
    }
    if (isset($_GET['language'])) {
        $_SESSION['language'] = $_GET['language'];
    }
}

/**
 * Processes displaying dismissable messages
 */
function processDismissableMessages() {

    foreach(array('error', 'warning', 'info', 'success') as $dismissable) {
        if (isset($_SESSION[$dismissable])) {
            DismissableMessage::fromArray($_SESSION[$dismissable])->echo();
            unset($_SESSION[$dismissable]);
        }
    }

}