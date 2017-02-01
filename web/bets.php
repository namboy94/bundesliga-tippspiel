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
include_once 'php/matchdb.php';
include_once 'templates/form.php';
include_once 'templates/navbar.php';
include_once 'templates/header.php';
include_once 'templates/betform.php';
include_once 'strings/dictionary.php';
include_once 'templates/title_jumbotron.php';

initializeSession();
redirectInvalidUser();
processGlobalGets();
$dictionary = new Dictionary($_SESSION['language']);

(new Header('@$BETS_TITLE'))->echo();
echo '<body>';

generateDefaultHeaderNavbar('bets.php')->echo();
(new TitleJumboTron('@$BETS_JUMBO'))->echo();
processDismissableMessages();

$matchday = getCurrentMatches();
$teams = getTeams();
$betform = new BetForm();

?>
<div class="container">
    <div class="row">
        <div class="col-sm-12 col-md-12 col-lg-12">
            <?php $betform->echo(); ?>
        </div>
    </div>
</div>
<?php

generateFooter('bets.php')->echoWithContainer();

echo '</body>';