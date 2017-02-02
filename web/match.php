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
include_once 'templates/navbar.php';
include_once 'templates/header.php';
include_once 'templates/betform.php';
include_once 'strings/dictionary.php';
include_once 'templates/match_jumbo.php';
include_once 'templates/title_jumbotron.php';
include_once 'templates/dismissable_message.php';

initializeSession();
processGlobalGets();
$dictionary = new Dictionary($_SESSION['language']);

$match = null;
if (isset($_GET['match_id'])) {
    $match = getMatch($_GET['match_id']);
}
if ($match === null) {
    (new DismissableMessage('error', '@$MATCH_NOT_FOUND_ERROR_TITLE', '@$MATCH_NOT_FOUND_ERROR_BODY'))
        ->show('index.php');
}
$teams = getTeamsForMatch($match);

(new Header('@$MATCH_TITLE'))->echo();

echo '<body>';
generateDefaultHeaderNavbar('match.php')->echo();

(new MatchJumbo($match, $teams['team_one'], $teams['team_two']))->echo();
processDismissableMessages();

$team_one_logo = 'resources/images/logos/' . $teams['team_one']['id'] . '.gif';
$team_two_logo = 'resources/images/logos/' . $teams['team_two']['id'] . '.gif';

?>
<div class="row">
    <div class="col-sm-3"><img class="center-block" src="<?php echo $team_one_logo?>"></div>
    <div class="col-sm-6">
        <div class="jumbotron">
            <div class="row">
                <div class="col-sm-2"></div>
                <div class="col-sm-2"><h1><?php echo $match['team_one_ft']?></h1></div>
                <div class="col-sm-4"></div>
                <div class="col-sm-2"><h1><?php echo $match['team_two_ft']?></h1></div>
                <div class="col-sm-2"></div>
            </div>
        </div>
    </div>
    <div class="col-sm-3"><img class="center-block" src="<?php echo $team_two_logo?>"></div>
</div>
<?php

generateFooter('password_reset.php')->echoWithContainer();
echo '</body>';
