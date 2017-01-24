<?php
/*  Copyright Hermann Krumrey <hermann@krumreyh.com> 2017

    This file is part of bundesliga-tippspiel.

    bundesliga-tippspiel is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    bundesliga-tippspiel is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
*/

include_once dirname(__FILE__) . '/generator.php';
include_once dirname(__FILE__) . '/../strings/dictionary.php';

/**
 * Class NavBar is a class that models a Navbar with custom elements
 */
class NavBar extends HtmlGenerator {

    /**
     * @var string: The Title of the Navbar, displayed on the Left side
     */
    private $title;

    /**
     * @var string: The link to which the title button leads to
     */
    private $title_link;

    /**
     * @var array: An Array of NavBarButtons or NavBarDropDowns to be displayed on the left side of the navbar
     */
    private $left_elements;

    /**
     * @var array: An Array of NavBarButtons or NavBarDropDowns to be displayed on the rigth side of the navbar
     */
    private $right_elements;

    /**
     * NavBar constructor.
     * UI elements can be either NavBarButtons or NavBarDropDowns
     * @param $title           string: the Navbar Title displayed on the Left side of the Navbar
     * @param $title_link      string: The Navbar Title button's destination link
     * @param $left_elements   array:  the UI elements on the left side of the navbar
     * @param $right_elements  array:  the UI elements on the right side of the button
     */
    public function __construct($title, $title_link, $left_elements, $right_elements) {
        $this->title = $title;
        $this->title_link = $title_link;
        $this->left_elements = $left_elements;
        $this->right_elements=$right_elements;
        $this->template = dirname(__FILE__) . '/html/navbar.html';
    }

    /**
     * Adds a UI element to the left side of the Navbar
     * @param $element: The element to add.
     */
    public function addLeft($element) {
        array_push($this->left_elements, $element);
    }

    /**
     * Adds a UI element to the right side of the Navbar
     * @param $element: The element to add.
     */
    public function addRight($element) {
        array_push($this->right_elements, $element);
    }

    /**
     * Renders the HTML for the Navbar UI Element
     * @return           string:  The generated HTML string
     */
    public function render() {
        $html = file_get_contents($this->template);

        $html = str_replace('@NAVBAR_TITLE', $this->title, $html);
        $html = str_replace('@NAVBAR_LINK', $this->title_link, $html);

        $left = '';
        foreach($this->left_elements as $element) {
            $left .= $element->render();
        }

        $right = '';
        foreach($this->right_elements as $element) {
            $right .= $element->render();
        }

        $html = str_replace('@LEFT', $left, $html);
        $html = str_replace('@RIGHT', $right, $html);

        return $html;

    }

    /**
     * Renders the HTML content of the Navbar, but with a container div wrapped around it
     * @return string: The rendered HTML
     */
    public function renderWithContainer() {
        return '<div class="container">' . $this->render() . '</div>';
    }

    /**
     * Directly prints the HTML content with a container wrapped around it.
     * @return void
     */
    public function echoWithContainer() {
        $dictionary = new Dictionary($_SESSION['language']);
        echo $dictionary->translate($this->renderWithContainer());
    }
}


/**
 * Class NavBarButton is a class that models a simple button on a Navbar
 */
class NavBarButton extends HtmlGenerator {

    /**
     * @var string: The title to be displayed on the button
     */
    private $name;

    /**
     * @var string: The URL to which the button will link to
     */
    private $link;

    /**
     * @var boolean: True if the button is currently selected
     */
    private $selected;

    /**
     * NavBarButton constructor.
     * @param $name     string:  The Button title
     * @param $link     string:  The Button URL
     * @param $selected boolean: The selection status of the button
     */
    public function __construct($name, $link, $selected) {
        $this->name = $name;
        $this->link = $link;
        $this->selected = $selected;
        $this->template = dirname(__FILE__) . '/html/navbar_button.html';
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {

        $active = ($this->selected ? 'class="active"' : '');

        $html = file_get_contents($this->template);
        $html = str_replace('@SELECTED', $active, $html);
        $html = str_replace('@TITLE', $this->name, $html);
        $html = str_replace('@URL', $this->link, $html);

        return $html;
    }
}

/**
 * Class NavBarDropDown is a class that models a dropdown menu in a Navbar
 */
class NavBarDropDown extends HtmlGenerator {

