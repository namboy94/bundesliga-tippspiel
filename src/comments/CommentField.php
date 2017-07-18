<?php
/**
 * Copyright Hermann Krumrey <hermann@krumreyh.com> 2017
 *
 * This file is part of bundesliga_tippspiel.
 *
 * bundesliga_tippspiel is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * bundesliga_tippspiel is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with bundesliga_tippspiel. If not, see <http://www.gnu.org/licenses/>.
 */

namespace bundesliga_tippspiel_comments;

use chameleon\Dictionary;
use chameleon\HtmlTemplate;
use welwitschi\User;


/**
 * Class CommentField
 * A single Comment field in the Comment Bar
 * @package bundesliga_tippspiel_comments
 */
class CommentField extends HtmlTemplate {

	/**
	 * CommentField constructor.
	 * @param Dictionary|null $dictionary: The dictionary to use
	 * @param User $user: The user that is associated with this comment
	 * @param Comment $comment: The comment to display
	 */
	public function __construct(
		? Dictionary $dictionary, User $user, Comment $comment
	) {

		$this->bindParams([
			"USERNAME" => $user->username,
			"CONTENT" => $comment->content,
			"TIMESTAMP" => date('Y-m-d:h-i-s', $comment->timestamp),
			"ID" => (string)$comment->id
		]);

		// Check which template to use
		$template = __DIR__ . "/template/comment" .
			(($user->id === $comment->user->id) ? "_editable" : "") . ".html";

		parent::__construct($template, $dictionary);
	}

}