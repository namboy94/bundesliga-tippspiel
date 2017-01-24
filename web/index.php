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
        <div class="col-sm-8 text-center">
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

            Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.

            Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi.

            Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer
        </div>
        <div class="col-sm-4">
            <?php
            if (!isLoggedIn()) {
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