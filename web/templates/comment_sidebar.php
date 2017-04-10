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
include_once dirname(__FILE__) . '/../php/database.php';
include_once dirname(__FILE__) . '/../php/string_sanitize.php';


/**
 * Class CommentSidebar is a class that renders the comment sidebar
 */
class CommentSidebar extends HtmlGenerator {

    /**
     * CommentSidebar constructor.
     */
    public function __construct() {
        $this->template = dirname(__FILE__) . '/html/comment_sidebar.html';
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $db = new Database();
        $html = $this->loadTemplate();

        $comments = $db->query('SELECT comments.id AS comment_id, comments.content AS content,
                                comments.created AS created, comments.last_modified AS last_modified, 
                                users.username AS username, users.user_id AS user_id
                                FROM comments LEFT JOIN users ON comments.user=users.user_id WHERE users.user_id != -1
                                ORDER BY comments.created DESC LIMIT 100',
                               '', array(), true);
        $comment_html = '';

        foreach ($comments as $comment) {
            $comment_html .= (new Comment($comment))->render();
        }

        $html = str_replace('@COMMENTS', $comment_html, $html);
        return $html;
    }
}

/**
 * Class Comment is a class that models a single comment
 */
class Comment extends HtmlGenerator {

    /**
     * @var array: The comment data
     */
    private $comment;

    /**
     * CommentSidebar constructor.
     * @param $comment array: The comment data
     */
    public function __construct($comment) {

        $user_id = $_SESSION['id'];
        if ((int)$user_id === (int)$comment['user_id']) {
            $this->template = dirname(__FILE__) . '/html/user_owned_comment.html';
        }
        //elseif (is_null($comment['user_id'])) {
        //  $this->template = dirname(__FILE__) . '/html/deleted_comment.html';
        //}
        else {
            $this->template = dirname(__FILE__) . '/html/comment.html';
        }
        $this->comment = $comment;
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    protected function render() {

        $html = $this->loadTemplate();

        $html = str_replace('@CONTENT', renderComment($this->comment['content']), $html);
        $html = str_replace('@USER', $this->comment['username'], $html);
        $html = str_replace('@COMMENT_ID', $this->comment['comment_id'], $html);

        $timestamp = date('Y-m-d:h-i-s', $this->comment['last_modified']);
        if ($this->comment['last_modified'] !== $this->comment['created']) {
            $timestamp .= '*';
        }

        $html = str_replace('@DATE', $timestamp, $html);

        return $html;
    }
}