from logging.config import dictConfig
from logging import getLogger

from imports import config

def init_logging():
    dictConfig({
        "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "time-rotate": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": config.LOG_FILENAME,
                "when": "D",
                "interval": 1,
                "backupCount": 14,
                "formatter": "default",
            },
        },
        "root": {
            "level": config.LOG_LEVEL, 
            "handlers": ["console", "time-rotate"]
        },
    })

    getLogger("werkzeug").setLevel("INFO")