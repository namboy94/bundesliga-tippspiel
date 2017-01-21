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

include_once dirname(__FILE__) . '/english.php';
Include_once dirname(__FILE__) . '/german.php';

/**
 * Class Dictionary is a class that handles strings in different languages
 */
class Dictionary {

    /**
     * @var array: The currently implemented dictionaries
     */
    private $dictionaries;

    /**
     * @var string: The active language of the dictionary
     */
    private $active_language;

    /**
     * Dictionary constructor.
     * @param $active_language: The active language of the dictionary
     */
    public function __construct($active_language) {

        $this->dictionaries = array(
            'en' => get_english(),
            'de' => get_german()
        );

        $this->active_language = strtolower($active_language);
    }

    /**
     * Replaces a specified keyword in a string using the correct equivalent in the selected language
     * @param $keyword     string:  The keyword to replace
     * @param $original    string:  The original string
     * @param $add_symbols boolean: Can be set to false if the keyword should be replaced raw,
     *                              and not with '@$' prepended
     * @return             string:  The string with the replacement in place
     */
    public function replace($keyword, $original, $add_symbols=true) {
        $replace_key = ($add_symbols ? '@$' . $keyword : $keyword);
        return str_replace($replace_key, $this->dictionaries[$this->active_language][$keyword], $original);
    }

    /**
     * @return array: The current dictionary map
     */
    public function getMap() {
        return $this->dictionaries[$this->active_language];
    }

    /**
     * Translates a text using the current dictionary.
     * Only Keywords starting with @$ are translated, and only if they exist in the dictionary
     * @param $text string: The text to translate
     * @return      string: The translated text
     */
    public function translate($text) {
        foreach(array_keys($this->dictionaries[$this->active_language]) as $key) {
            $keyword = '@$' . $key;
            $text = str_replace($keyword, $this->dictionaries[$this->active_language][$key], $text);
        }
        return $text;
    }

}