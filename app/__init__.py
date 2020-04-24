from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app_lol = Flask(__name__)
app_lol.config.from_object(Config)
db = SQLAlchemy(app_lol)
migrate = Migrate(app_lol, db)

from app import routes, models