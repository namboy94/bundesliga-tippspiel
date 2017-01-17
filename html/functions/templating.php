<?php

function load_html($html_file) {
	return file_get_contents($html_file, true);
}

function load_header($title) {

	$content = load_html("templates/header.html");
	$content = str_replace("@TITLE", $title, $content);
	$content = str_replace("@CSS_THEME", get_css_theme_file(), $content);
	return $content;
}

function get_css_theme_file() {

	if ($_SESSION['theme'] === "placeholder") {
		return "";
	} 
	else {
		return "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/
		        css/bootstrap.min.css";
	}
}

function initialize_session() {

	if (!isset($_SESSION['theme'])) {
			session_start();
			$_SESSION['theme'] = "default";
	}
}


?>