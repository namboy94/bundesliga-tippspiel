# How to set up MySQL/MariaDB for testing

    CREATE USER 'phpunit'@'localhost' IDENTIFIED BY 'password';
    CREATE DATABASE bundesliga_tippspiel_test;
    GRANT ALL PRIVILEGES ON bundesliga_tippspiel_test . * TO 'phpunit'@'localhost';
    
The phpunit user's password must be stored in the `TEST_DB_PASS` environment
variable.