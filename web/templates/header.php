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

class Header extends HtmlGenerator {

    /**
     * @var string: The title of the header
     */
    private $title;

    /**
     * Header constructor.
     * @param $title string: The title of the header
     */
    public function __construct($title) {
        $this->title = $title;
        $this->template = dirname(__FILE__) . '/html/header.html';
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = $this->loadTemplate();
        $html = str_replace('@TITLE', $this->title, $html);
        $html = str_replace('@CSS_THEME', $this->determineCssFile()[0], $html);
        $html = str_replace('@CUSTOM_CSS_THEME', $this->determineCssFile()[1], $html);

        return $html;
    }

    /**
     * @return array: a tuple of css files according to the current theme
     */
    private function determineCssFile() {

        $css_files = array(
            'default' => array(
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                'css/custom-default.css'
            ),
            'terminal' => array('css/hacker.css', 'css/custom-hacker.css')
        );

        return $css_files[$_SESSION['theme']];

    }
}