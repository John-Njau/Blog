from app import create_app, db
from app.models import User, Blog, Photos, Comment, Subscriptions, Likes
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('development')

manager = Manager(app)
manager.add_command('server', Server)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Blog=Blog, Likes=Likes, Photos=Photos, Comments=Comment,
                Subscriptions=Subscriptions)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
