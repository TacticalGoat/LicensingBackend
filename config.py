import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(os.path.join(basedir,
                                            'license.db'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')