# How to set up MySQL/MariaDB for website

    CREATE USER 'tippspiel'@'localhost' IDENTIFIED BY 'password';
    CREATE DATABASE tippspiel_bundesliga;
    GRANT ALL PRIVILEGES ON tippspiel_bundesliga . * TO 'tippspiel'@'localhost';
    
The tippspiel user's password must be stored in a file in the root directory of
this project with the name DB_PASS.secret

Make sure this file is not accessible from outside!!!