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

$page = new Page('@$CONTACT_TITLE', 'contact.php', '@$CONTACT_JUMBO', array(), false);

$admin_title = '<h2>@$ADMIN_SECTION_TITLE</h2>';
$admin_email = '<h3><a href="mailto:hermann@krumreyh.com">hermann@krumreyh.com</a></h3>';
$gitlab_title = '<h2>@$SOURCE_CODE_SECTION_TITLE</h2>';
$gitlab_url = '<h3><a href="https://gitlab.namibsun.net/namboy94/bundesliga-tippspiel">Gitlab</a></h3>';

$page->addStringBodyElement('<div class="container"><div class="row"><div class="col-sm-1"></div>');
$page->addStringBodyElement('<div class="col-sm-4">' . $admin_title . $admin_email . '</div>');
$page->addStringBodyElement('<div class="col-sm-2"></div>');
$page->addStringBodyElement('<div class="col-sm-4">' .$gitlab_title . $gitlab_url . '</div>');
$page->addStringBodyElement('<div class="col-sm-1"></div></div></div>');

$page->display();
