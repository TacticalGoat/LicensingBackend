import os

basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(os.path.join(basedir,
#                                            'license.db'))

SQLALCHEMY_DATABASE_URI = "postgres://db_user:DbUserPostgres@localhost:5432/\
                           license_db"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False