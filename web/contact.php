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
include_once 'strings/dictionary.php';
include_once 'templates/header.php';
include_once 'templates/navbar.php';

initializeSession();
processGlobalGets();
$dictionary = new Dictionary($_SESSION['language']);

(new Header('@$CONTACT_TITLE'))->echo();
echo '<body>';
generateDefaultHeaderNavbar('contact.php')->echo();

?>
<div class="container">
	<div class="jumbotron text-center">
		<h1><?php echo $dictionary->translate('@$CONTACT_JUMBO') ?></h1>
	</div>
	<div class="row">
		<div class="col-sm-6 col-md-6 col-lg-6 text-center">
			<h2><?php echo $dictionary->translate('@$ADMIN_SECTION_TITLE') ?></h2>
			<h3><a href="mailto:hermann@krumreyh.com">hermann@krumreyh.com</a></h3>
		</div>
		<div class="col-sm-6 col-md-6 col-lg-6 text-center">
			<h2><?php echo $dictionary->translate('@$SOURCE_CODE_SECTION_TITLE') ?></h2>
			<h3><a href="https://gitlab.namibsun.net/namboy94/bundesliga-tippspiel">Gitlab</a></h3>
		</div>
	</div>
</div>
<?php

generateFooter('contact.php')->echoWithContainer();
echo '</body>';
