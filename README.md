# Bundesliga Tippspiel

|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel/badges/master/build.svg)](https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel/commits/master)|[![build status](https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel/badges/develop/build.svg)](https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel/commits/develop)|

![Logo](resources/logo/logo-readme.png)

Bundesliga Tippspiel is a website using flask and various plugins that allows
users to bet on Bundesliga matches and compete with one another.

A live version of the page is available at
[hk-tippspiel.com](https://hk-tippspiel.com). A development instance is available
at [develop.hk-tippspiel.com](https://develop.hk-tippspiel.com)

## Documentation

Documentation on the API can be found [here](doc/api/API.md).

For general documentation visit the
[progstats](https://progstats.namibsun.net/projects/bundesliga-tippspiel)
page

# Deployment notes:

Since this site uses MySQL, `python3-mysql` (Ubuntu) needs to be installed.

To correctly function, a lot of environment variables must be set and
written to a JSON file using the [generate_secrets.py](generate_secrets.py)
file. Consult that file to see which variables need to be set.

## Further Information

* [Changelog](CHANGELOG)
* [License (GPLv3)](LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel)
* [Github](https://github.com/namboy94/bundesliga-tippspiel)
* [Progstats](https://progstats.namibsun.net/projects/bundesliga-tippspiel)
* [PyPi](https://pypi.org/project/bundesliga-tippspiel)
