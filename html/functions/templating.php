<?php

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

	$content = load_html("templates/header.html");
	$content = str_replace("@TITLE", $page_title, $content);
	$content = str_replace("@CSS_THEME", $css, $content);

	return $content;
}

function get_css_theme_file() {

	if ($_SESSION['theme'] === "clean_blog") {
		return "css/clean-blog.css";
	} 
	else {
		return "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/" .
		       "css/bootstrap.min.css";
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

	if (!array_key_exists('theme', $_SESSION['theme'])) {
			$_SESSION['theme'] = "default";
	}
	if (!array_key_exists('language', $_SESSION)) {
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
	$language = $_SESSION['language'];

	$default_sel = ($theme === 'default' ? 'class="active"' : "");
	$default_link = $page_file . "?theme=default";
	$content = str_replace("@DEFAULT_THEME_NAV", $default_link, $content);
	$content = str_replace("@DEFAULT_THEME_SELECTED", $default_sel, $content);

	$cleanb_sel = ($theme === 'clean_blog' ? 'class="active"' : "");
	$cleanb_link = $page_file . "?theme=clean_blog";
	$content = str_replace("@CLEANB_THEME_NAV", $cleanb_link, $content);
	$content = str_replace("@CLEANB_THEME_SELECTED", $cleanb_sel, $content);

	$german_selected = ($language === 'de' ? 'class="active"' : "");
	$german_link = $page_file . "?language=de";
	$content = str_replace("@NAV_GERMAN_LINK", $german_link, $content);
	$content = str_replace("@NAV_GERMAN_SELECT", $german_selected, $content);

	$english_selected = ($language === 'en' ? 'class="active"' : "");
	$english_link = $page_file . "?language=en";
	$content = str_replace("@NAV_ENGLISH_LINK", $english_link, $content);
	$content = str_replace("@NAV_ENGLISH_SELECT", $english_selected, $content);

	return $content;

}

function fill_string_variables($content) {

	$urls = get_url_map();
	$dictionary = get_current_dictionary();

	$content = fill_strings($content, $dictionary);
	$content = fill_strings($content, $urls);

	return $content;

}

function fill_strings($content, $dictionary) {

	foreach (array_keys($dictionary) as $key) {
		$content = str_replace($key, $dictionary[$key], $content);
	}
	return $content;

}




?>