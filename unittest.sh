#!/bin/bash

if [ -z "$TEST_DB_PASS" ]; then
    echo "Need to set TEST_DB_PASS"
    exit 1
fi

echo $TEST_DB_PASS > DB_PASS.secret
vendor/bin/phpunit test --coverage-html=coverage --stderr

if [ -z "$SHOW_COVERAGE" ]; then
    echo "Not Displaying Coverage"
else
    firefox coverage/index.html
fi