    /**
     * @var string: The title of the Dropdown Menu
     */
    private $title;

    /**
     * @var array: An array of NavBarButtons to be displayed in the menu
     */
    private $entries;

    /**
     * NavBarDropDown constructor.
     * @param $title   string: The title of the Dropdown Menu
     * @param $entries string: The entries to be displayed
     */
    public function __construct($title, $entries) {
        $this->title = $title;
        $this->entries = $entries;
        $this->template = dirname(__FILE__) . '/html/navbar_dropdown.html';
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public function render() {
        $html = file_get_contents($this->template);
        $html = str_replace('@TITLE', $this->title, $html);

        $entries_html = '';
        foreach($this->entries as $entry) {
            $entries_html .= $entry->render();
        }

        return str_replace('@ENTRIES', $entries_html, $html);

    }
}

/**
 * Generates the default header Navbar
 * @param $page_file string: The page calling this method
 * @return           NavBar: The generated Navbar
 */
function generateDefaultHeaderNavbar($page_file) {

    $home_active = $page_file === 'index.php';
    $login_active = $page_file === 'signup.php';
    $bets_active = $page_file === 'bets.php';
    $default_theme_active = $_SESSION['theme'] === 'default';
    $terminal_theme_active = $_SESSION['theme'] === 'terminal';
    $english_active = $_SESSION['language'] === 'en';
    $german_active = $_SESSION['language'] === 'de';

    $navbar = new NavBar('@$WEBSITE_NAME', 'index.php',
        array(
            new NavBarButton('@$HOME_NAV_TITLE', 'index.php', $home_active)
        ),
        array(
            new NavBarDropDown('@$THEMES_NAV_TITLE', array(
                new NavBarButton('@$THEME_DEFAULT_NAV_TITLE', $page_file . '?theme=default', $default_theme_active),
                new NavBarButton('@$THEME_TERMINAL_NAV_TITLE', $page_file . '?theme=terminal', $terminal_theme_active)
            )),
            new NavBarDropDown('@$LANGUAGES_NAV_TITLE', array(
                new NavBarButton('@$LANGUAGE_GERMAN_NAV_TITLE', $page_file . '?language=de', $german_active),
                new NavBarButton('@$LANGUAGE_ENGLISH_NAV_TITLE', $page_file . '?language=en', $english_active)
            ))
        )
    );

    if (isset($_SESSION['token'])) {
        $navbar->addRight(new NavBarButton('@$LOGOUT_NAV_TITLE', 'actions/logout.php', false));
        $navbar->addLeft(new NavBarButton('@$BETS_NAV_TITLE', 'bets.php', $bets_active));
    }
    else {
        $navbar->addLeft(new NavBarButton('@$LOGIN_NAV_TITLE', 'signup.php', $login_active));
    }

    return $navbar;

}

/**
 * Generated the site-wide footer navbar
 * @param $page_file string: The page calling this method
 * @return           NavBar: The generated Navbar
 */
function generateFooter($page_file) {

    $contact_page_active = $page_file === 'contact.php';

    $navbar = new NavBar('@$FOOTER_IMPRESSUM_TITLE', 'about.php',
        array(new NavBarButton('@$FOOTER_COPYRIGHT_TEXT', 'contact.php', $contact_page_active)),
        array(new NavBarButton('@$FOOTER_VERSION_TEXT',
            'https://gitlab.namibsun.net/namboy94/bundesliga-tippspiel', false))
    );
    $navbar->changeTemplateFile(dirname(__FILE__) . '/html/navbar_bottom.html');
    return $navbar;
}