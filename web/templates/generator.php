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

include_once dirname(__FILE__) . '/../strings/dictionary.php';

/**
 * Class HtmlGenerator is a common interface for HTML generators to enable a developer
 * to expect some sort of default behaviour for all template generators
 */
abstract class HtmlGenerator {

    /**
     * @var string: The HTML template file to be used when generating the content
     */
    protected $template;

    /**
     * Changes the HTML template file to be used
     * @param $template string: The new template file
     * @return          void
     */
    public function changeTemplateFile($template) {
        $this->template = $template;
    }

    /**
     * Directly prints the rendered HTML content
     * @return void
     */
    public function echo() {
        $dictionary = new Dictionary($_SESSION['language']);
        echo $dictionary->translate($this->render());
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public abstract function render();

}