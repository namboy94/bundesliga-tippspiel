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

class Page {

    private $header;
    private $body;
    private $footer;
    public $dictionary;

    public function __construct($title, $filename, $jumbo_title, $body_elements, $login_required=false) {

        initializeSession();
        processGlobalGets();
        $this->dictionary = new Dictionary();

        if ($login_required) {
            redirectInvalidUser();
        }

        $this->header = new Header($title);
        $this->body = array('<body>',
                            generateDefaultHeaderNavbar($filename)->renderHtml(),
                            (new TitleJumboTron($jumbo_title))->renderHtml(),
                            processDismissableMessages()
                            //(new CommentSidebar())->renderHtml(),
                            //'<div id="wrapper">',
                            //'<div id="page-content-wrapper">'
                            );

        foreach ($body_elements as $body_element) {
            array_push($this->body, $body_element->renderHtml());
        }
        $this->footer = generateFooter($filename)->renderHtmlWithContainer();
    }

    public function addGeneratorBodyElement($element, $position=null) {
        $this->addStringBodyElement($element->renderHtml(), $position);
    }

    public function addStringBodyElement($element, $position=null) {
        if ($position === null) {
            array_push($this->body, $element);
        }
        else {
            array_splice($this->body, $position, 0, $element);
        }

    }

    public function display() {

        array_push($this->body, $this->footer);
        array_push($this->body, '</div>');
        array_push($this->body, '</body>');

        $this->header->echo();
        foreach ($this->body as $body_element) {
            echo $body_element;
        }
    }

}
