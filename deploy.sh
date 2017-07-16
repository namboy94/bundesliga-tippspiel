#!/bin/bash

composer update
echo $DB_PASS > DB_PASS.secret
if [ -z "$PRODUCTION" ]; then
    rsync -av -e 'ssh -p 9022' --delete-after ./* gitlab-runner@demo.tippspiel.krumreyh.com:/var/www/demo.tippspiel.krumreyh.com/app
else
    rsync -av --delete-after ./* /var/www/demo.tippspiel.krumreyh.com/app
fi
