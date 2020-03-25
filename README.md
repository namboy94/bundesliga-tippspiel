# Bundesliga Tippspiel

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel/badges/master/build.svg)](https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel/commits/master)|[![build status](https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel/badges/develop/build.svg)](https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel/commits/develop)|

![Logo](resources/logo/logo-readme.png)

Bundesliga Tippspiel is a website using flask and various plugins that allows
users to bet on Bundesliga matches and compete with one another.

A live version of the page is available at
[hk-tippspiel.com](https://hk-tippspiel.com). A development instance is available
at [develop.hk-tippspiel.com](https://develop.hk-tippspiel.com)

## Documentation

Documentation on the API can be found [here](doc/api/API.md).

For general documentation visit the
[progstats](https://progstats.namibsun.net/projects/bundesliga-tippspiel)
page

# Deployment notes:

You can deploy the website using docker and docker-compose.
To do this run the following commands:

    # Builds the docker image
    docker build -f docker/Dockerfile -t bundesliga-tippspiel-prod . --no-chache
    # Starts the container and the database container
    docker-compose -f docker/docker-compose-prod.yml up -d
    # If you want to use an updated image
    docker-compose -f docker/docker-compose-prod.yml up -d --no-deps bundesliga-tippspiel-prod-app

The .env file must contain the following variables:

* MYSQL_ROOT_PASSWORD
* MYSQL_USER
* MYSQL_PASSWORD
* MYSQL_DATABASE
* FLASK_SECRET
* RECAPTCHA_SITE_KEY
* RECAPTCHA_SECRET_KEY
* SMTP_ADDRESS
* SMTP_PASSWORD
* SMTP_PORT
* SMTP_HOST
* OPENLIGADB_SEASON
* OPENLIGADB_LEAGUE

# Backing up and restoring

All the data is stored in the mysql/mariadb database, so you can backup the
database using the following command:

    docker exec bundesliga-tippspiel-prod-db-container mysqldump --user root --password=$MYSQL_ROOT_PASSWORD bundesliga_tippspiel > $BACKUPS_DIR/bundesliga_tippspiel-$(date --iso-8601).db

And restoring can be done like this:

    docker exec bundesliga-tippspiel-prod-db-container mysql -u root --password=$MYSQL_ROOT_PASSWORD bundesliga_tippspiel < $BACKUP_FILE

## Further Information

* [Changelog](CHANGELOG)
* [License (GPLv3)](LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel)
* [Github](https://github.com/namboy94/bundesliga-tippspiel)
* [Progstats](https://progstats.namibsun.net/projects/bundesliga-tippspiel)
* [PyPi](https://pypi.org/project/bundesliga-tippspiel)
