<?php

function username_exists($username) {
	$db = open_db_connection();
	
	$stmt = $db->prepare('SELECT name FROM users WHERE name = ?;');
	$stmt->bind_param('s', $username);
	$stmt->execute();

	$result = $stmt->get_result();
	$db->close();

	return $result->num_rows > 0;
}

function new_user($username, $password) {
	$hash = password_hash($password, PASSWORD_BCRYPT);
	$db = open_db_connection();

	$stmt = $db->prepare('INSERT INTO users (id, name, hash) VALUES (?, ?, ?);');
	$stmt->bind_param('i', get_next_user_id());
    $stmt->bind_param('s', $username);
    $stmt->bind_param('s', $hash);
    $stmt->execute();

    $db->commit();
    $db->close();
}

function get_next_user_id() {

    $db = open_db_connection();
    $result = $db->query("SELECT MAX(id) FROM users");
    $next_id = $result->fetch_assoc()["id"] + 1;

    $db->close();

    return $next_id;
}

function change_password($username, $password) {
	$hash = password_hash($password, PASSWORD_BCRYPT);
    $db = open_db_connection();

    $stmt = $db->prepare('UPDATE users SET hash=? WHERE name=?');
    $stmt->bind_param('s', $hash);
    $stmt->bind_param('s', $username);
    $stmt->execute();

    $db->commit();
    $db->close();

}

function verify_password($username, $password) {
    $db = open_db_connection();

    $stmt = $db->prepare("SELECT hash FROM users WHERE name=?");
    $stmt->bind_param('s', $username);
    $stmt->execute();
    $result = $stmt->get_result();

    $hash = $result->fetch_assoc()["hash"];
    $db->close();

    return password_verify($password, $hash);

}

function open_db_connection() {

	$user = file_get_contents("../secrets/db_user", true);
	$pass = file_get_contents("../secrets/db_pass", true);

	return new mysqli("localhost", $user, $pass, "bundesliga_tippspiel");
}

?>