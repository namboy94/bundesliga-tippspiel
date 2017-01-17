<?php

Include "resources/strings-en.php";
Include "resources/urls.php";

function load_html($html_file) {
	$content = file_get_contents($html_file, true);
	$content = fill_string_variables($content);
	return $content;
}

function load_header($title) {

	$css = '<link rel="stylesheet" href="' . get_css_theme_file() . '">';

	$content = load_html("templates/header.html");
	$content = str_replace("@TITLE", $title, $content);
	$content = str_replace("@CSS_THEME", $css, $content);

	return $content;
}

function get_css_theme_file() {

	if ($_SESSION['theme'] === "placeholder") {
		return "";
	} 
	else {
		return "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/" .
		       "css/bootstrap.min.css";
	}
}

function initialize_session() {

	if (!isset($_SESSION['theme'])) {
			session_start();
			$_SESSION['theme'] = "default";
			$_SESSION['language'] = "en";
	}
}

function load_navbar($page_name) {

	$page_file = ($page_name == "home" ? "index.php" : $page_name . ".php");

	$home_selected = ($page_name === "home" ? 'class="active"' : "");
	$about_selected = ($page_name === "about" ? 'class="active"' : "");
	$contact_selected = ($page_name === "contact" ? 'class="active"' : "");

	$content = load_html("templates/navbar.html");
	$content = str_replace("@HOME_SELECTED", $home_selected, $content);
	$content = str_replace("@ABOUT_SELECTED", $about_selected, $content);
	$content = str_replace("@CONTACT_SELECTED", $contact_selected, $content);

	$theme = $_SESSION['theme'];

	$default_selected = ($theme === 'default' ? 'class="active"' : "");
	$default_link = $page_file . "?theme=default";

	$content = str_replace("@DEFAULT_T_SELECTED", $default_selected, $content);
	$content = str_replace("@DEFAULT_T_LINK", $default_link, $content);

	return $content;

}

function fill_string_variables($content) {

	$urls = get_url_map();

	if ($_SESSION['language'] === "de") {
		$dictionary = array();
	}
	else {
		$dictionary = get_english_dictionary();
	}

	$content = fill_strings($content, $dictionary);
	$content = fill_strings($content, $urls);

	return $content;

}

function fill_strings($content, $dictionary) {

	foreach (array_keys($dictionary) as $key) {
		echo $key;
		$content = str_replace($key, $dictionary[$key], $content);
	}
	return $content;

}




?>