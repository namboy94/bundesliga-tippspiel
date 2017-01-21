<?php
/**
 * Copyright Hermann Krumrey<hermann@krumreyh.com> 2017
 */

/**
 * Class NavBar is a class that models a Navbar with custom elements
 */
class NavBar extends HtmlGenerator {

    /**
     * @var string The Title of the Navbar, displayed on the Left side
     */
    private $title;

    /**
     * @var array An Array of NavBarButtons or NavBarDropDowns to be displayed on the left side of the navbar
     */
    private $left_elements;

    /**
     * @var array An Array of NavBarButtons or NavBarDropDowns to be displayed on the rigth side of the navbar
     */
    private $right_elements;

    /**
     * @var string The template file used to generate the HTML content
     */
    private $template;

    /**
     * NavBar constructor.
     * UI elements can be either NavBarButtons or NavBarDropDowns
     * @param $title           string: the Navbar Title displayed on the Left side of the Navbar
     * @param $left_elements   array:  the UI elements on the left side of the navbar
     * @param $right_elements  array:  the UI elements on the right side of the button
     */
    public function __construct($title, $left_elements, $right_elements) {
        $this->title = $title;
        $this->left_elements = $left_elements;
        $this->right_elements=$right_elements;
        $this->template = dirname(__DIR__) . '/html/navbar.html';
    }

    /**
     * Renders the HTML for the Navbar UI Element
     * @return           string:  The generated HTML string
     */
    public function render() {
        $html = file_get_contents($this->template);

        $html = str_replace('@NAVBAR_TITLE', $this->title, $html);

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
        echo $this->renderWithContainer();
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
        $this->template = dirname(__DIR__) . '/html/navbar_button.html';
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
        $this->template = dirname(__DIR__) . '/html/navbar_dropdown.html';
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
