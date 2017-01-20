<?php

Include "php_functions/auth.php";
Include "resources/strings-de.php";
Include "resources/strings-en.php";

session_start();

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

if ($email === "") {
    header('Location: signup.php?no_email=true');
}
else if ($username === "") {
    header('Location: signup.php?no_username=true');
}
else if ($password === "") {
    header('Location: signup.php?no_password=true');
}
else if ($password != $repeat_password) {
    header('Location: signup.php?password_mismatch=true');
}
else if (username_exists($username)) {
    header('Location: signup.php?username_exists=true');
}
else if (email_used($email)) {
    header('Location: signup.php?email_used=true');
}
else if (strlen($password) < 8) {
    header('Location: signup.php?password_too_short=true');
}
else {

    $confirmation = create_new_user($email, $username, $password);

    $from = "From: " . $dictionary['@$WEBSITE_NAME']  . "<noreply@tippspiel.krumreyh.com>";
    $title = $dictionary['@$CONFIRMATION_NAME'];
    $body = $dictionary['@$EMAIL_CONFIRMATION'] . '<a href="tippspiel.krumreyh.com/confirmation.php?confirmation='
            . $confirmation . "&username=" . $username . '">Confirmation<a>';
    mail($email, $title, $body, $from);

    header('Location: signup.php?registration_initialized=true');

}



?>