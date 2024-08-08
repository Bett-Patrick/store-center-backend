# Standard library imports

# Remote library imports
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy import MetaData
import os




# Instantiate app, set attributes
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://store_center_i2ii_user:nOTZk5gxnUHpKHPl4kSYK2jEayUUjbo1@dpg-cp6uh8nsc6pc73cnggt0-a.oregon-postgres.render.com/store_center_i2ii'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False
# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)



api = Api(app)
bcrypt = Bcrypt(app)

