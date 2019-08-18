from flask import Flask,request
import urllib3
import json
import configwx
import pymysql
from pymysql import IntegrityError

app = Flask(__name__)
wx_appid = configwx.wx_appid
wx_secret = configwx.wx_secret

class grimmdb():
    def __init__(self, host, user, passwd, dbName):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
    
    def connect(self):
        self.db = pymysql.connect(self.host, self.user, self.passwd, self.dbName)
        self.cursor = self.db.cursor()

    def get_one(self, sql):
        res = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except:
            print("query fail!")
        return res
    
    def get_all(self, sql):
        res = None
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except:
            print("query fail!")
        return res

    def insert(self, sql, args):
        return self.__edit(sql, args)

    def update(self, sql):
        return self.__edit(sql, args)

    def delete(self, sql):
        return self.__edit(sql, args)

    def __edit(self, sql, args):
        res = None
#        try:
        self.connect()
        res = self.cursor.execute(sql, args)
        self.db.commit()
        self.db.close()
#        except IntegrityError:
#return("duplicated id!")
#       self.db.rollback()
        return res

grimmdb = grimmdb('localhost', 'root', '123Xty1.', 'grimm')

@app.route('/jscode2session')
def wx_jscode2session():
    js_code = request.args.get("js_code")
    
    print(wx_appid)
    print(wx_secret)
    print(js_code)
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + wx_appid + '&secret=' + wx_secret + '&js_code=' + js_code + '&grant_type=authorization_code'
    print('request url:', url)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    
    if response.status == 200:      
        response_data = response.data
        
        json_data = json.loads(response_data)
        json_data['server_errcode'] = 0
        
        json_data['is_register'] = False
        
        ret_data_str = json.dumps(json_data)
        print('response_data: ', ret_data_str)
    else:
        json_data = json.loads('{"server_errcode": -1}')
        ret_data_str = json.dumps(json_data)
    return ret_data_str
    
@app.route('/register', methods=['POST', 'GET'])
def maininfoset():
    data = json.loads('{}')
    if request.method == 'GET':
        data['birthDate']        = request.args.get("birthdate")
        data['usercomment']      = request.args.get("usercomment")
        data['disabledID']       = request.args.get("disabledID")
        data['emergencyPerson']  = request.args.get("emergencyPerson")
        data['emergencyTel']     = request.args.get("emergencyTel")
        data['gender']           = request.args.get("gender")
        data['idcard']           = request.args.get("idcard")
        data['linkaddress']      = request.args.get("linkaddress")
        data['linktel']          = request.args.get("linktel")
        data['name']             = request.args.get("name")
        data['password']         = request.args.get('password')
        data['role']             = request.args.get('role')
        data['tel']              = request.args.get('tel')
    else:
        data['birthDate']        = request.form.get("birthdate")
        data['usercomment']      = request.form.get("usercomment")
        data['disabledID']       = request.form.get("disabledID")
        data['emergencyPerson']  = request.form.get("emergencyPerson")
        data['emergencyTel']     = request.form.get("emergencyTel")
        data['gender']           = request.form.get("gender")
        data['idcard']           = request.form.get("idcard")
        data['linkaddress']      = request.form.get("linkaddress")
        data['linktel']          = request.form.get("linktel")
        data['name']             = request.form.get("name")
        data['password']         = request.form.get('password')
        data['role']             = request.form.get('role')
        data['tel']              = request.form.get('tel')
    sql = "INSERT INTO mainInfo (birthDate, usercomment, disabledID, emergencyPerson, emergencyTel, gender, idcard, linkaddress,\
           linktel, name, password, role, tel) VALUES (%(birthDate)s, %(usercomment)s, %(disabledID)s, %(emergencyPerson)s, %(emergencyTel)s,\
           %(gender)s, %(idcard)s, %(linkaddress)s, %(linktel)s, %(name)s, %(password)s, %(role)s, %(tel)s)"
    try:
        grimmdb.insert(sql, data)
    except Exception as e:
        print('reason', e)
        return('duplicated id!')
    return 'mainInfo set success!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
