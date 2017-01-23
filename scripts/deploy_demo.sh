#!/usr/bin/bash

rsync -av -e 'ssh -p 9022' --delete-after ../web/ gitlab-runner@demo.tippspiel.krumreyh.com:/var/www/demo.tippspiel.krumreyh.com/public_html
