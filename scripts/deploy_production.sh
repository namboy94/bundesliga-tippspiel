#!/usr/bin/bash

rsync -av -e 'ssh -p 9022' --delete-after ../web/ gitlab-runner@tippspiel.krumreyh.com:/var/www/demo.tippspiel.krumreyh.com/public_html
rsync -av -e 'ssh -p 9022' --delete-after ../scripts/ gitlab-runner@tippspiel.krumreyh.com:/var/www/tippspiel.krumreyh.com/scripts