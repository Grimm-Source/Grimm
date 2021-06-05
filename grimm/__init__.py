import logging
import os

from flask import Flask, Blueprint
from flask_compress import Compress
from flask_migrate import Migrate
from flask_restx import Api
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.engine import create_engine

from config import GrimmConfig


compress = Compress()
db = SQLAlchemy()
engine = create_engine(GrimmConfig.SQLALCHEMY_DATABASE_URI)
TOP_DIR = os.path.dirname(__file__) or "."
socketio = SocketIO(cors_allowed_origins='*', debug=True)
migrate = Migrate()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)s:%(lineno)d:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)
blueprint = Blueprint('api', __name__)
api = Api(blueprint)

from grimm.main.views import main
from grimm.admin.views import admin
from grimm.activity.views import activity
from grimm.wxapp.views import wxapp


def create_app():
    app = Flask(__name__)
    app.config.from_object(GrimmConfig)
    compress.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    app.url_map.redirect_defaults = False
    socketio.init_app(app)

    app.register_blueprint(blueprint)
    api.add_namespace(main)
    api.add_namespace(admin)
    api.add_namespace(activity)
    api.add_namespace(wxapp)

    return app
