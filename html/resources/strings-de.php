<?php

function get_german_dictionary() {

	return array(

		'@$ADMIN_CONTACT_TITLE' => 'Administrator',
		'@$SOURCE_CODE_TITLE' => "Quellcode",
		'@$HOME_TITLE' => "Bundesliga Tippspiel - HOME",
		'@$ABOUT_TITLE' => "Bundesliga Tippspiel - IMPRESSUM",
		'@$CONTACT_TITLE' => "Bundesliga Tippspiel - KONTAKT",
		'@$NAVBAR_TITLE' => "Bundesliga Tippspiel",
		'@$HOME_NAV' => "Home",
		'@$ABOUT_NAV' => "Impressum",
		'@$CONTACT_NAV' => "Kontakt",
		'@$THEMES_NAV' => "Themen",
		'@$GERMAN_LANG' => "Deutsch",
		'@$ENGLISH_LANG' => "Englisch",
		'@$DEFAULT_THEME' => "Standard",
		'@$TERMINAL_THEME' => "Terminal",
		'@$GITLAB_NAME' => "Gitlab",
		"@$ABOUT_TEXT" => file_get_contents("resources/impressum.de", true)

	);

}

?>