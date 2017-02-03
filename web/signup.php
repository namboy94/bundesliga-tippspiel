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

$page = new Page('@$SIGNUP_TITLE', 'signup.php', '@$SIGNUP_JUMBO', array(), false);

$page->addStringBodyElement('<div class="container"><div class="row"><div class="col-sm-5">');
$page->addGeneratorBodyElement(generateRegistrationForm());
$page->addStringBodyElement('</div><div class="col-sm-2"></div><div class="col-sm-5">');
$page->addGeneratorBodyElement(generateLoginForm());
$page->addStringBodyElement('<a href="password_reset.php">@$FORGOT_PASSWORD_TEXT</a>');
$page->addStringBodyElement('</div></div></div>');

$page->display();
