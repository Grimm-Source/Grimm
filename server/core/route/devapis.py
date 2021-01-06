# Python 3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import server.core.db as db
import server.utils.db_utils as db_utils
import server.utils.import_user as imptuser
import server.utils.misctools as misc
from server import admin_logger, user_logger
from server.core import api
from flask import request
from flask_restx import Resource


@api.route("/devtools/importusers")
class dev_tools(Resource):
    def get(self):
        """this import history user data into database"""
        return misc.json_dump_http_response(
            {"status": "failed", "message": "please run 'python3 grimm_backup.py -t import_user' in server directly."}
        )
