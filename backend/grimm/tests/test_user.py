import io
import os
import json
import uuid
import pathlib
import unittest
from unittest import mock
# import urllib3
from datetime import datetime, timedelta 
os.environ['FLASK_ENV'] = 'dev'

from grimm import db, GrimmConfig
from grimm.utils import constants
from grimm.models.admin import Admin, User, PreSignedUrl

from .base import post_json, MockResponse
from .base import UserCase

class TestUserRegister(UserCase):
    def test_register(self):
        res = post_json(self.client, '/register', {
                'role': 'volunteer',
                'gender': 'm',
                # TODO?
                'linkaddress': 'linkaddress',
                'name': 'name',
                'phone': uuid.uuid4().hex[:11],
                'email': uuid.uuid4().hex[:10],
                # TODO?
                'avatarUrl': 'avatarUrl',
            }, headers={'Authorization': 'openid'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "success")

class TestUserQuery(UserCase):
    def test_get_users(self):
        # Assuming there are users in the database
        res = self.client.get('/users', headers={})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(len(data) > 0)

        # Check the structure of the response
        for user in data:
            # it's filtered attrs, not all
            for attr in ('openid', 'name', 'role', 'birthdate', 'comment', 'emergencyPerson', 'emergencyTel', 'gender', 'idcard', 'linkaddress', 'linktel', 'phone', 'registrationDate', 'activitiesJoined', 'joindHours', 'audit_status'):
                self.assertIn(attr, user)

    def test_patch_users(self):
        res = self.client.patch('/users', 
                data=json.dumps([
                    {'openid': self.default_volunteer_attrs['openid'],
                        'audit_status': 'approved'}]), 
                headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "success")

class TestUserProfile(UserCase):
    def test_get_profile(self):
        # Assuming there is a user with openid 'openid'
        res = self.client.get('/profile', headers={'Authorization': self.default_volunteer_attrs['openid']})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "success")
        self.assertTrue(len(data) > 0)

        # Check the structure of the response
        expected_attrs = ('openid', 'birthDate', 'usercomment', 'disabledID', 'emergencyPerson',
              'emergencyTel', 'gender', 'idcard', 'linkaddress', 'linktel', 'name',
              'role', 'phone', 'email', 'registrationDate', 'activitiesJoined', 'joindHours')

        for attr in expected_attrs:
            self.assertIn(attr, data)

    def test_get_profile_non_existent_user(self):
        # Trying to retrieve profile for a non-existent user
        res = self.client.get('/profile', headers={'Authorization': 'nonexistentopenid'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "failure")
        self.assertEqual(data["message"], "用户未注册")

    @mock.patch('grimm.utils.botutils.send_error_to_spark')
    def test_post_profile(self, mocked_func):
        mocked_func.return_value = (200, '')

        new_info = {
            "gender": "f",
            "birthDate": "2000-01-01",
            "name": "Test User",
            "linkaddress": "Test address",
            "email": "test@test.com",
            "role": "volunteer"
        }
        res = self.client.post('/profile', data=json.dumps(new_info), headers={
            'Authorization': self.default_volunteer_attrs['openid'], 'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "success")

        # Check the user info in the database is updated
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == self.default_volunteer_attrs['openid']).first()
            self.assertIsNotNone(user_info)
            self.assertEqual(user_info.gender, new_info["gender"])
            self.assertEqual(str(user_info.birth)[:10], new_info["birthDate"])
            self.assertEqual(user_info.name, new_info["name"])
            self.assertEqual(user_info.address, new_info["linkaddress"])
            self.assertEqual(user_info.email, new_info["email"])
            self.assertEqual(user_info.role, 0)  # 0 corresponds to "volunteer"

    @mock.patch('grimm.utils.botutils.send_error_to_spark')
    def test_post_profile_non_existent_user(self, mocked_func):
        mocked_func.return_value = (200, '')

        # Trying to update profile for a non-existent user
        new_info = {
            "gender": "f",
            "birthDate": "2000-01-01",
            "name": "Test User",
            "linkaddress": "Test address",
            "email": "test@test.com",
            "role": "volunteer"
        }
        res = self.client.post('/profile', data=json.dumps(new_info), headers={
            'Authorization': 'nonexistentopenid', 'Content-Type': 'application/json'})
        # As the current function does not handle non-existent users, the status will still be "success"
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "success")

        # Check the non-existent user info in the database is not created
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == 'nonexistentopenid').first()
            self.assertIsNone(user_info)

