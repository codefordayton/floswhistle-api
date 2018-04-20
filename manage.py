#!env/bin/python

from flask_script import Manager, Command, Option
from flask_migrate import MigrateCommand

from app import create_app

import scripts.load_zips
import scripts.demo_data

app = create_app()
manager = Manager(app)

class DemoDataCommand(Command):

    def run(self):
        scripts.demo_data.load()

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

class ZipLoaderCommand(Command):

    def run(self):
        scripts.load_zips.load()

manager.add_command('db', MigrateCommand)
manager.add_command('serve', ServerCommand())
manager.add_command('zips', ZipLoaderCommand())
manager.add_command('demo', DemoDataCommand())

manager.run()
