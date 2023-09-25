from flask import Flask, session
from flask_cors import CORS
import os
import sys

from imports import config
from imports.blueprints import Blueprint_Auth, Blueprint_Models, Blueprint_Frontend
from database.database import db
from imports.logs import init_logging

# Init logging
init_logging()

# App setup
app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY
app.logger.info("Flask app initiated")
CORS(app)

# Database setup
# TODO: Find a more reliable way
if os.path.basename(sys.argv[0]) == "pytest":
  app.config ['SQLALCHEMY_DATABASE_URI'] = config.PYTEST_DATABASE_URI
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.PYTEST_DATABASE_TRACK_MODIFICATIONS
else:
  app.config ['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.DATABASE_TRACK_MODIFICATIONS
db.init_app(app)
app.logger.info("Database at " + config.DATABASE_URI + " initiated")

# Blueprints
app.register_blueprint(Blueprint_Auth.blueprint)
app.register_blueprint(Blueprint_Models.blueprint)
app.register_blueprint(Blueprint_Frontend.blueprint)
app.logger.info("Flask blueprints initiated")

# Run the app
if __name__ == "__main__":
  app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.APP_DEBUG) 