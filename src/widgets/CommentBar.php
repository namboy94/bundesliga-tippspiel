<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/18/17
 * Time: 4:39 PM
 */

namespace bundesliga_tippspiel;
use chameleon\Dictionary;
use chameleon\HtmlTemplate;

class CommentBar extends HtmlTemplate {

	public function __construct(? Dictionary $dictionary)
	{
		parent::__construct(__DIR__ . "/templates/comment_bar.html", $dictionary);
	}

}