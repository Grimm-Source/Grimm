from datetime import datetime

import bcrypt
from flask import jsonify, request
from flask_restx import Resource

from grimm import logger, db
from grimm.main import main
from grimm.models.admin import Admin
from grimm.utils import constants


@main.route("/addAdmin")
class AddAdmin(Resource):
    @main.doc(params={"email": "input email", 'password': 'input password'})
    def get(self):
        """ You can add an admin user by this api for project init """
        email = request.args.get('email') or 'no.reply@rp-i.org'
        password = request.args.get('password') or 'Cisco123456.'
        admin_info = Admin()
        admin_info.id = 0
        admin_info.registration_date = datetime.now().strftime("%Y-%m-%d")
        admin_info.email = email
        admin_info.email_verified = 1
        admin_info.name = "root"
        salt = bcrypt.gensalt(constants.DEFAULT_PASSWORD_SALT)
        bcrypt_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        admin_info.password = bcrypt_password
        db.session.add(admin_info)
        db.session.commit()
        return 'Admin add successfully.'


@main.route("/tags", methods=['GET'])
class TagsDB(Resource):
    def get(self):
        """view function to get all tags info."""
        tag_list = [{'tag_id': i, 'tag_name': constants.TAG_LIST[i]} for i in range(len(constants.TAG_LIST))]
        logger.info("query all tags info successfully")
        return jsonify(tag_list)
