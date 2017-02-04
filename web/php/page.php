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

include_once dirname(__FILE__) . '/gets.php';
include_once dirname(__FILE__) . '/session.php';
include_once dirname(__FILE__) . '/../strings/dictionary.php';
include_once dirname(__FILE__) . '/../templates/navbar.php';
include_once dirname(__FILE__) . '/../templates/header.php';
include_once dirname(__FILE__) . '/../templates/title_jumbotron.php';
include_once dirname(__FILE__) . '/../templates/comment_sidebar.php';

/**
 * Class Page is a class that offers a unified framework of sorts to display an HTML page using strings
 * an HtmlGenerator objects
 */
class Page {

    /**
     * @var Header: The header object generated for this page
     */
    private $header;

    /**
     * @var array: The string elements in the body of the page
     */
    private $body;

    /**
     * @var NavBar: The footer Navbar at the bottom of the page
     */
    private $footer;

    /**
     * @var Dictionary: The currently used dictionary for string replacements
     */
    public $dictionary;

    /**
     * @var bool: State variable that is set to true whenever the user is logged in
     */
    public $logged_in;

    /**
     * Page constructor.
     * @param $title          string:  The title of the page
     * @param $filename       string:  The page's filename
     * @param $jumbo_title    string:  The jumbotron title
     * @param $body_elements  array:   The initial body elements of the page
     * @param $login_required boolean: Can be set to true to redirct non-authenticated users to index.php
     */
    public function __construct($title, $filename, $jumbo_title, $body_elements, $login_required=false) {

        initializeSession();
        processGlobalGets();
        $this->dictionary = new Dictionary();
        $this->logged_in = isLoggedIn();

        if ($login_required) {
            redirectInvalidUser();
        }

        $this->header = new Header($title);
        $this->body = array('<body>',
                            generateDefaultHeaderNavbar($filename)->renderHtml(),
                            (new TitleJumboTron($jumbo_title))->renderHtml(),
                            '<div class="row">');

        if ($this->logged_in) {
            $this->addStringBodyElement('<div class="col-sm-3 comments">');
            $this->addGeneratorBodyElement(new CommentSidebar());
            $this->addStringBodyElement('</div><div class="col-sm-9">');
        }
        else {
            $this->addStringBodyElement('<div class="col-sm-12">');
        }
        $this->addStringBodyElement(processDismissableMessages());

        foreach ($body_elements as $body_element) {
            array_push($this->body, $body_element->renderHtml());
        }
        $this->footer = generateFooter($filename);
    }

    /**
     * Adds a HtmlGenerator to the body
     * @param $element  HtmlGenerator: The generator object to add
     * @param $position int:           Can be specified to but the element at a specific position
     */
    public function addGeneratorBodyElement($element, $position=null) {
        $this->addStringBodyElement($element->renderHtml(), $position);
    }

    /**
     * Adds a string to the body
     * @param $element  string: The string to add
     * @param $position int:    Can be specified to but the element at a specific position
     */
    public function addStringBodyElement($element, $position=null) {
        $translated = $this->dictionary->translate($element);
        if ($position === null) {
            array_push($this->body, $translated);
        }
        else {
            array_splice($this->body, $position, 0, $translated);
        }
    }

    /**
     * Displays the page
     * @param $echo boolean: Can be set to false to not echo the page
     * @return      string:  The page content HTML
     */
    public function display($echo=true) {

        $html = '';

        array_push($this->body, $this->footer->renderHtmlWithContainer());
        array_push($this->body, '</div></div>');
        array_push($this->body, '</body>');

        $this->header->echo();
        foreach ($this->body as $body_element) {
            $html .= $body_element;
        }

        if ($echo) {
            echo $html;
        }
        return $html;
    }
}
