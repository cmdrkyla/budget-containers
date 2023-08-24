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
SESSION_TIMEOUT_MINUTES = 10
STRING_ENCODING = "utf-8"