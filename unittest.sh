#!/bin/bash

if [ -z "$TEST_DB_PASS" ]; then
    echo "Need to set TEST_DB_PASS"
    exit 1
fi

vendor/bin/phpunit test --coverage-html=coverage

if [ -z "$SHOW_COVERAGE" ]; then
    echo "Not Displaying Coverage"
else
    firefox coverage/index.html
fi