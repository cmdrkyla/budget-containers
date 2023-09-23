"""
Global config settings
"""

import os

ROOT_PATH = os.path.abspath(os.getcwd())
APP_DEBUG = True
APP_HOST = "localhost"
APP_PORT = 8001
APP_SECRET_KEY = "8D88FF35A9EB5171383FF3AEB9866"
DATABASE_TRACK_MODIFICATIONS = False
DATABASE_URI = 'sqlite:///' + ROOT_PATH + '/database/BudgetContainers.db'
DEFAULT_TIMEZONE = "UTC"
LOG_FILENAME = ROOT_PATH + '/logs/flask.log'
LOG_LEVEL = "INFO"
PYTEST_DATABASE_TRACK_MODIFICATIONS = False
PYTEST_DATABASE_URI = 'sqlite:///:memory:'
SERVER_TIMEZONE = "America/New_York"
SESSION_TIMEOUT_MINUTES = 30
STRING_ENCODING = "utf-8"