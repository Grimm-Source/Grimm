#!-*- coding: utf-8 -*-

# this file is used to init database for **DEV ONLY**.
# use file grimm-dev.ini to config,
# creates minimal records for each table.

import os
import sys
import datetime as dt

# ensure import grimm
sys.path.append(
    os.path.dirname(
        os.path.realpath(os.path.dirname(__file__)))
)

assert os.environ.get('FLASK_ENV') not in ['production', 'testing']

from grimm import create_app, db
from grimm.models.admin import Admin, User
from grimm.models.activity import Activity, ActivityParticipant
from grimm.models.activity import PickupImpaired, PickupVolunteer

app = create_app()
def create_tables():
    with app.app_context():
        db.create_all()

def create_admin(name='default_admin'):
    admin = Admin(
            name = name,
            password = name,
            email = f'{name}@exmaple.com',
            email_verified = 1
    )
    with app.app_context():
        db.session.add(admin)

        db.session.flush()
        admin_id = admin.id
        db.session.commit()

    return admin_id

def create_user():
    volunteer_name = 'volunteer'
    volunteer = User(
            openid = f'{volunteer_name}_openid',
            registration_date = dt.datetime.now(),
            role = 0,
            name = f'{volunteer_name}',
            real_name = f'{volunteer_name}_real_name',
            id_type = '身份证',
            idcard = fake_id_no('0'),
            idcard_verified = 1,
            phone = fake_mobile('3'),
            phone_verified = 1,
            email = f'{volunteer_name}@exmaple.com',
            email_verified = 1,
            contact = fake_mobile('4'),
            gender = '男',
            birth = dt.datetime.now(),
            address = f'{volunteer_name}_address',
            remark = f'{volunteer_name}_remark',
            audit_status = 1,
            recipient_name = f'{volunteer_name}_recipient_name',
            recipient_address = f'{volunteer_name}_address',
            recipient_phone = fake_mobile('5'),
            avatar_url = f'{volunteer_name}_avatar_url'
    )

    impaired_name = 'impaired'
    impaired = User(
            openid = f'{impaired_name}_openid',
            registration_date = dt.datetime.now(),
            role = 1,
            name = f'{impaired_name}',
            real_name = f'{impaired_name}_real_name',
            id_type = '身份证',
            idcard = fake_id_no('1'),
            idcard_verified = 1,
            disabled_id = 'disabled_id',
            disabled_id_verified = 1,
            phone = fake_mobile('6'),
            phone_verified = 1,
            email = f'{impaired_name}@exmaple.com',
            email_verified = 1,
            contact = fake_mobile('7'),
            gender = '男',
            birth = dt.datetime.now(),
            address = f'{impaired_name}_address',
            emergent_contact = 'imp_ec',
            emergent_contact_phone = fake_mobile('8'),
            remark = f'{impaired_name}_remark',
            audit_status = 1,
            recipient_name = f'{impaired_name}_recipient_name',
            recipient_address = f'{impaired_name}_address',
            recipient_phone = fake_mobile('9'),
            avatar_url = f'{impaired_name}_avatar_url'
    )
    with app.app_context():
        db.session.add(volunteer)
        db.session.add(impaired)

        db.session.flush()
        volunteer_openid = volunteer.openid
        impaired_openid = impaired.openid

        db.session.commit()


    return volunteer_openid, impaired_openid

def create_activity(admin_id, volunteer_openid):
    activity_title = 'default_activity'
    activity = Activity(
            title = activity_title,
            start_time = dt.datetime.now(),
            location = 'activity_location',
            location_latitude = 1.1,
            location_longitude = 2.2,
            end_time = dt.datetime.now(),
            content = f'{activity_title}_content',
            notice = f'{activity_title}_notice',
            others = f'{activity_title}_others',
            admin_raiser = admin_id,
            approver = admin_id,
            assignee = volunteer_openid,
            published = 1,
            tag_ids = 'tag1',
            volunteer_capacity = 1,
            vision_impaired_capacity = 2,
            volunteer_job_title = f'{activity_title}_volunteer_job_title',
            volunteer_job_content = f'{activity_title}_volunteer_job_content',
            sign_in_radius = 1,
            sign_in_token = 'sgn_in_tkn',
            theme_pic_name = f'{activity_title}_theme_pic_name'
    )

    with app.app_context():
        db.session.add(activity)
        db.session.flush()
        activity_id = activity.id
        db.session.commit()

    return activity_id

def create_activityparticipant(activity_id,
        volunteer_openid, impaired_openid):

    for openid in (volunteer_openid, impaired_openid):
        participant = ActivityParticipant(
                activity_id = activity_id,
                participant_openid = openid,
                certificated = 0,
                certificate_date = dt.datetime.now(),
                paper_certificate = 0,
                current_state = 'Registered',
                sign_method = 'token',
                signup_time = dt.datetime.now(),
                signup_latitude = 1.1,
                signup_longitude = 2.2,
                signoff_time = dt.datetime.now(),
                signoff_latitude = 1.1,
                signoff_longitude = 2.2
        )

        with app.app_context():
            db.session.add(participant)
            db.session.commit()

def create_pick(activity_id, volunteer_openid, impaired_openid):
    abbr = 'pkp_impd'
    pickup_impaired = PickupImpaired(
            openid = impaired_openid,
            activity_id = activity_id,
            name = f'{abbr}_name',
            id_no = fake_id_no('2'),
            impaired_no = f'{abbr}_impaired_no',
            emergency_contact = f'{abbr}_emergent_contact',
            pickup_method = f'{abbr}_pickup_method',
            pickup_volunteer_openid = volunteer_openid
    )

    abbr = 'pkp_vlnt'
    pickup_volunteer = PickupVolunteer(
            openid = volunteer_openid,
            activity_id = activity_id,
            name = f'{abbr}_name',
            id_no = fake_id_no('3'),
            pickup_addr = f'{abbr}_pickup_addr',
            provide_service = f'{abbr}_provide_service',
    )

    with app.app_context():
        db.session.add(pickup_impaired)
        db.session.add(pickup_volunteer)
        db.session.commit()

def init_all():
    admin_id = create_admin()
    volunteer_openid, impaired_openid = create_user()
    activity_id = create_activity(admin_id, volunteer_openid)

    create_activityparticipant(activity_id,
            volunteer_openid, impaired_openid)
    create_pick(activity_id, volunteer_openid, impaired_openid)

def fake_mobile(n):
    return '1' + (str(n) * 10)

def fake_id_no(n):
    return str(n) * 18

if __name__ == '__main__':
   create_tables()
   init_all()