class TestUserPhoneNumber(UserCase):
    # '/getPhoneNumber'
    @mock.patch('urllib3.PoolManager.request')
    def test_get_phone_number_no_js_code(self, mock_request):
        # Test when `js_code` is not provided in the request.
        info = {}
        response = self.client.post('/getPhoneNumber', data=json.dumps(info), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "failure")

    @mock.patch('urllib3.PoolManager.request')
    def test_get_phone_number_authorization_failure(self, mock_request):
        # Mocking the Weixin API response without `openid`
        mock_request.return_value = MockResponse(json.dumps({'errcode': 40029, 'errmsg': 'invalid code'}), 200)

        info = {
            "js_code": "test_js_code",
            "encryptedData": "test_encrypted_data",
            "iv": "test_iv"
        }
        response = self.client.post('/getPhoneNumber', data=json.dumps(info), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "failure")
        self.assertNotIn("session_key", data)

    @mock.patch('urllib3.PoolManager.request')
    @mock.patch('grimm.utils.decrypt.PhoneNumberDecrypt.decrypt')
    def test_get_phone_number_success(self, mock_decrypt, mock_request):
        # Mocking the Weixin API response with `openid` and `session_key`
        mock_request.return_value = MockResponse(json.dumps({
            'openid': 'test_openid',
            'session_key': 'test_session_key'
        }), 200)

        # Mocking the successful decryption of phone number
        mock_decrypt.return_value = {
            'phoneNumber': '12345678901',
            'countryCode': '86',
            'purePhoneNumber': '12345678901',
            'watermark': {
                'appid': 'test_appid',
                'timestamp': 1234567890
            }
        }

        info = {
            "js_code": "test_js_code",
            "encryptedData": "test_encrypted_data",
            "iv": "test_iv"
        }
        response = self.client.post('/getPhoneNumber', data=json.dumps(info), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["decrypt_data"]["phoneNumber"], '12345678901')
        self.assertNotIn("session_key", data)  # session_key should not be returned in the response

