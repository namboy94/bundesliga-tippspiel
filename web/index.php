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
processGlobalGets();
$dictionary = new Dictionary($_SESSION['language']);

(new Header('@$HOME_TITLE'))->echo();

echo '<body>';

$login_form = new Form('@$LOGIN_SECTION_TITLE', 'actions/login.php', array(
    new FormTextEntry('@$LOGIN_EMAIL_TITLE', 'login_email', 'text',
        '@$LOGIN_EMAIL_PLACEHOLDER', 'login_email_id'),
    new FormTextEntry('@$LOGIN_PASSWORD_TITLE', 'login_password', 'password',
        '@$LOGIN_PASSWORD_PLACEHOLDER', 'login_password_id'),
    new ConfirmationButton('@$LOGIN_SUBMIT_TITLE')
));

generateDefaultHeaderNavbar('index.php')->echo();

if (isLoggedIn()) {
    (new TitleJumboTron($_SESSION['userdata']['name']))->echo();
}
else {
    (new TitleJumboTron('@$HOME_JUMBO'))->echo();
}

processDismissableMessages();

?>
<div class="container">
    <div class="row">
        <?php if (isLoggedIn()) {
            echo '<div class="col-sm-6 text-center">';
        }
        else {
            echo '<div class="col-sm-8 text-center">';
        }
        echo $dictionary->translate('@$HOME_WELCOME_TEXT');
        ?>
        </div>
        <?php
        if (isLoggedIn()) {
            echo '<div class="col-sm-6">';
            $betform = new BetForm(-1, true);
            $betform->echo();
        }
        else {
            echo '<div class="col-sm-4">';
            $login_form->echo();
            echo $dictionary->translate('<h5>@$OR_SIGN_UP_TEXT</h5>');
        }
        ?>
        </div>
    </div>
</div>
<?php

generateFooter('index.php')->echoWithContainer();

echo '</body>';