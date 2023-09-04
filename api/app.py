from flask import Flask, session
import os
import sys

import config
from database.database import db
from blueprints import Blueprint_Auth, Blueprint_Models


# App setup
app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY

# Database setup
# TODO: Find a more reliable way
if os.path.basename(sys.argv[0]) == "pytest":
  app.config ['SQLALCHEMY_DATABASE_URI'] = config.PYTEST_DATABASE_URI
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.PYTEST_DATABASE_TRACK_MODIFICATIONS
else:
  app.config ['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.DATABASE_TRACK_MODIFICATIONS
db.init_app(app)

# Blueprints
app.register_blueprint(Blueprint_Auth.blueprint)
app.register_blueprint(Blueprint_Models.blueprint)

# Run the app
if __name__ == "__main__":
  app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.APP_DEBUG) 