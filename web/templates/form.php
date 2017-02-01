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
 * Class Form is a class that models an entry form
 */
class Form extends HtmlGenerator {

    /**
     * @var string: The form's title
     */
    private $title;

    /**
     * @var string: The target .php file that handles the form's POST request
     */
    private $target;

    /**
     * @var array: An array of Form Elements, defined below this class
     */
    private $elements;

    /**
     * Form constructor.
     * @param $title    string: The title of the form
     * @param $target   string: The target PHP file
     * @param $elements array:  The array of form elements
     */
    public function __construct($title, $target, $elements) {
        $this->title = $title;
        $this->target = $target;
        $this->elements = $elements;
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = file_get_contents(dirname(__FILE__) . '/html/form.html');

        $html = str_replace('@TITLE', $this->title, $html);
        $html = str_replace('@ACTION', $this->target, $html);

        $elements = '';
        foreach($this->elements as $element) {
            $elements .= $element->render();
        }

        return str_replace('@ELEMENTS', $elements, $html);

    }
}

/**
 * Class FormTextEntry is a class that models a Form text entry
 */
class FormTextEntry extends HtmlGenerator {

    /**
     * @var string: The title of the Entry
     */
    private $title;

    /**
     * @var string: The name of the variable to be POSTed
     */
    private $name;

    /**
     * @var string: The type of entry the form is. Usual values are 'text' or 'password'
     */
    private $type;

    /**
     * @var string: A placeholder text that is displayed by default
     */
    private $placeholder;

    /**
     * @var string: The id in the HTML document
     */
    private $id;


    /**
     * FormTextEntry constructor.
     * @param $title         string: The Title
     * @param $variable_name string: The POST-variable
     * @param $type          string: The type of entry
     * @param $placeholder   string: The placeholder text
     * @param $element_id    string: The element ID
     */
    public function __construct($title, $variable_name, $type, $placeholder, $element_id) {
        $this->title = $title;
        $this->name = $variable_name;
        $this->type = $type;
        $this->placeholder = $placeholder;
        $this->id = $element_id;
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = file_get_contents(dirname(__FILE__) . '/html/form_text_entry.html');

        $html = str_replace('@TITLE', $this->title , $html);
        $html = str_replace('@NAME', $this->name, $html);
        $html = str_replace('@TYPE', $this->type, $html);
        $html = str_replace('@PLACEHOLDER', $this->placeholder, $html);
        $html = str_replace('@ID', $this->id, $html);

        return $html;
    }
}

/**
 * Class ConfirmationButton is a class that models a confirmation button
 */
class ConfirmationButton extends HtmlGenerator {

    /**
     * @var string: The text to be displayed on the button
     */
    private $text;

    public function __construct($text) {
        $this->text = $text;
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = file_get_contents(dirname(__FILE__) . '/html/form_confirm_button.html');
        $html = str_replace('@TEXT', $this->text , $html);
        return $html;
    }
}