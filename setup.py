"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of bundesliga-tippspiel.

bundesliga-tippspiel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

bundesliga-tippspiel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import sys
from setuptools import setup, find_packages
from subprocess import Popen, check_output


if __name__ == "__main__":

    if sys.argv[1] == "install":
        # Static dependencies (JS and CSS)
        Popen([
            "npm", "install", "--prefix", "bundesliga_tippspiel/static"
        ]).wait()
        Popen(["sass", "--update", "--force", "--style", "compressed",
               "bundesliga_tippspiel/static/scss/style.scss",
               "bundesliga_tippspiel/static/scss"]).wait()
        js_dir = "bundesliga_tippspiel/static/javascript"
        minified = b""
        for js_file in os.listdir(js_dir):
            if js_file == "min.js":
                continue
            js_path = os.path.join(js_dir, js_file)
            minified += check_output(["yui-compressor", js_path]) + b"\n"
        with open(os.path.join(js_dir, "min.js"), "wb") as f:
            f.write(minified)

    setup(
        name="bundesliga-tippspiel",
        version=open("version", "r").read(),
        description="A Bundesliga Tippspiel Website",
        long_description=open("README.md", "r").read(),
        long_description_content_type="text/markdown",
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ],
        url="https://gitlab.namibsun.net/namibsun/python/bundesliga-tippspiel",
        author="Hermann Krumrey",
        author_email="hermann@krumreyh.com",
        license="GNU GPL3",
        packages=find_packages(),
        scripts=list(map(lambda x: os.path.join("bin", x), os.listdir("bin"))),
        install_requires=[
            "flask",
            "flask_login",
            "flask_sqlalchemy",
            "requests",
            "blinker",
            "sentry-sdk",
            "sqlalchemy",
            "werkzeug",
            "cherrypy",
            "puffotter[crypto]",
            "beautifulsoup4",
            "pytz",
            "jerrycan>=0.3.2"
        ],
        include_package_data=True,
        zip_safe=False
    )
