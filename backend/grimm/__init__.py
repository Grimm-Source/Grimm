import logging
import os

from flask import Flask, Blueprint, request
from flask_compress import Compress
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.engine import create_engine

from config import GrimmConfig

compress = Compress()
db = SQLAlchemy()
engine = create_engine(GrimmConfig.SQLALCHEMY_DATABASE_URI)
TOP_DIR = os.path.dirname(__file__) or "."
migrate = Migrate()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)s:%(lineno)d:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)
blueprint = Blueprint('api', __name__)
api = Api(blueprint)

from grimm.main.views import main
from grimm.admin.views import admin
from grimm.activity.views import activity
from grimm.wxapp.views import wxapp
from grimm.utils import botutils


def create_app():
    app = Flask(__name__)
    app.config.from_object(GrimmConfig)

    compress.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    app.url_map.redirect_defaults = False

    app.register_blueprint(blueprint)
    api.add_namespace(main)
    api.add_namespace(admin)
    api.add_namespace(activity)
    api.add_namespace(wxapp)
    os.makedirs(os.path.dirname(GrimmConfig.GRIMM_USER_DOCUMENT_UPLOAD_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GrimmConfig.GRIMM_DISABLED_ID_UPLOAD_PATH), exist_ok=True)

    return app


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    import traceback

    logger.warning('Handle internal server error start...')
    url, method = request.url, request.method
    message = "Error: " + getattr(error, 'message', str(error))
    traceback = traceback.format_exc()
    botutils.send_error_to_spark(url, method, traceback, message)
    return {"status": "failure", "message": "系统异常"}, getattr(error, 'code', 500)
