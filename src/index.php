<?php

namespace bundesliga_tippspiel;
require __DIR__ . '/../vendor/autoload.php';

session_start();
session_set_cookie_params(86400);

(new Home())->display("en");
