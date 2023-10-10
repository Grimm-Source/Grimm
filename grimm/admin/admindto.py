from flask_restx import fields

from grimm.admin import admin


class AdminDto:
    login = admin.model(
        "User login",
        {
            "email": fields.String,
            "password": fields.String
        }
    )

    login_success = admin.model(
        "Login success response",
        {
            "id": fields.Integer,
            "status": fields.String,
            "email": fields.String,
            "type": fields.String
        },
    )
