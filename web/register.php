<?php

Include "php_functions/auth.php";

$email = $_POST["register_email"];
$username = $_POST["register_username"];
$password = $_POST["register_password"];
$repeat_password = $_POST["register_password_repeat"];

echo $username;

if (username_exists($username)) {
    echo "Username Exists";
}
else {
    echo "Username Does Not Exist. Creating User: ";
    create_new_user($email, $username, $password);

    if (username_exists($username)) {
        echo "Username Exists Now";
    }
}



?>