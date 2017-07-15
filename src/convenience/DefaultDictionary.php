<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/15/17
 * Time: 11:43 AM
 */

namespace bundesliga_tippspiel;
use chameleon\Dictionary;


class DefaultDictionary extends Dictionary {

	public function __construct() {
		parent::__construct(__DIR__ . "/../resources/translations");
	}

}