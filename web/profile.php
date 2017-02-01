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

include_once 'php/gets.php';
include_once 'php/session.php';
include_once 'templates/form.php';
include_once 'templates/navbar.php';
include_once 'templates/header.php';
include_once 'templates/betform.php';
include_once 'strings/dictionary.php';
include_once 'templates/title_jumbotron.php';

initializeSession();
redirectInvalidUser();
processGlobalGets();
$dictionary = new Dictionary($_SESSION['language']);

(new Header('@$PROFILE_TITLE'))->echo();
echo '<body>';
generateDefaultHeaderNavbar('profile.php')->echo();
(new TitleJumboTron($_SESSION['userdata']['name']))->echo();
processDismissableMessages();

?>
    <div class="row">
        <div class="col-lg-3"></div>
        <div class="col-lg-6">
            <?php (new Form('@$PROFILE_PASSWORD_CHANGE_TITLE', 'actions/password_change.php', array(
                new FormTextEntry('@$PROFILE_PASSWORD_CHANGE_CURRENT_LABEL',
                    'current', 'password', '********', 'current'),
                new FormTextEntry('@$PROFILE_PASSWORD_CHANGE_NEW_LABEL',
                    'new', 'password', '********', 'new'),
                new FormTextEntry('@$PROFILE_PASSWORD_RESET_CHANGE_REPEAT_LABEL',
                    'repeat', 'password', '********', 'repeat'),
                new ConfirmationButton('@$PROFILE_PASSWORD_CHANGE_SUBMIT'))))->echo(); ?>
        </div>
        <div class="col-lg-3"></div>
    </div>
<?php

generateFooter('signup.php')->echoWithContainer();
echo '</body>';
