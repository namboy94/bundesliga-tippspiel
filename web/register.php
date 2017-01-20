<?php

Include "php_functions/auth.php";
Include "resources/strings-de.php";
Include "resources/strings-en.php";

$email = $_POST["register_email"];
$username = $_POST["register_username"];
$password = $_POST["register_password"];
$repeat_password = $_POST["register_password_repeat"];

switch ($_SESSION['language']) {
    case 'de':
        $dictionary = get_german_dictionary();
        break;
    default:
        $dictionary = get_english_dictionary();
}

if ($password != $repeat_password) {
    header('Location: signup.php?password_mismatch=true');
}

if (username_exists($username)) {
    echo "Username Exists";
}
else {

    $confirmation = create_new_user($email, $username, $password);

    $from = "From: " . $dictionary['@$WEBSITE_NAME']  . "<noreply@tippspiel.krumreyh.com>";
    $title = $dictionary['@$CONFIRMATION'];
    $body = $dictionary['@$EMAIL_CONFIRMATION'] . "tippspiel.krumreyh.com/confirmation.php?" . $confirmation;
    mail($email, $title, $body, $from);

    header('Location: login.php?registration=initialized');

}



?>