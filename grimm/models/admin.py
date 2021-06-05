from grimm import db
from sqlalchemy import func


class Admin(db.Model):
    __tablename__ = 'ADMIN'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    registration_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    password = db.Column(db.String(60), default=0, nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(32), unique=True)
    email_verified = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'USER'
    openid = db.Column(db.String(28), primary_key=True, nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), default='志愿者')
    real_name = db.Column(db.String(100))
    id_type = db.Column(db.String(100), default='身份证')
    idcard = db.Column(db.String(18), unique=True)
    idcard_verified = db.Column(db.Integer, default=0)
    disabled_id = db.Column(db.String(60))
    disabled_id_verified = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(16))
    phone_verified = db.Column(db.Integer, default=0, nullable=False)
    email = db.Column(db.String(32))
    email_verified = db.Column(db.Integer, default=0)
    contact = db.Column(db.String(16))
    gender = db.Column(db.String(1), nullable=False)
    birth = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(80))
    emergent_contact = db.Column(db.String(8))
    emergent_contact_phone = db.Column(db.String(16))
    activities_joined = db.Column(db.Integer, default=0, nullable=False)
    activities_absence = db.Column(db.Integer, default=0, nullable=False)
    remark = db.Column(db.String(255))
    audit_status = db.Column(db.Integer, default=0, nullable=False)
    push_status = db.Column(db.Integer, default=0, nullable=False)
    recipient_name = db.Column(db.String(100))
    recipient_address = db.Column(db.String(80))
    recipient_phone = db.Column(db.String(16))
