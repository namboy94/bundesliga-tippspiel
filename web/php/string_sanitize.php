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

/**
* Formats the content of a comment to avoid XSS vulnerabilities, but allows certain formatting tags
* @param $content string: The content of the comment
* @return         string: The formatted content
*/
function sanitizeComment($content) {

    foreach(colors() as $color) {
        $content = str_replace('@' . strtoupper($color), '@' . strtolower($color), $content);
        $content = str_replace('<' . strtolower($color) . '>', '@' . strtoupper($color), $content);
    }
    $content = htmlspecialchars($content);
    return $content;
}

/**
 * Renders a comment
 * @param $content string: The comment content
 * @return         string: The rendered comment
 */
function renderComment($content) {
    $content = preg_replace('#&lt;(/?(?:small|strong|i|b))&gt;#', '<\1>', $content);
    foreach(colors() as $color) {
        $content = str_replace('@' . strtolower($color), '@' . strtoupper($color), $content);
        $content = str_replace('@' . strtoupper($color), '<span style="color:' . strtolower($color) . '; ">', $content);
    }
    return $content;
}

/**
 * @return array: Defines the colors that are available for custom formatting
 */
function colors() {
    return array('red', 'blue', 'yellow', 'green', 'white');
}