<?php

namespace bundesliga_tippspiel_api;
require __DIR__ . '/../../../vendor/autoload.php';

// Make ErrorException catch everything
use bundesliga_tippspiel\Functions;
use cheetah\Bet;
use cheetah\BetManager;
use ErrorException;
use welwitschi\Authenticator;

set_error_handler(function($errno, $errstr, $errfile, $errline) {
	throw new ErrorException($errstr, $errno, 0, $errfile, $errline);
});
try {

	header('Content-Type: application/json');
	$data = json_decode(file_get_contents("php://input"), true);

	$username = $data["username"];
	$apiKey = $data["api_key"];
	// $matchday = (int)$data["matchday"];

	$auth = new Authenticator(Functions::getMysqli());
	$user = $auth->getUserFromUsername($username);

	if ($user === null) {
		echo json_encode(["status" => "error", "cause" => "no_user"]);
	} elseif (!$user->verifyApiKey($apiKey)) {
		echo json_encode(["status" => "error", "cause" => "invalid_key"]);
	} else {

		echo 1;
		// $betManager = new BetManager(Functions::getMysqli());
		// $bets = $betManager->getAllBetsForUser($user);

	}


} catch (ErrorException $e) {
	echo json_encode(["status" => "error", "cause" => "exception"]);
	throw $e;
}
