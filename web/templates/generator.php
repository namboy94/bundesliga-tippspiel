<?php
/**
 * Copyright Hermann Krumrey<hermann@krumreyh.com> 2017
 */

session_start();
include_once dirname(__FILE__) . '/../strings/dictionary.php';

/**
 * Class HtmlGenerator is a common interface for HTML generators to enable a developer
 * to expect some sort of default behaviour for all template generators
 */
abstract class HtmlGenerator {

    /**
     * @var string: The HTML template file to be used when generating the content
     */
    protected $template;

    /**
     * Changes the HTML template file to be used
     * @param $template string: The new template file
     * @return          void
     */
    public function changeTemplateFile($template) {
        $this->template = $template;
    }

    /**
     * Directly prints the rendered HTML content
     * @return void
     */
    public function echo() {
        $dictionary = new Dictionary($_SESSION['language']);
        echo $dictionary->translate($this->render());
    }

    /**
     * Renders the HTML string
     * @return string: The generated HTML content
     */
    public abstract function render();

}