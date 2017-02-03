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

include_once 'php/page.php';
include_once 'templates/form.php';

$page = new Page('@$PASSWORD_RESET_TITLE', 'password_reset.php', '@$PASSWORD_RESET_JUMBO', array(), false);

$reset_form = new Form('@$PASSWORD_RESET_FORM_TITLE', 'actions/password_reset.php', array(
    new FormTextEntry('@$PASSWORD_RESET_EMAIL_TITLE', 'reset_email', 'text', 'email@example.com', 'email'),
    new ConfirmationButton('@$PASSWORD_RESET_FORM_BUTTON')
));

$page->addStringBodyElement('<div class="row"><div class="col-sm-3"></div><div class="col-sm-6">');
$page->addGeneratorBodyElement($reset_form);
$page->addStringBodyElement('</div><div class="col-sm-3"></div></div>');

$page->display();
