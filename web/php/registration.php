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

session_start();

/**
 * Handles the registration of a new user
 * @param $email    string: The email address of the user
 * @param $username string: The username
 * @param $password string: The password
 * @return          array:  an array detailing the status of the method.
 *                          'status': true if succeeded, else false
 *                          'error_title'/'error_body': An error message detailing what went wrong
 *                          'token': Provided when registration was successful
 */
function register($email, $username, $password) {

    if (usernameExists($username)) {
        return array('status' => false,
                     'error_title' => '@$REGISTER_ERROR_USERNAME_EXISTS_TITLE',
                     'error_body' => '@$REGISTER_ERROR_USERNAME_EXISTS_BODY');
    }
    elseif (emailExists($email)) {
        return array('status' => false,
                     'error_title' => '@$REGISTER_ERROR_EMAIL_USED_TITLE',
                     'error_body' => '@$REGISTER_ERROR_EMAIL_USED_BODY');
    }
    else {
        return array('status' => true,
                     'token' => createNewUser($email, $username, $password));
    }
}

/**
 * Creates a new user in the database
 * @param $email    string: The email address
 * @param $username string: The Username
 * @param $password string: The password (which will be hashed using BCrypt)
 * @return          string: The confirmation token
 */
function createNewUser($email, $username, $password) {

    $db = new Database();

    $id = calculateNextId();
    $hash = password_hash($password, PASSWORD_BCRYPT);
    $confirmation_string = password_hash($email, PASSWORD_BCRYPT);

    $db->queryWrite('INSERT INTO users (user_id, email_address, username, password_hash, confirmation) ' .
                    'VALUES (?, ?, ?, ?, ?)', 'issss', array($id, $email, $username, $hash, $confirmation_string));

    return $confirmation_string;
}

/**
 * Calculates the next user id, which is the currently highest user id incremented by 1
 * @return int: The next user id
 */
function calculateNextId() {
    return (new Database())->query('SELECT MAX(user_id) as id FROM users', '', array())->fetch_assoc()['id'] + 1;
}

/**
 * Checks if a username has already been used
 * @param $username string:  The username to check
 * @return          boolean: true if the username exists, false otherwise
 */
function usernameExists($username) {
    return (new Database())->query('SELECT * FROM users WHERE username=?', 's', array($username))->num_rows > 0;
}

/**
 * Checks if an email address is already in use
 * @param $email string:  The email address to check
 * @return       boolean: true if the email already exists, false otherwise
 */
function emailExists($email) {
    return (new Database())->query('SELECT * FROM users WHERE email_address=?', 's', array($email))->num_rows > 0;
}

/**
 * Processes a confirmation
 * @param $token    string: The confirmation token
 * @param $username string: The username
 * @return          array:  The status, title and body of the resulting message
 */
function confirm($token, $username) {

    $db = new Database();

    $confirmation_query = $db->query('SELECT confirmation FROM users WHERE username=?', 's', array($username));
    $result_count = $confirmation_query->num_rows;
    $previous_token = $confirmation_query->fetch_assoc()[''];

    if ($result_count < 1) {
        return array('status' => 'error',
                     'title' => '@$CONFIRMATION_ERROR_NO_CONFIRMATION_TITLE',
                     'body' => '@$CONFIRMATION_ERROR_NO_CONFIRMATION_BODY');
    }
    elseif ($previous_token === 'confirmed') {
        return array('status' => 'error',
                     'title' => '@$CONFIRMATION_ERROR_ALREADY_CONFIRMED_TITLE',
                     'body' => '@$CONFIRMATION_ERROR_ALREADY_CONFIRMED_BODY');
    }
    elseif ($previous_token !== $token) {
        return array('status' => 'error',
                     'title' => '@$CONFIRMATION_ERROR_TOKEN_MISMATCH_TITLE',
                     'body' => '@$CONFIRMATION_ERROR_TOKEN_MISMATCH_BODY');
    }

    else {
        $db->queryWrite('UPDATE users SET confirmation=? WHERE username=?', 'ss', array('confirmed', $username));
        return array('status' => 'success',
                     'title' => '@$CONFIRMATION_SUCCESS_TITLE',
                     'body' => '@$CONFIRMATION_SUCCESS_BODY');
    }

}