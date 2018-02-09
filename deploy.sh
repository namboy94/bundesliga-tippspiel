#!/bin/bash

if [ -z "$DB_PASS" ]; then
    echo "Need to set DB_PASS"
    exit 1
fi

if [ -z "$KUDUBOT_WHATSAPP_CONFIG" ]; then
    echo "Need to set KUDUBOT_WHATSAPP_CONFIG"
    exit 1
fi

if [ -z "$KUDUBOT_TELEGRAM_CONFIG" ]; then
    echo "Need to set KUDUBOT_TELEGRAM_CONFIG"
    exit 1
fi

echo $DB_PASS > DB_PASS.secret
echo $RECAPTCHA_SITE_KEY > RECAPTCHA_SITE_KEY.secret
echo $KUDUBOT_WHATSAPP_CONFIG > kudubot/connection_config/whatsapp.conf
echo $KUDUBOT_TELEGRAM_CONFIG > kudubot/connection_config/telegram.conf

if [ -z "$PRODUCTION" ]; then  # NOT production
    echo "domain = \"develop.hk-tippspiel.com\"" > kudubot/modules/bundesliga_tippspiel_reminder/__init__.py
    composer update
    if [ -z "$LIVE" ]; then
        rsync -av -e 'ssh -p 9022' --delete-after ./* gitlab-runner@develop.hk-tippspiel.com:/var/www/develop.hk-tippspiel.com/app
        rsync -av -e 'ssh -p 9022' kudubot/ gitlab-runner@hk-tippspiel.com:/var/www/develop.hk-tippspiel.com/kudubot
        ssh -p 9022 gitlab-runner@develop.hk-tippspiel.com "chmod 777 /var/www/develop.hk-tippspiel.com/kudubot"
        ssh -p 9022 gitlab-runner@develop.hk-tippspiel.com "chmod 777 /var/www/develop.hk-tippspiel.com/kudubot/data -R"
    else
        rsync -av -e 'ssh -p 9022' --delete-after ./* gitlab-runner@hk-tippspiel.com:/var/www/hk-tippspiel.com/app
        rsync -av -e 'ssh -p 9022' kudubot/ gitlab-runner@hk-tippspiel.com:/var/www/hk-tippspiel.com/kudubot
        ssh -p 9022 gitlab-runner@hk-tippspiel.com "chmod 777 /var/www/hk-tippspiel.com/kudubot"
        ssh -p 9022 gitlab-runner@hk-tippspiel.com "chmod 777 /var/www/hk-tippspiel.com/kudubot/data -R"
    fi

else
    echo "domain = \"hk-tippspiel.com\"" > kudubot/modules/bundesliga_tippspiel_reminder/__init__.py
    composer update --no-dev
    if [ -z "$LIVE" ]; then  # NOT LIVE
        rsync -av --delete-after ./* /var/www/develop.hk-tippspiel.com/app
        rsync -av kudubot/ /var/www/develop.hk-tippspiel.com/kudubot
        chmod 777 /var/www/develop.hk-tippspiel.com/kudubot
        chmod 777 /var/www/develop.hk-tippspiel.com/kudubot/data -R
    else
        rsync -av --delete-after ./* /var/www/hk-tippspiel.com/app
        rsync -av kudubot/ /var/www/hk-tippspiel.com/kudubot
        chmod 777 /var/www/hk-tippspiel.com/kudubot
        chmod 777 /var/www/hk-tippspiel.com/kudubot/data -R
    fi
fi
