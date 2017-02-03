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
$page = new Page('@$ABOUT_TITLE', 'about.php', '@$ABOUT_JUMBO', array(), false);

$about_content = file_get_contents('resources/text/impressum.' . $_SESSION['language']);
$content_layout_start = '<div class="container"><div class="row"><div class="col-sm-10">';
$content_layout_end = '</div></div></div>';

$page->addStringBodyElement($content_layout_start . $about_content . $content_layout_end);

$page->display();
