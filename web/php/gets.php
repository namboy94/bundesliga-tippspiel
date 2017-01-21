<?php

session_start();

/**
 * Process GET requests that act the same on every page (e.g. switching the theme)
 */
function process_global_gets() {

    if (isset($_GET['theme'])) {
        $_SESSION['theme'] = $_GET['theme'];
    }
    if (isset($_GET['language'])) {
        $_SESSION['language'] = $_GET['language'];
    }

}