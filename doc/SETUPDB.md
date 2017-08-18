# How to set up MySQL/MariaDB for testing

    CREATE USER 'tippspiel'@'localhost' IDENTIFIED BY 'password';
    CREATE DATABASE tippspiel_bundesliga_test;
    GRANT ALL PRIVILEGES ON tippspiel_bundesliga_test . * TO 'phpunit'@'localhost';
    
The phpunit user's password must be stored in the `TEST_DB_PASS` environment
variable.