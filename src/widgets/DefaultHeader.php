<?php
/**
 * Created by PhpStorm.
 * User: hermann
 * Date: 7/15/17
 * Time: 11:41 AM
 */

namespace bundesliga_tippspiel;
use chameleon_widgets\BootstrapScript;
use chameleon_widgets\BootstrapStyleSheet;
use chameleon_widgets\GoogleAnalyticsScript;
use chameleon_widgets\Header;
use chameleon_widgets\ReCaptchaScript;

class DefaultHeader extends Header {

	public function __construct(string $title, bool $useCaptcha = false) {

		$scripts = [
			new BootstrapScript(),
			new GoogleAnalyticsScript("UA-77243880-6"),
			new BootstrapStyleSheet()
		];

		if ($useCaptcha) {
			array_push($scripts, new ReCaptchaScript());
		}

		parent::__construct(
			new DefaultDictionary(),
			$title, __DIR__ . "/../resources/favicon.png", $scripts,
			[new BootstrapStyleSheet()], []);

	}

}