class TestUserSMScode(UserCase):
    def test_get_sms_code_no_phone(self):
        # Test when `phone` URL parameter is not provided.
        response = self.client.get('/smscode')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "failure")
        self.assertIn("无效url参数", data["message"])

    @mock.patch('grimm.utils.smsverify.SMSVerifyToken.send_sms', return_value=False)
    def test_get_sms_code_send_failure(self, mock_send_sms):
        # Test when sending an SMS fails.
        response = self.client.get('/smscode?phone=12345678901')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "failure")
        self.assertIn("发送失败", data["message"])

    @mock.patch('grimm.utils.smsverify.SMSVerifyToken.send_sms', side_effect=Exception("Test Exception"))
    def test_get_sms_code_exception(self, mock_send_sms):
        # Test when an exception is raised during the process.
        response = self.client.get('/smscode?phone=12345678901')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "failure")
        self.assertIn("Test Exception", data["message"])

    @mock.patch('grimm.utils.smsverify.SMSVerifyToken.send_sms', return_value=True)
    @mock.patch('grimm.utils.smsverify.append_token')
    @mock.patch('grimm.utils.smsverify.drop_token')
    def test_get_sms_code_success(self, mock_drop_token, mock_append_token, mock_send_sms):
        # Test when sending an SMS is successful.
        with mock.patch('grimm.utils.smsverify.SMSVerifyToken.vrfcode', new_callable=mock.PropertyMock) as mock_vrfcode:
            mock_vrfcode.return_value = '123456'
            response = self.client.get('/smscode?phone=12345678901')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data["status"], "success")
            # Ensure that logging information includes the correct verification code
            mock_drop_token.assert_called_once_with('12345678901')
            mock_append_token.assert_called()

    def test_post_sms_code_no_token(self):
        # Test when there is no SMS token for the provided phone number.
        with mock.patch('grimm.utils.smsverify.fetch_token', return_value=None):
            data = {"phone": "12345678901", "verification_code": "123456"}
            response = self.client.post('/smscode', data=json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            result = json.loads(response.data)
            self.assertEqual(result["status"], "failure")
            self.assertIn("未向该用户发送验证短信", result["message"])

    @mock.patch('grimm.utils.smsverify.fetch_token')
    def test_post_sms_code_validation_failure(self, mock_fetch_token):
        # Test when SMS code validation fails.
        mock_token = mock.Mock()
        mock_token.validate.return_value = "Validation Failed Message"
        mock_fetch_token.return_value = mock_token

        data = {"phone": "12345678901", "verification_code": "123456"}
        response = self.client.post('/smscode', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result["status"], "failure")
        self.assertIn("Validation Failed Message", result["message"])

    @mock.patch('grimm.utils.smsverify.fetch_token')
    @mock.patch('grimm.utils.smsverify.drop_token')
    def test_post_sms_code_success(self, mock_drop_token, mock_fetch_token):
        # Test when the SMS code validates successfully.
        mock_token = mock.Mock()
        mock_token.validate.return_value = True
        mock_fetch_token.return_value = mock_token

        data = {"phone": "12345678901", "verification_code": "123456"}
        headers = {'Authorization': 'test_openid'}
        response = self.client.post('/smscode', data=json.dumps(data), headers=headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result["status"], "success")
        mock_drop_token.assert_called_once_with('12345678901')

class TestUserAuthorize(UserCase):
    def test_get_authorize_user_no_user_found(self):
        # Test when the provided `Authorization` header does not correspond to any user.
        with self.app.app_context():
            headers = {'Authorization': 'nonexistent_openid'}
            response = self.client.get('/authorize_user', headers=headers)
            data = response.get_json()
            self.assertIsNone(data)

    def test_get_authorize_user_success(self):
        with self.app.app_context():
            headers = {'Authorization': self.default_volunteer_attrs['openid']}
            response = self.client.get('/authorize_user', headers=headers)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIsNotNone(data)
            self.assertEqual(data['name'], self.default_volunteer_attrs['name'])

class TestUserIDCard(UserCase):
    get_signed_urls = '/user_idcard/urls'
    image_url = '/user_idcard/image'

    def test_get_user_identity_urls_not_found(self):
        with self.app.app_context():
            target = 'nonexistent_openid'
            headers = {'Authorization': target}
            response = self.client.get(f'{self.get_signed_urls}/{target}', headers=headers)
            self.assertEqual(response.status_code, 404)
            data = response.get_json()
            self.assertEqual(data, {
                'status': 'failure',
                'error': '用户信息未找到'
            })

    def test_get_user_identity_urls_success(self):
        with self.app.app_context():
            target = self.default_volunteer_attrs['openid']
            headers = {'Authorization': target}
            response = self.client.get(f'{self.get_signed_urls}/{target}', headers=headers)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['status'], 'success')

            # Verify that the pre-signed token is stored in the database with the correct expiration time
            for side in constants.USER_IDENTITY_IMAGE_SIDE:
                token = data['urls'][side].split('token=')[1].split('&')[0]
                self.assertTrue(data['urls'][side].startswith('/user_idcard/image/'))
                self.assertTrue(uuid.UUID(token, version=4))  # Check if the token is a valid UUIDv4
                pre_signed_url = db.session.query(PreSignedUrl).filter_by(token=token).first()
                self.assertIsNotNone(pre_signed_url)
                self.assertEqual(pre_signed_url.openid, target)
                self.assertEqual(pre_signed_url.target_openid, target)
                self.assertTrue(pre_signed_url.expire_at > datetime.now())

    @mock.patch('werkzeug.datastructures.FileStorage.save')
    def test_post_success(self, mock_save): # mock_os, mock_open):
        mock_save.return_value = None

        openid = self.default_volunteer_attrs['openid']
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == openid).first()
            user_info.idcard_obverse_path = None
            user_info.idcard_reverse_path = None
            # FIXME this audit_status set is for test
            user_info.audit_status = 1
            db.session.add(user_info)
            db.session.commit()

            psu = PreSignedUrl.query.filter(PreSignedUrl.openid == openid).first()
            self.assertIsNone(psu)

        response = self.client.post(f'{self.image_url}/{openid}',
                       data={
                           'obverse': (io.BytesIO(b"dummy data"), 'obverse.jpg'),
                       },
                       headers={'Authorization': openid})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        obverse_side_file = os.path.realpath(
            os.path.join(GrimmConfig.GRIMM_USER_DOCUMENT_UPLOAD_PATH,
                f'{openid}_obverse_side.jpg'))
        mock_save.assert_any_call(obverse_side_file)
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == openid).first()
            self.assertIsNotNone(user_info.idcard_obverse_path)
            self.assertIsNone(user_info.idcard_reverse_path)
            # FIXME this audit_status set is for test
            self.assertEqual(user_info.audit_status, 0)

            psu = PreSignedUrl.query.filter(PreSignedUrl.openid == openid).first()
            self.assertEqual(psu.target_openid, openid)

        response = self.client.post(f'{self.image_url}/{openid}',
                       data={
                           'reverse': (io.BytesIO(b"dummy data"), 'obverse.jpg')
                       },
                       headers={'Authorization': openid})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

        reverse_side_file = os.path.realpath(
            os.path.join(GrimmConfig.GRIMM_USER_DOCUMENT_UPLOAD_PATH,
                f'{openid}_reverse_side.jpg'))
        mock_save.assert_any_call(reverse_side_file)
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == openid).first()
            self.assertIsNotNone(user_info.idcard_obverse_path)
            self.assertIsNotNone(user_info.idcard_reverse_path)

    def test_post_no_files(self):
        openid = self.default_volunteer_attrs['openid']
        with self.client as client:
            response = client.post(f'{self.image_url}/{openid}', data={},
                                   headers={'Authorization': openid})

        self.assertEqual(response.status_code, 400)

    def test_post_wrong_filename(self):
        openid = self.default_volunteer_attrs['openid']
        with self.client as client:
            response = self.client.post(f'{self.image_url}/{openid}',
                           data={
                               'not_reverse': (io.BytesIO(b"dummy data"), 'obverse.jpg')
                           },
                           headers={'Authorization': openid})

        self.assertEqual(response.status_code, 400)

    # @mock.patch('flask.send_file', autospec=True)
    def test_get_image_success(self): #, mock_send_file):
        # TODO mock not working
        # mock_send_file.return_value = None
        # Prepopulate the database with a test record and a valid token
        token = 'valid_token'
        openid = self.default_volunteer_attrs['openid']
        side = 'obverse'

        with self.app.app_context():
            pre_signed_url = PreSignedUrl(token=token, openid=openid, expire_at=datetime.now() + timedelta(hours=1), target_openid=openid)
            db.session.add(pre_signed_url)
            db.session.commit()

        obverse_side_file = os.path.realpath(
            os.path.join(GrimmConfig.GRIMM_USER_DOCUMENT_UPLOAD_PATH,
                self.default_volunteer_attrs['idcard_obverse_path']))
        pathlib.Path(obverse_side_file).touch()
        with self.client as client:
            response = client.get(
                    f'{self.image_url}/{openid}?token={token}&side={side}',
                          headers={'Authorization': openid})

        # mock_send_file.assert_any_call(obverse_side_file)
        # mock_send_file.assert_called_once()
        os.remove(obverse_side_file)
        self.assertEqual(response.status_code, 200)

    def test_get_image_invalid_token(self):
        openid = 'test_openid'
        token = 'invalid_token'
        side = 'obverse'

        with self.client as client:
            response = client.get(f'{self.image_url}/{openid}?token={token}&side={side}',
                                  headers={'Authorization': openid})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], '非法口令')

    def test_get_image_expired_token(self):
        # Prepopulate the database with a test record and an expired token
        token = 'expired_token'
        openid = 'test_openid'
        side = 'obverse'
        with self.app.app_context():
            pre_signed_url = PreSignedUrl(token=token, openid=openid, expire_at=datetime.now() - timedelta(hours=1), target_openid=openid)
            db.session.add(pre_signed_url)
            db.session.commit()

        with self.client as client:
            response = client.get(f'{self.image_url}/{openid}?token={token}&side={side}',
                              headers={'Authorization': openid})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], '口令已过期')

