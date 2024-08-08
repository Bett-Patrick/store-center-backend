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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://storecenter_db_user:v7hVd3oxz1TYI6dhbaRk4ldCGTFwS2ll@dpg-cqqakgbv2p9s73b4lda0-a.oregon-postgres.render.com/storecenter_db'
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

