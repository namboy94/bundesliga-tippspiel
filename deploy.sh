#!/bin/bash

echo $DB_PASS > DB_PASS.secret
echo $RECAPTCHA_SITE_KEY > RECAPTCHA_SITE_KEY.secret

if [ -z "$PRODUCTION" ]; then  # NOT production
    composer update
    if [ -z "$LIVE" ]; then
        rsync -av -e 'ssh -p 9022' --delete-after ./* gitlab-runner@develop.hk-tippspiel.com:/var/www/develop.hk-tippspiel.com/app
    else
        rsync -av -e 'ssh -p 9022' --delete-after ./* gitlab-runner@hk-tippspiel.com:/var/www/hk-tippspiel.com/app
    fi

else
    composer update --no-dev
    if [ -z "$LIVE" ]; then
        rsync -av --delete-after ./* /var/www/develop.hk-tippspiel.com/app
    else
        rsync -av --delete-after ./* /var/www/hk-tippspiel.com/app
    fi
fi
