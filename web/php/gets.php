<?php

session_start();
include_once dirname(__FILE__) . '/../templates/dismissable_message.php';

/**
 * Process GET requests that act the same on every page (e.g. switching the theme)
 */
function processGlobalGets() {

    if (isset($_GET['theme'])) {
        $_SESSION['theme'] = $_GET['theme'];
    }
    if (isset($_GET['language'])) {
        $_SESSION['language'] = $_GET['language'];
    }
}

/**
 * Processes displaying dismissable messages
 */
function processDismissableMessages() {

    foreach(array('error', 'warning', 'info', 'success') as $dismissable) {
        if (isset($_SESSION[$dismissable])) {
            DismissableMessage::fromArray($_SESSION[$dismissable])->echo();
            unset($_SESSION[$dismissable]);
        }
    }

}