class TestUserIDCard(UserCase):
    get_signed_urls = '/user_disabled_id/urls'
    image_url = '/user_disabled_id/image'

    @mock.patch('werkzeug.datastructures.FileStorage.save')
    def test_post_success(self, mock_save): # mock_os, mock_open):
        mock_save.return_value = None

        openid = self.default_impaired_attrs['openid']
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == openid).first()
            user_info.disabled_id_obverse_path = None
            db.session.add(user_info)
            db.session.commit()

            psu = PreSignedUrl.query.filter(PreSignedUrl.openid == openid).first()
            self.assertIsNone(psu)

        response = self.client.post(f'{self.image_url}/{openid}',
                       data={
                           'obverse': (io.BytesIO(b"dummy data"), 'obverse.jpg'),
                       },
                       headers={'Authorization': openid})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        obverse_side_file = os.path.realpath(
            os.path.join(GrimmConfig.GRIMM_DISABLED_ID_UPLOAD_PATH,
                f'{openid}_obverse_side.jpg'))
        mock_save.assert_any_call(obverse_side_file)
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == openid).first()
            self.assertIsNotNone(user_info.disabled_id_obverse_path)

            psu = PreSignedUrl.query.filter(PreSignedUrl.openid == openid).first()
            self.assertEqual(psu.target_openid, openid)

        pathlib.Path(obverse_side_file).touch()
        with self.client as client:
            response = client.get(response.json['urls']['obverse'],
                          headers={'Authorization': openid})

        os.remove(obverse_side_file)
        self.assertEqual(response.status_code, 200)

