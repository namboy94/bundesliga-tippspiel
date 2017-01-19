<?php


$email = $_POST["register_email"];
$username = $_POST["register_username"];
$password = $_POST["register_password"];
$repeat_password = $_POST["register_password_repeat"];

echo $username . ": Password is same: ";

if ($password === $repeat_password) {
    echo "Yes.";
}
else {
    echo "No.";
}




?>