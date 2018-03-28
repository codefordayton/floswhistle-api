#!env/bin/python

from flask_script import Manager, Command, Option
from flask_migrate import MigrateCommand

from app import create_app

app = create_app()
manager = Manager(app)

class ServerCommand(Command):

    def __init__(self, default_port=manager.app.config['SERVER_PORT']):
        self.default_port=default_port

    def get_options(self):
        return [
            Option('--port', '-p', dest='port', default=self.default_port),
        ]

    def run(self, port):
        port = int(port)
        manager.app.run(host=manager.app.config['SERVER_HOST'], port=port)

manager.add_command('db', MigrateCommand)
manager.add_command('serve', ServerCommand())

manager.run()
