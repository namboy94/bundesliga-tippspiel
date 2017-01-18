<?php

function username_exists($username) {
	$db = open_db_connection();
	
	$stmt = $db->prepare('SELECT name FROM users WHERE name = ?;');
	$stmt->bind_param('s', $username);
	$stmt->execute();

	$result = $stmt->get_result();

	return $result->num_rows > 0;
}

function new_user($username, $password) {
	$hash = password_hash($password, PASSWORD_BCRYPT);
	$db = open_db_connection();

	$stmt = $db->prepare('INSERT INTO users (id, name, hash) VALUES (?, ?, ?);')


}

function change_password($username, $password) {
	$hash = password_hash($password, PASSWORD_BCRYPT);
}

function verify_password($username, $password) {

}

function open_db_connection() {

	$user = file_get_contents("../secrets/db_user", true);
	$pass = file_get_contents("../secrets/db_pass", true)

	return new mysqli("localhost", $user, $pass, "bundesliga_tippspiel");
}

?>