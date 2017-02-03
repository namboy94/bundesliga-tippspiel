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

include_once dirname(__FILE__) . '/generator.php';

/**
 * Class TitleJumboTron is class that models the title jumbotron of a page
 */
class TitleJumboTron extends HtmlGenerator {

    /**
     * @var string: The title of the jumbotron
     */
    private $title;

    /**
     * TitleJumboTron constructor.
     * @param $title: The jumbotron's title
     */
    public function __construct($title) {
        $this->title = $title;
        $this->template = dirname(__file__) . '/html/title_jumbotron.html';
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = $this->loadTemplate();
        return str_replace('@TITLE', $this->title, $html);
    }
}