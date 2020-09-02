#!/bin/bash
# Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>
#
# This file is part of bundesliga-tippspiel.
#
# bundesliga-tippspiel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# bundesliga-tippspiel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: backup.sh <backup-file>"
    exit 1
fi

APP="bundesliga-tippspiel-app"
DB="bundesliga-tippspiel-db"
TARGET=$1

rm -rf backup
mkdir backup

docker-compose up --no-recreate -d
docker exec "$APP" printenv > backup/.env
docker exec -i "$DB" bash -c 'pg_dump $POSTGRES_DB -U $POSTGRES_USER' > backup/db.sql
tar -zcvpf "$TARGET" backup
rm -rf backup
