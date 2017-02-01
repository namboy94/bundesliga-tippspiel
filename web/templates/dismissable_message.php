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
 * Class DismissableMessage is a class that models a dismissable Message
 */
class DismissableMessage extends HtmlGenerator {

    /**
     * @var string: The type of message. Can be 'error', 'success', 'warning' and 'info'
     */
    private $message_type;

    /**
     * @var string: The title of the message.
     */
    private $title;

    /**
     * @var string: The body of the message.
     */
    private $body;

    /**
     * DismissableMessage constructor.
     * @param $message_type string: The type of message
     * @param $title        string: The title of the message
     * @param $body         string: The body of the message
     */
    public function __construct($message_type, $title, $body) {
        $this->message_type = $message_type;
        $this->title = $title;
        $this->body = $body;
    }

    /**
     * Parses the message type to the correct CSS class
     * @return string The correct class type
     */
    private function parseMessageType() {
        $types = array(
            'error' => 'alert-danger',
            'success' => 'alert-success',
            'info' => 'alert-info',
            'warning' => 'alert-warning'
        );
        return $types[$this->message_type];
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = file_get_contents(dirname(__FILE__) . '/html/dismissable_message.html');
        $html = str_replace('@TYPE', $this->parseMessageType(), $html);
        $html = str_replace('@TITLE', $this->title, $html);
        $html = str_replace('@BODY', $this->body, $html);
        return $html;
    }

    /**
     * Turns this message into an array to be able to store in session
     * @return array: The resulting array
     */
    public function toArray() {
        return array($this->message_type, $this->title, $this->body);
    }

    /**
     * Creates a new DismissableMessage from an array of values
     * @param $values array:       The values to use
     * @return DismissableMessage: The generated DismissableMessage object
     */
    public static function fromArray($values) {
        return new DismissableMessage($values[0], $values[1], $values[2]);
    }

    /**
     * Redirects to the specified target and stores itself in the session to be displayed
     * @param $target
     */
    public function show($target) {
        $_SESSION[$this->message_type] = $this->toArray();
        header('Location: ' . $target);
        exit();
    }
}
