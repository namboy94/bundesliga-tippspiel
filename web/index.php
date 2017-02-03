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
include_once 'php/session.php';
include_once 'templates/form.php';
include_once 'templates/betform.php';

$page = new Page('@$HOME_TITLE', 'index.php', '@$HOME_JUMBO', array(), false);

$page->addStringBodyElement('<div class="container">');
$page->addStringBodyElement('<div class="row">');
$page->addStringBodyElement('<div class="col-sm-' . ($page->logged_in ? '6' : '8') . ' text-center">' .
                            '@$HOME_WELCOME_TEXT</div>');
$page->addStringBodyElement('<div class="col-sm-' . ($page->logged_in ? '6' : '4') . ' text-center">');

if ($page->logged_in) {
    $page->addGeneratorBodyElement(new BetForm(-1, true));
}
else {
    $page->addGeneratorBodyElement(generateLoginForm());
    $page->addStringBodyElement('<h5>@$OR_SIGN_UP_TEXT</h5>');
}

$page->addStringBodyElement('</div></div></div>');

$page->display();