class TestUserToggleRole(UserCase):
    def test_toggle(self):
        openid = self.default_volunteer_attrs['openid']
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == openid).first()
            self.assertEqual(user_info.role, 0)

        username = self.default_volunteer_attrs['name']
        response = self.client.get(f'/user_tmp_toggle/{username}')
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == openid).first()
            self.assertEqual(user_info.role, 1)

        response = self.client.get(f'/user_tmp_toggle/{username}')
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == openid).first()
            self.assertEqual(user_info.role, 0)

class TestUserIdentityImages(UserCase):
    def test_get_success(self): # mock_os, mock_open):
        openid = self.default_impaired_attrs['openid']
        with self.app.app_context():
            user_info = db.session.query(User).filter(User.openid == openid).first()
            user_info.idcard_obverse_path = 'obverse.png'
            user_info.idcard_reverse_path = 'reverse.png'
            user_info.disabled_id_obverse_path = 'disabled_id_obverse.png'
            db.session.add(user_info)

        response = self.client.get(f'/user_identities/urls/{openid}',
                        headers={'Authorization': openid})
        self.assertEqual(response.status_code, 200)
        urls = response.json['urls']
        self.assertEqual(len(urls), 3)
        for k in urls:
            self.assertTrue(urls[k] is not None and urls[k] != '')

if __name__ == "__main__":
    unittest.main()

