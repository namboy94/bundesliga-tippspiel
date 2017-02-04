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
include_once 'php/matchdb.php';
include_once 'templates/dismissable_message.php';

$match = null;
$score = null;
if (isset($_GET['match_id'])) {
    $match = getMatch($_GET['match_id']);
    $score = getCurrentScore($_GET['match_id']);
}
if ($match === null || $score == null) {
    (new DismissableMessage('error', '@$MATCH_NOT_FOUND_ERROR_TITLE', '@$MATCH_NOT_FOUND_ERROR_BODY'))
        ->show('index.php');
}

$teams = getTeamsForMatch($match);
$title = $teams['team_one']['name'] . ' vs. ' . $teams['team_two']['name'];
$team_one_logo = 'resources/images/logos/' . $teams['team_one']['id'] . '.gif';
$team_two_logo = 'resources/images/logos/' . $teams['team_two']['id'] . '.gif';

$page = new Page($title, 'match.php', $title, array(), false);

$page->addStringBodyElement('<div class="row">');
$page->addStringBodyElement('<div class="col-sm-3"><img class="center-block" src="' . $team_one_logo . '"></div>');

$page->addStringBodyElement('<div class="col-sm-6"><div class="jumbotron"><div class="row">');
$page->addStringBodyElement('<div class="col-sm-2"></div>');
$page->addStringBodyElement('<div class="col-sm-2"><h1>' . $score['team_one_score'] . '</h1></div>');
$page->addStringBodyElement('<div class="col-sm-4"></div>');
$page->addStringBodyElement('<div class="col-sm-2"><h1>' . $score['team_two_score'] . '</h1></div>');
$page->addStringBodyElement('<div class="col-sm-2"></div></div></div></div>');

$page->addStringBodyElement('<div class="col-sm-3"><img class="center-block" src="' . $team_two_logo . '"></div>');
$page->addStringBodyElement('</div>');

$page->display();
