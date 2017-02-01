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
include_once 'templates/header.php';
include_once 'templates/navbar.php';
include_once 'strings/dictionary.php';
include_once 'templates/title_jumbotron.php';

initializeSession();
processGlobalGets();
$dictionary = new Dictionary($_SESSION['language']);

(new Header('@$SIGNUP_TITLE'))->echo();
echo '<body>';
generateDefaultHeaderNavbar('signup.php')->echo();
(new TitleJumboTron('@$SIGNUP_JUMBO'))->echo();
processDismissableMessages();

$signup_form = new Form('@$REGISTER_SECTION_TITLE', 'actions/register.php', array(
    new FormTextEntry('@$REGISTER_EMAIL_TITLE', 'register_email', 'text',
        '@$REGISTER_EMAIL_PLACEHOLDER', 'reg_email'),
    new FormTextEntry('@$REGISTER_USERNAME_TITLE', 'register_username', 'text',
        '@$REGISTER_USERNAME_PLACEHOLDER', 'reg_username'),
    new FormTextEntry('@$REGISTER_PASSWORD_TITLE', 'register_password', 'password',
        '@$REGISTER_PASSWORD_PLACEHOLDER', 'reg_password'),
    new FormTextEntry('@$REGISTER_PASSWORD_REPEAT_TITLE', 'register_password_repeat', 'password',
        '@$REGISTER_PASSWORD_REPEAT_PLACEHOLDER', 'reg_password_repeat'),
    new ConfirmationButton('@$REGISTER_SUBMIT_TITLE')
));

$login_form = new Form('@$LOGIN_SECTION_TITLE', 'actions/login.php', array(
    new FormTextEntry('@$LOGIN_EMAIL_TITLE', 'login_email', 'text',
        '@$LOGIN_EMAIL_PLACEHOLDER', 'login_email_id'),
    new FormTextEntry('@$LOGIN_PASSWORD_TITLE', 'login_password', 'password',
        '@$LOGIN_PASSWORD_PLACEHOLDER', 'login_password_id'),
    new ConfirmationButton('@$LOGIN_SUBMIT_TITLE')
));

?>
<div class="container">
    <div class="row">
        <div class="col-sm-5 col-md-5 col-lg-5">
            <?php $signup_form->echo(); ?>
        </div>
        <div class="col-sm-2 col-md-2 col-lg-2">
            <hr width="1" size="500">
        </div>
        <div class="col-sm-5 col-md-5 col-lg-5">
            <?php $login_form->echo(); ?>
            <a href="password_reset.php"><?php echo $dictionary->translate('@$FORGOT_PASSWORD_TEXT'); ?></a>
        </div>
    </div>
</div>
<?php

generateFooter('signup.php')->echoWithContainer();
echo '</body>';
