<?php

# user_id, username, email_address, password_hash

function username_exists($username) {
	$db = open_db_connection();
	
	$stmt = $db->prepare('SELECT username FROM users WHERE username = ?;');
	$stmt->bind_param('s', $username);
	$stmt->execute();

	$result = $stmt->get_result();
	$db->close();

	return $result->num_rows > 0;
}

function create_new_user($email_address, $username, $password) {
	$hash = password_hash($password, PASSWORD_BCRYPT);
	$db = open_db_connection();

	$stmt = $db->prepare('INSERT INTO users (user_id, email_address, username, password_hash) VALUES (?, ?, ?, ?);');
	$stmt->bind_param('i', get_next_user_id());
	$stmt->bind_param('s', $email_address);
    $stmt->bind_param('s', $username);
    $stmt->bind_param('s', $hash);
    $stmt->execute();

    $db->commit();
    $db->close();
}

function get_next_user_id() {

    $db = open_db_connection();
    $result = $db->query("SELECT MAX(user_id) FROM users");
    $next_id = $result->fetch_assoc()["id"] + 1;

    $db->close();

    return $next_id;
}

function change_password($username, $password) {
	$hash = password_hash($password, PASSWORD_BCRYPT);
    $db = open_db_connection();

    $stmt = $db->prepare('UPDATE users SET password_hash=? WHERE username=?');
    $stmt->bind_param('s', $hash);
    $stmt->bind_param('s', $username);
    $stmt->execute();

    $db->commit();
    $db->close();

}

function verify_password($username, $password) {
    $db = open_db_connection();

    $stmt = $db->prepare("SELECT password_hash FROM users WHERE username=?");
    $stmt->bind_param('s', $username);
    $stmt->execute();
    $result = $stmt->get_result();

    $hash = $result->fetch_assoc()["hash"];
    $db->close();

    return password_verify($password, $hash);

}

function open_db_connection() {

	$user = trim(file_get_contents("../secrets/db_user", true));
	$pass = trim(file_get_contents("../secrets/db_pass", true));

	return new mysqli("localhost", $user, $pass, "bundesliga_tippspiel");
}

?>