import os
import sys
import unittest
import json
from datetime import datetime, timedelta
os.environ['FLASK_ENV'] = 'dev'

from grimm import create_app, db
from grimm.utils import misctools
from grimm.models.admin import Admin, User
from grimm.models.activity import Project, Duty, Gift, Activity, ActivityParticipant

app = create_app()
def post_json(client, uri, data, headers=None):
    if not isinstance(headers, dict):
        headers = {}

    headers["Content-Type"] = "application/json"

    return client.post(uri, headers=headers, data=json.dumps(data))

class BaseCase(unittest.TestCase):
    def setUp(self):
        self.addCleanup(self.cleanup)
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def cleanup(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

class AdminCase(BaseCase):
    def setUp(self):
        super().setUp()

        name = 'default_admin'
        self.default_admin_attrs = {
                'name': name,
                'password': name,
                'email': f'{name}@exmaple.com',
                'email_verified': 1
        }
        with self.app.app_context():
            admin = Admin(**self.default_admin_attrs)
            admin.password = misctools.generate_password_hash(
                self.default_admin_attrs['password'])
            db.session.add(admin)

            name = 'second_admin'
            second_admin_attrs = {
                    'name': name,
                    'password': name,
                    'email': f'{name}@exmaple.com',
                    'email_verified': 1
            }
            admin = Admin(**second_admin_attrs)
            admin.password = misctools.generate_password_hash(
                second_admin_attrs['password'])
            db.session.add(admin)
            db.session.commit()

class UserCase(BaseCase):
    def setUp(self):
        super().setUp()

        self.default_volunteer_attrs = {
                'role': 0,
                'gender': 'm',
                'address': 'address',
                'name': 'default_volunteer',
                'phone': '123456',
                'email': 'email',
                'avatar_url': 'avatar_url',
                'openid': 'default_volunteer_openid',
                'registration_date': datetime.now(),
                'birth': datetime.now(),
                'idcard_obverse_path': 'default_volunteer_openid_obverse.png',
                'idcard_reverse_path': 'default_volunteer_openid_reverse.png',
        }

        self.default_impaired_attrs = {
                'role': 1,
                'gender': 'm',
                'address': 'address',
                'name': 'default_impaired',
                'phone': '12345678',
                'email': 'default_impaired_email',
                'avatar_url': 'avatar_url',
                'openid': 'default_impaired',
                'registration_date': datetime.now(),
                'birth': datetime.now(),
        }

        with self.app.app_context():
            user = User(**self.default_volunteer_attrs)
            db.session.add(user)
            self.default_volunteer = user
            impaired = User(**self.default_impaired_attrs)
            db.session.add(impaired)
            self.default_impaired = impaired
            db.session.commit()

class ActivityCase(AdminCase, UserCase):
    def setUp(self):
        super().setUp()

        self.default_projects = [{
            'name': 'project_1',
        }, {
            'name': 'project_2',
        }]
        self.default_activities = [{
            'title': 'activity_title_1',
            'location': 'activity_localtion_1',
            'content': 'activity_content_1',
            'notice': 'activity_notice_1',
            'others': 'activity_others_1',
            'theme_pic_name': 'activity_them_1.jpeg',
            'tag_ids': '1,2',
            'volunteer_job_title': 'activity_job_title_1',
            'volunteer_job_content': 'activity_job_content_1',
            'sign_in_token': 's_token_1',
            'start_time': datetime.now() + timedelta(seconds=1),
            'end_time': datetime.now(),
            'activity_fee': 0,
            'admin_raiser': 1,
            'volunteer_capacity': 1,
            'vision_impaired_capacity': 1,
            'project_id': 1,
            'project_seq': 1,
        }, {
            'title': 'activity_title_2',
            'location': 'activity_localtion_2',
            'content': 'activity_content_2',
            'notice': 'activity_notice_2',
            'others': 'activity_others_2',
            'theme_pic_name': 'activity_them_2.jpeg',
            'tag_ids': '1,2',
            'volunteer_job_title': 'activity_job_title_2',
            'volunteer_job_content': 'activity_job_content_2',
            'sign_in_token': 's_token_2',
            'start_time': datetime.now(),
            'end_time': datetime.now(),
            'activity_fee': 0,
            'admin_raiser': 1,
            'volunteer_capacity': 1,
            'vision_impaired_capacity': 1,
            'project_id': 2,
            'project_seq': 2,
        }]
        self.user_helper_attrs = [{
                'role': 1,
                'gender': 'm',
                'address': 'address',
                'name': 'impaired_helper',
                'phone': '123456700',
                'email': 'impaired_helper_email',
                'avatar_url': 'avatar_url',
                'openid': 'impaired_helper',
                'registration_date': datetime.now(),
                'birth': datetime.now(),
                'idcard_obverse_path': 'impaired_helper.png',
                'idcard_reverse_path': 'impaired_helper.png',
            }, {
                'role': 1,
                'gender': 'm',
                'address': 'address',
                'name': 'impaired_helper_1',
                'phone': '123456701',
                'email': 'impaired_helper_1_email',
                'avatar_url': 'avatar_url',
                'openid': 'impaired_helper_1',
                'registration_date': datetime.now(),
                'birth': datetime.now(),
                'idcard_obverse_path': 'impaired_helper_1.png',
                'idcard_reverse_path': 'impaired_helper_1.png',
        }]

        with self.app.app_context():
            # admin = Admin(**self.default_admin_attrs)
            # admin.password = misctools.generate_password_hash(
            #     self.default_admin_attrs['password'])
            # db.session.add(admin)
            # db.session.flush()

            user = User(**{
                'role': 1,
                'gender': 'm',
                'address': 'address',
                'name': 'impaired_leader',
                'phone': '1234567',
                'email': 'impaired_leader_email',
                'avatar_url': 'avatar_url',
                'openid': 'impaired_leader',
                'registration_date': datetime.now(),
                'birth': datetime.now(),
                'idcard_obverse_path': 'impaired_leader.png',
                'idcard_reverse_path': 'impaired_leader.png',
            })
            db.session.add(user)
            db.session.flush()

            for idx, name in enumerate(('志愿者领队', '视障者领队',
                    '主持', '推文写作', '公众号编辑', '拍照')):
                db.session.add(Duty(name=name, seq=idx))

            for idx, name in enumerate(('衣服', '帽子', '臂包', '腰包')):
                db.session.add(Gift(name=name, seq=idx))

            for attrs in self.default_projects:
                activity = Project(**attrs)
                db.session.add(activity)

            db.session.flush()

            for attrs in self.default_activities:
                activity = Activity(**attrs)
                db.session.add(activity)

            db.session.add(ActivityParticipant(user=self.default_volunteer,
                activity=activity, duties=[1,], gifts={1:1}))
            db.session.add(ActivityParticipant(user=user,
                activity=activity, gifts={2:2}))

            for attrs in self.user_helper_attrs:
                user_helper = User(**attrs)
                db.session.add(user_helper)
                db.session.flush()
            db.session.add(ActivityParticipant(
                user=user_helper, activity=activity))

            db.session.commit()

# Helper class for mocking responses
class MockResponse:
    def __init__(self, data, status):
        self.data = data.encode('utf-8')  # Mocked responses should be bytes
        self.status = status
