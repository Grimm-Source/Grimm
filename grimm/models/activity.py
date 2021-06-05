from grimm import db


class Activity(db.Model):
    __tablename__ = 'ACTIVITY'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60))
    start_time = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    end_time = db.Column(db.DateTime)
    content = db.Column(db.String(4000))
    notice = db.Column(db.String(4000))
    others = db.Column(db.String(120))
    admin_raiser = db.Column(db.Integer, db.ForeignKey('ADMIN.id'))
    user_raiser = db.Column(db.String(28), db.ForeignKey('USER.openid'))
    approver = db.Column(db.Integer, db.ForeignKey('ADMIN.id'))
    assignee = db.Column(db.String(28), db.ForeignKey('USER.openid'))
    published = db.Column(db.Integer, nullable=False, default=0)
    tag_ids = db.Column(db.String(120))
    volunteer_capacity = db.Column(db.Integer)
    vision_impaired_capacity = db.Column(db.Integer)
    volunteer_job_title = db.Column(db.String(500))
    volunteer_job_content = db.Column(db.String(100))
    activity_fee = db.Column(db.Integer)
    sign_in_radius = db.Column(db.Integer)


class RegisteredActivity(db.Model):
    __tablename__ = 'REGISTERED_ACTIVITY'
    user_openid = db.Column(db.String(28), db.ForeignKey('USER.openid'), primary_key=True)
    activity_id = db.Column(db.BigInteger, db.ForeignKey('ACTIVITY.id'), primary_key=True)
    phone = db.Column(db.String(16))
    address = db.Column(db.String(80))
    needpickup = db.Column(db.Integer)
    topickup = db.Column(db.Integer)
    accepted = db.Column(db.Integer)


class PickupPair(db.Model):
    __tablename__ = 'PICKUP_PAIR'
    activity_id = db.Column(db.BigInteger, db.ForeignKey('ACTIVITY.id'))
    offer = db.Column(db.String(28), db.ForeignKey('USER.openid'), primary_key=True)
    need = db.Column(db.String(28), db.ForeignKey('USER.openid'), primary_key=True)
    time = db.Column(db.DateTime)
    location = db.Column(db.String(100))


class ActivityParticipant(db.Model):
    __tablename__ = 'ACTIVITY_PARTICIPANT'
    activity_id = db.Column(db.BigInteger, db.ForeignKey('ACTIVITY.id'), primary_key=True)
    participant_openid = db.Column(db.String(28), db.ForeignKey('USER.openid'), primary_key=True)
    interested = db.Column(db.Integer)
    share = db.Column(db.Integer)
    thumbs_up = db.Column(db.Integer)
    certificated = db.Column(db.Integer)
    certiticate_date = db.Column(db.DateTime)
    paper_certificate = db.Column(db.Integer)


class PickupImpaired(db.Model):
    __tablename__ = 'PICKUP_IMPAIRED'
    openid = db.Column(db.String(64), primary_key=True)
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    id_no = db.Column(db.String(18))
    impaired_no = db.Column(db.String(20))
    pickup_addr = db.Column(db.String(256))
    emergency_contact = db.Column(db.String(32))


class PickupVolunteer(db.Model):
    __tablename__ = 'PICKUP_VOLUNTEER'
    openid = db.Column(db.String(64), primary_key=True)
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    id_no = db.Column(db.String(18))
    pickup_addr = db.Column(db.String(512))
    provide_service = db.Column(db.String(32))
