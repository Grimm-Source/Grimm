import json
from base64 import b64encode,b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class PhoneNumberDecrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = b64decode(self.sessionKey)
        encryptedData = b64decode(encryptedData)
        iv = b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]


def encrypt_pwd(pwd):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB)
    ct_bytes = cipher.encrypt(pwd.encode('utf-8'))
    return {
        'iv' : b64encode(cipher.iv).decode('utf-8'),
        'Password' : b64encode(ct_bytes).decode('utf-8'),
        'key' : b64encode(key).decode('utf-8'),
        'encrypted' : True
    }


def decrypt_pwd(pwd_info):
    cipher = AES.new(b64decode(pwd_info['key']), AES.MODE_CFB, iv=b64decode(pwd_info['iv']))
    return cipher.decrypt(b64decode(pwd_info['Password'])).decode('utf-8')
