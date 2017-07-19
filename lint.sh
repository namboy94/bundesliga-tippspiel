#!/bin/bash

if [ -z "$SHOW_LINT_RESULTS" ]; then
    php vendor/phpcheckstyle/phpcheckstyle/run.php --src src --src test --config checkstyle.xml
else
    php vendor/phpcheckstyle/phpcheckstyle/run.php --src src --src test --config checkstyle.xml || firefox style-report/index.html
fi
