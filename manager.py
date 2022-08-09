
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from database import db

migrate = Migrate(app, db, render_as_batch=True, compare_type=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
