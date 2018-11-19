import os

basedir = os.path.abspath(os.path.dirname(__file__))



env = os.environ.get("ENVIRONMENT", "DEBUG")

if env == "DEBUG":
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(os.path.join(basedir,
                                            'license.db'))
    
if env == "PROD":
    SQLALCHEMY_DATABASE_URI = "postgres://db_user:DbUserPostgres@localhost:5432/license_db"

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False