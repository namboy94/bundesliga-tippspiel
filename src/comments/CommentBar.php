<?php
/**
 * Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>
 *
 * This file is part of bundesliga-tippspiel.
 *
 * bundesliga-tippspiel is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * bundesliga-tippspiel is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with bundesliga-tippspiel. If not, see <http://www.gnu.org/licenses/>.
 */

namespace bundesliga_tippspiel_comments;
use bundesliga_tippspiel\Functions;
use chameleon\Dictionary;
use chameleon\HtmlTemplate;
use welwitschi\User;


/**
 * Class CommentBar
 * The Sidebar displaying the comments
 * @package bundesliga_tippspiel_comments
 */
class CommentBar extends HtmlTemplate {

	/**
	 * @var string: The content ID which acts as a key in the $_POST variable
	 */
	public static $contentId = "comment_content";

	/**
	 * CommentBar constructor.
	 * @param Dictionary|null $dictionary: Dictionary used to translate
	 * @param User $activeUser: The user that requsted the page
	 */
	public function __construct(
		? Dictionary $dictionary, User $activeUser
	) {

		parent::__construct(
			__DIR__ . "/templates/comment_bar.html", $dictionary
		);

		$db = Functions::getMysqli();
		$commentManager = new CommentManager($db);
		$comments = $commentManager->getComments();

		$commentFields = [];
		foreach ($comments as $comment) {
			array_push(
				$commentFields,
				new CommentField($dictionary, $activeUser, $comment)
			);
		}

		$this->addCollectionFromArray("COMMENTS", $commentFields);
		$this->bindParam("CONTENT_ID", self::$contentId);
	}

}