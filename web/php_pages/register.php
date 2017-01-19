<?php

Include "../php_functions/auth.php";

$email = $_POST["register_email"];
$username = $_POST["register_username"];
$password = $_POST["register_password"];
$repeat_password = $_POST["register_password_repeat"];

if (username_exists($username)) {
    echo "Username Exists";
}
else {
    echo "Username Does Not Exist";
}



?>