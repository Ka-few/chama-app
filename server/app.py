from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS


from models import db, Chama, Member, Contribution, membership


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chama.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


CORS(app)
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)