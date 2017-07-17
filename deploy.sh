#!/bin/bash

composer update
echo $DB_PASS > DB_PASS.secret
echo $RECAPTCHA_SITE_KEY > RECAPTCHA_SITE_KEY.secret
if [ -z "$PRODUCTION" ]; then
    rsync -av -e 'ssh -p 9022' --delete-after ./* gitlab-runner@develop.hk-tippspiel.com:/var/www/develop.hk-tippspiel.com/app
else
    rsync -av --delete-after ./* /var/www/develop.hk-tippspiel.com/app
fi
