<?php

namespace bundesliga_tippspiel_api;
require __DIR__ . '/../../../vendor/autoload.php';

// Make ErrorException catch everything
use bundesliga_tippspiel\Functions;
use ErrorException;
use welwitschi\Authenticator;

set_error_handler(function($errno, $errstr, $errfile, $errline) {
	throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
});
try {
	header('Content-Type: application/json');
	$data = json_decode(file_get_contents("php://input"), true);
	$username = $data["username"];
	$password = $data["password"];

	$auth = new Authenticator(Functions::getMysqli());
	$user = $auth->getUserFromUsername($username);


	if ($user === null) {
		echo json_encode(["status" => "error", "cause" => "no_user"]);
	} elseif (!$user->doesPasswordMatch($password)) {
		echo json_encode(["status" => "error", "cause" => "password_fail"]);
	} else {
		$apiKey = $user->generateNewApiKey();
		if ($apiKey === null) {
			echo json_encode([
				"status" => "error",
				"cause" => "not_confirmed"
			]);
		} else {
			echo json_encode(["status" => "success", "key" => $apiKey]);
		}
	}

} catch (ErrorException $e) {
	echo json_encode(["status" => "error", "cause" => "exception"]);
	throw $e;
}
