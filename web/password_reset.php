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

(new Header('@$PASSWORD_RESET_TITLE'))->echo();
echo '<body>';
generateDefaultHeaderNavbar('password_reset.php')->echo();
(new TitleJumboTron('@$PASSWORD_RESET_JUMBO'))->echo();
processDismissableMessages();

$reset_form = new Form('@$PASSWORD_RESET_FORM_TITLE', 'actions/password_reset.php', array(
    new FormTextEntry('@$PASSWORD_RESET_EMAIL_TITLE', 'reset_email', 'text', 'email@example.com', 'email'),
    new ConfirmationButton('@$PASSWORD_RESET_FORM_BUTTON')
));

?>
    <div class="row">
        <div class="col-lg-3"></div>
        <div class="col-lg-6">
            <?php $reset_form->echo(); ?>
        </div>
        <div class="col-lg-3"></div>
    </div>
<?php


generateFooter('password_reset.php')->echoWithContainer();
echo '</body>';
