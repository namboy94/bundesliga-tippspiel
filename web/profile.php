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

$page = new Page('@$PROFILE_TITLE', 'profile.php', '@$PROFILE_JUMBO', array(), true);

$reset_form = new Form('@$PROFILE_PASSWORD_CHANGE_TITLE', 'actions/password_change.php',
    array(
        new FormTextEntry('@$PROFILE_PASSWORD_CHANGE_CURRENT_LABEL',
            'current', 'password', '********', 'current'),
        new FormTextEntry('@$PROFILE_PASSWORD_CHANGE_NEW_LABEL',
            'new', 'password', '********', 'new'),
        new FormTextEntry('@$PROFILE_PASSWORD_RESET_CHANGE_REPEAT_LABEL',
            'repeat', 'password', '********', 'repeat'),
        new ConfirmationButton('@$PROFILE_PASSWORD_CHANGE_SUBMIT')
    )
);

$rename_form = new Form('@$PROFILE_USERNAME_CHANGE_TITLE', 'actions/username_change.php',
    array(
        new FormTextEntry('@$PROFILE_NEW_USERNAME_LABEL',
            'new name', 'text', '********', 'new_name'),
        new ConfirmationButton('@$PROFILE_USERNAME_CHANGE_SUBMIT')
    )
);

$page->addStringBodyElement('<div class="row"><div class="col-lg-1"></div><div class="col-lg-4">');
$page->addGeneratorBodyElement($reset_form);
$page->addStringBodyElement('</div><div class="col-lg-2"></div><div class="col-lg-4">');
$page->addGeneratorBodyElement($rename_form);
$page->addStringBodyElement('</div><div class="col-lg-1"></div></div>');

echo str_replace('@$PROFILE_JUMBO', $_SESSION['userdata']['name'], $page->display(false));
