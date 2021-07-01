from grimm import db


class Activity(db.Model):
    __tablename__ = 'ACTIVITY'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(60), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    location_latitude = db.Column(db.DECIMAL(9,6))
    location_longitude = db.Column(db.DECIMAL(9,6))
    end_time = db.Column(db.DateTime)
    content = db.Column(db.String(4000), nullable=False)
    notice = db.Column(db.String(4000))
    others = db.Column(db.String(120), nullable=False, server_default='无')
    admin_raiser = db.Column(db.Integer, db.ForeignKey('ADMIN.id'))
    user_raiser = db.Column(db.String(28), db.ForeignKey('USER.openid'))
    approver = db.Column(db.Integer, db.ForeignKey('ADMIN.id'))
    assignee = db.Column(db.String(28), db.ForeignKey('USER.openid'))
    published = db.Column(db.Integer, nullable=False, server_default='0')
    tag_ids = db.Column(db.String(120))
    volunteer_capacity = db.Column(db.Integer, server_default='0')
    vision_impaired_capacity = db.Column(db.Integer, server_default='0')
    volunteer_job_title = db.Column(db.String(500))
    volunteer_job_content = db.Column(db.String(100))
    activity_fee = db.Column(db.Integer, server_default='0')
    sign_in_radius = db.Column(db.Integer)


class RegisteredActivity(db.Model):
    __tablename__ = 'REGISTERED_ACTIVITY'
    user_openid = db.Column(db.String(28), db.ForeignKey('USER.openid'), primary_key=True)
    activity_id = db.Column(db.BigInteger, db.ForeignKey('ACTIVITY.id'), primary_key=True)
    phone = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    needpickup = db.Column(db.Integer, nullable=False, server_default='0')
    topickup = db.Column(db.Integer, nullable=False, server_default='0')
    accepted = db.Column(db.Integer, nullable=False, server_default='-1')


class PickupPair(db.Model):
    __tablename__ = 'PICKUP_PAIR'
    activity_id = db.Column(db.BigInteger, db.ForeignKey('ACTIVITY.id'))
    offer = db.Column(db.String(28), db.ForeignKey('USER.openid'), primary_key=True)
    need = db.Column(db.String(28), db.ForeignKey('USER.openid'), primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)


class ActivityParticipant(db.Model):
    __tablename__ = 'ACTIVITY_PARTICIPANT'
    activity_id = db.Column(db.BigInteger, db.ForeignKey('ACTIVITY.id'), primary_key=True)
    participant_openid = db.Column(db.String(28), db.ForeignKey('USER.openid'), primary_key=True)
    interested = db.Column(db.Integer, server_default='0')
    share = db.Column(db.Integer, server_default='0')
    thumbs_up = db.Column(db.Integer, server_default='0')
    certificated = db.Column(db.Integer)
    certiticate_date = db.Column(db.DateTime)
    paper_certificate = db.Column(db.Integer)
    signup_time = db.Column(db.DateTime)
    signup_latitude = db.Column(db.DECIMAL(9,6))
    signup_longitude = db.Column(db.DECIMAL(9,6))
    signoff_time = db.Column(db.DateTime)
    signoff_latitude = db.Column(db.DECIMAL(9,6))
    signoff_longitude = db.Column(db.DECIMAL(9,6))


class PickupImpaired(db.Model):
    __tablename__ = 'PICKUP_IMPAIRED'
    openid = db.Column(db.String(64), primary_key=True)
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    id_no = db.Column(db.String(18))
    impaired_no = db.Column(db.String(20))
    pickup_addr = db.Column(db.String(256))
    emergency_contact = db.Column(db.String(32))
    pickup_method = db.Column(db.String(32))
    pickup_volunteer_openid = db.Column(db.String(64))


class PickupVolunteer(db.Model):
    __tablename__ = 'PICKUP_VOLUNTEER'
    openid = db.Column(db.String(64), primary_key=True)
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    id_no = db.Column(db.String(18))
    pickup_addr = db.Column(db.String(512))
    provide_service = db.Column(db.String(32))
