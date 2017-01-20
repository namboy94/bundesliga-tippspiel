<?php

Include "php_functions/auth.php";

$username = $_GET['username'];
$confirmation_token = $_GET['confirmation'];

$status = confirm($username, $confirmation_token);

if ($status === "no_user") {
    header('Location: signup.php?not_existing_user=true');
}
elseif ($status === "no_match") {
    header('Location: signup.php?confirmation_not_matching=true');
}
elseif ($status === "already_confirmed") {
    header('Location: signup.php?already_confirmed=true');
}
elseif ($status === "success") {
    header('Location: signup.php?registration_success=true');
}


?>