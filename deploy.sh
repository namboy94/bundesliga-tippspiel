#!/bin/bash

if [ -z "$PRODUCTION" ]; then
    rsync -av . hermann@namibsun.net
else
    rsync -av .
fi
