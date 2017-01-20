<?php

Include "php_functions/auth.php";

session_start();

$email = $_POST["login_email"];
$password = $_POST["login_password"];


if (verify_password($email, $password)) {

    $token = login($email);

    if ($token === "") {
        header('Location: signup.php?invalid_credentials');
    }

    $_SESSION['token'] = $token;
    header('Location: index.php');
}
else {
    header('Location: signup.php?invalid_credentials');
}

?>