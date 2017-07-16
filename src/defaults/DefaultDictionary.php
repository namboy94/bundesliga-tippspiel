<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/15/17
 * Time: 11:43 AM
 */

namespace bundesliga_tippspiel;
use chameleon\Dictionary;


/**
 * Class DefaultDictionary
 * A Dictionary class that automatically sets the correct path to the
 * translation files
 * @package bundesliga_tippspiel
 */
class DefaultDictionary extends Dictionary {

	/**
	 * DefaultDictionary constructor.
	 */
	public function __construct() {
		parent::__construct(__DIR__ . "/../resources/translations");
	}

}