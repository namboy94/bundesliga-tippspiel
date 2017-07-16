<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/15/17
 * Time: 11:41 AM
 */

namespace bundesliga_tippspiel;
use chameleon\BootstrapScript;
use chameleon\BootstrapStyleSheet;
use chameleon\GoogleAnalyticsScript;
use chameleon\Header;
use chameleon\ReCaptchaScript;
use chameleon\Stylesheet;


/**
 * Class DefaultHeader
 * The Header displayed in the <head> section of pretty much every page
 * @package bundesliga_tippspiel
 */
class DefaultHeader extends Header {

	/**
	 * DefaultHeader constructor.
	 * @param string $title: The title of the page
	 * @param bool $useRecaptcha: Can be set to true to enable Recaptcha
	 */
	public function __construct(string $title, bool $useRecaptcha = false) {

		$scripts = [
			new BootstrapScript(),
			new GoogleAnalyticsScript("UA-77243880-6"),
			new BootstrapStyleSheet()
		];

		$styleSheets = [
			new BootstrapStyleSheet(),
			new Stylesheet("css/custom.css")
		];

		if ($useRecaptcha) {
			array_push($scripts, new ReCaptchaScript());
		}

		parent::__construct(
			new DefaultDictionary(),
			$title,
			"resources/images/favicon.png",
			$scripts,
			$styleSheets
		);
	}
}