<?php

Include "resources/strings.php";
Include "resources/strings-en.php";
Include "resources/strings-de.php";
Include "resources/urls.php";


function load_html($html_file) {
	$content = file_get_contents($html_file, true);
	$content = fill_string_variables($content);
	return $content;
}

function process_global_gets() {

	if (isset($_GET['theme'])) {
		$_SESSION['theme'] = $_GET['theme'];
	}
	if (isset($_GET['language'])) {
		$_SESSION['language'] = $_GET['language'];
	}

}

function load_header($title) {

	$dictionary = get_current_dictionary();
	$page_title = $dictionary["@$" . strtoupper($title) . "_TITLE"];
	$css = '<link rel="stylesheet" href="' . get_css_theme_file() . '">';

	$content = load_html("html_content/templates/header.html");
	$content = str_replace("@TITLE", $page_title, $content);
	$content = str_replace("@CSS_THEME", $css, $content);

	return $content;
}

function get_css_theme_file() {

	if ($_SESSION['theme'] === "terminal") {
		return "css/hacker.css";
	} 
	else {
		return get_url_map()['@!DEFAULT_CSS_THEME'];
	}
}

function get_current_dictionary() {

	if ($_SESSION['language'] === "de") {
		return get_german_dictionary();
	}
	else {
		return get_english_dictionary();
	}
}

function initialize_session() {

	if (session_id() == "") {
  		session_start();
	}

	if (!array_key_exists('theme', $_SESSION) 
		|| $_SESSION['theme'] === "") {
			$_SESSION['theme'] = "default";
	}
	if (!array_key_exists('language', $_SESSION)
		|| $_SESSION['language'] === "") {
		$_SESSION['language'] = "en";
	}
}

function load_navbar($page_name) {

	$page_file = ($page_name == "home" ? "index.php" : $page_name . ".php");

	$home_selected = ($page_name === "home" ? 'class="active"' : "");

	$content = load_html("html_content/templates/navbar.html");
	$content = str_replace("@HOME_SELECTED", $home_selected, $content);

	$content = fill_navbar_element("theme", "default", $page_file, $content);
	$content = fill_navbar_element("theme", "terminal", $page_file, $content);
	$content = fill_navbar_element("language", "en", $page_file, $content);
	$content = fill_navbar_element("language", "de", $page_file, $content);

	return $content;

}

function fill_navbar_element($keyname, $keyvalue, $page_file, $content) {

	$link = $page_file . "?" . $keyname . "=" . $keyvalue;
	$active = ($keyvalue === $_SESSION[$keyname] ? 'class="active"' : "");

	$nav_link = "@NAV_LINK_" . strtoupper($keyvalue);
	$nav_active = "@NAV_ACTIVE_" . strtoupper($keyvalue);

	$content = str_replace($nav_link, $link, $content);
	$content = str_replace($nav_active, $active, $content);

	return $content;

}

function fill_string_variables($content) {

	$urls = get_url_map();
	$dictionary = get_current_dictionary();
	$strings = get_strings();

	$content = fill_strings($content, $dictionary);
	$content = fill_strings($content, $urls);
	$content = fill_strings($content, $strings);

	return $content;

}

function fill_strings($content, $dictionary) {

	foreach (array_keys($dictionary) as $key) {
		$content = str_replace($key, $dictionary[$key], $content);
	}
	return $content;

}




?>