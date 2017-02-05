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

include_once dirname(__FILE__) . '/database.php';

/**
 * Initializes a default session, if none has yet been initialized
 */
function initializeSession() {

    session_start();

    if (!isset($_SESSION['theme'])) {
        $_SESSION['theme'] = "default";
    }
    if (!isset($_SESSION['language'])) {
        $_SESSION['language'] = "en";
    }
}

/**
 * Logs the user in.
 * @param $email    string: The user's email address
 * @param $password string: The user's password
 * @return          array:  The Status of the login attempt
 *                          status: the status of the attempt. If true, successful, else not successful
 *                          title, body: if failed, detailed explanation
 */
function login($email, $password) {

    if (isLoggedIn()) {
        return array('status' => false,
                     'title' => '@$LOGIN_ERROR_ALREADY_LOGGED_IN_TITLE',
                     'body' => '@$LOGIN_ERROR_ALREADY_LOGGED_IN_BODY');
    }
    elseif (!passwordMatches($email, $password)) {
        return array('status' => false,
                     'title' => '@$LOGIN_ERROR_PASSWORD_MISMATCH_TITLE',
                     'body' => '@$LOGIN_ERROR_PASSWORD_MISMATCH_BODY');
    }
    else {

        $token = password_hash($email, PASSWORD_DEFAULT);
        $db = new Database();
        $result = $db->query('SELECT user_id, username, confirmation FROM users WHERE email_address=?',
            's', array($email), true);

        if (count($result) < 1) {
            return array('status' => false,
                         'title' => '@$LOGIN_ERROR_USER_DOES_NOT_EXIST_TITLE',
                         'body' => '@$LOGIN_ERROR_USER_DOES_NOT_EXIST_BODY');

        }
        else if ($result[0]['confirmation'] !== 'confirmed') {
            return array('status' => false,
                        'title' => '@$LOGIN_ERROR_NOT_CONFIRMED_TITLE',
                        'body' => '@$LOGIN_ERROR_NOT_CONFIRMED_BODY');
        }
        else {
            $id = $result[0]['user_id'];

            if ($db->query('SELECT * FROM sessions WHERE id=?', 'i', array($id))->num_rows === 0) {
                $db->queryWrite('INSERT INTO sessions (id, token) VALUES (?, ?)', 'is', array($id, $token));
            } else {
                $db->queryWrite('UPDATE sessions SET token=? WHERE id=?', 'si', array($token, $id));
            }

            $_SESSION['id'] = $id;
            $_SESSION['token'] = $token;
            $_SESSION['userdata'] = array('email' => $email, 'id' => $id, 'name' => $result[0]['username']);

            return array('status' => true, );
        }
    }
}

/**
 * Checks if the password for an email address matches
 * @param $email     string:  The Email Address
 * @param $password  string:  The Password to check
 * @return           boolean: true if the password matches, false otherwise
 */
function passwordMatches($email, $password) {

    $db = new Database();
    $result = $db->query('SELECT password_hash FROM users WHERE email_address=?', 's', array($email));

    return password_verify($password, $result->fetch_assoc()['password_hash']);
}

/**
 * @return bool: true if the user is logged in currently, false otherwise
 */
function isLoggedIn() {

    if (!isset($_SESSION['id']) or !isset($_SESSION['token'])) {
        return false;
    }
    else {

        $db = new Database();
        $result = $db->query('SELECT token FROM sessions WHERE id=?', 'i', array($_SESSION['id']));

        if ($result->num_rows < 1) {
            return false;
        }
        elseif ($result->fetch_assoc()['token'] !== $_SESSION['token']) {
            return false;
        }
        else {
            return true;
        }
    }
}

/**
 * Logs out the user
 */
function logOut() {

    if (isLoggedIn()) {

        (new DataBase())->query('DELETE FROM sessions WHERE id=? AND token=?', 'is',
            array($_SESSION['id'], $_SESSION['token']));

        $language = $_SESSION['language'];
        $theme = $_SESSION['language'];
        session_unset();
        $_SESSION['language'] = $language;
        $_SESSION['language'] = $theme;
    }
}

/**
 * Checks if user is logged in on a particular site. If not, the user is redirected to the home page
 * @param $target string: The redirect target
 */
function redirectInvalidUser($target='index.php') {
    if (!isLoggedIn()) {
        (new DismissableMessage('error', '@$UNAUTHORIZED_MESSAGE_TITLE', '@$UNAUTHORIZED_MESSAGE_BODY'))
            ->show($target);
    }
}

/**
 * Redirects a banned IP address
 */
function redirectBannedIp() {
    $ip = $_SERVER['REMOTE_ADDR'];
    $banned_ips = explode(',', trim(file_get_contents(dirname(__FILE__) . '/../resources/banned_ips')));

    $banned = false;
    foreach ($banned_ips as $banned_ip) {
        if (strcmp($ip, $banned_ip)) {
            $banned = true;
        }
        else {
            echo '<p>' . $ip . '</p>';
            echo '<p>' . $banned_ip . '</p>';
        }
    }

    //print_r($banned_ips);
    //echo $ip;
    //echo $banned;

    if ($banned) {
        header('Location: https://google.com');
        exit();
    }
}
