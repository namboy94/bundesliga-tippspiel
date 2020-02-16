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

import cherrypy
from cherrypy.process.plugins import BackgroundTask
from bundesliga_tippspiel.run import app, init
from bundesliga_tippspiel.bg_tasks import bg_tasks

if __name__ == '__main__':

    init()
    for name, (delay, function) in bg_tasks.items():

        def task_function():
            """
            Makes sure that thread doesn't die if there was an exception
            :return: None
            """
            try:
                function()
            except Exception as e:
                app.logger.error("Encountered exception in background thread "
                                 "{} - {}".format(name, e))


        app.logger.info("Starting background task {}".format(name))
        task = BackgroundTask(delay, task_function)
        task.start()

    cherrypy.tree.graft(app, "/")

    cherrypy.server.unsubscribe()

    # noinspection PyProtectedMember
    server = cherrypy._cpserver.Server()

    server.socket_host = "0.0.0.0"
    server.socket_port = 8000
    server.thread_pool = 30

    server.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
