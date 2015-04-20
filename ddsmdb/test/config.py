import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '33stanlake#'

DEBUG = True
TESTING = True
LIVESERVER_PORT = 5200

APP_TITLE = 'Data Driven Simulation Management Database'

VERSION = '0.1-dev'

MONGODB_SETTINGS = {
    'db': 'ddsm-test',
    'host': 'localhost',
    'port': 27018
}
