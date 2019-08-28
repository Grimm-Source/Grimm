from flask import Flask,request
import urllib3
import json
import pymysql
from pymysql import IntegrityError

app = Flask(__name__)

with open('config/wxapp.config', 'r') as fp:
    config = json.load(fp=fp, encoding='utf8')

wx_appid = config['appid']
wx_secret = config['secret']

del config

class grimmdb():
    def __init__(self, host, user, passwd, dbName):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
    
    def connect(self):
        self.db = pymysql.connect(self.host, self.user, self.passwd, self.dbName)
        self.cursor = self.db.cursor()

    def get_one(self, sql, args):
        res = None
        try:
            self.connect()
            self.cursor.execute(sql, args)
            res = self.cursor.fetchone()
            self.db.close()
        except Exception as e:
            print("query fail!")
            print("XTYDBG_ERR:", e)
        return res
    
    def get_all(self, sql):
        res = None
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.db.close()
        except:
            print("query fail!")
        return res

    def insert(self, sql, args):
        return self.__edit(sql, args)

    def update(self, sql, args):
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
        json_data['is_register'] = False # make it True for debug
        openid = json_data['openid']
        sql = "SELECT * from mainInfo where openid = %s"
        res = grimmdb.get_one(sql, openid)
        if res is not None:
            json_data['is_register'] = True
            print('xtydbug:', res)
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
        data['openid']           = request.args.get('openid')
        data['birthDate']        = request.args.get("birthdate") #the name different here
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
        data['openid']           = request.form.get("openid")
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
    sql = "INSERT INTO mainInfo (openid, birthDate, usercomment, disabledID, emergencyPerson, emergencyTel, gender, idcard, linkaddress,\
           linktel, name, password, role, tel) VALUES (%(openid)s, %(birthDate)s, %(usercomment)s, %(disabledID)s, %(emergencyPerson)s, %(emergencyTel)s,\
           %(gender)s, %(idcard)s, %(linkaddress)s, %(linktel)s, %(name)s, %(password)s, %(role)s, %(tel)s)"
    try:
        grimmdb.insert(sql, data)
    except Exception as e:
        print('XTYDBG:', e)
        return('XTYDBG: error happen in maininfoset')
    return 'mainInfo set success!'

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if request.method =='GET':
        openid = request.headers.get('Authorization')
        sql = "SELECT * from mainInfo where openid = %s"
        res = grimmdb.get_one(sql, openid)
        print(res)
        birthDate = (res[1]).isoformat()
        if res is not None:
            data = json.loads('{}')
            data['openid']           = res[0]
            data['birthDate']        = birthDate
            data['usercomment']      = res[2]
            data['disabledID']       = res[3]
            data['emergencyPerson']  = res[4]
            data['emergencyTel']     = res[5]
            data['gender']           = res[6]
            data['idcard']           = res[7]
            data['linkaddress']      = res[8]
            data['linktel']          = res[9]
            data['name']             = res[10]
            data['password']         = res[11]
            data['role']             = res[12]
            data['tel']              = res[13]
            print(data)
            ret_data_str = json.dumps(data)
        else:
            print('XTYDBG: query error')
            json_data = json.loads('{"server_errcode": -2}')
            ret_data_str = json.dumps(json_data)
        return ret_data_str
    else:
        data = request.get_data() # get the POST data bytes format
        s_data = str(data, encoding = "utf-8") # decode it to string
        j_data = json.loads(s_data) # make it a json
        openid = j_data['openid']
        print('XTYDBG: new data:', j_data)
        print('XTYDBG:', openid)
        newdata = json.loads('{}')
        newdata['tel']                 = j_data['tel']
        newdata['gender']              = j_data['gender']
        newdata['birthDate']           = j_data['birthDate']
        newdata['linktel']             = j_data['linktel']
        newdata['linkaddress']         = j_data['linkaddress']
        newdata['emergencyPerson']     = j_data['emergencyPerson']
        newdata['emergencyTel']        = j_data['emergencyTel']
        newdata['usercomment']         = j_data['usercomment']
        newdata['openid']              = j_data['openid']
        print("XTYDBG:", newdata)
        sql = "UPDATE mainInfo SET tel=%(tel)s, gender=%(gender)s, birthDate=%(birthDate)s, linktel=%(linktel)s, linkaddress=%(linkaddress)s,\
               emergencyPerson=%(emergencyPerson)s, emergencyTel=%(emergencyTel)s, usercomment=%(usercomment)s WHERE openid=%(openid)s"
        try:
            grimmdb.update(sql, newdata)
        except Exception as e:
            print('XTYDBG_ERR:', e)
            return('{"server_errcode": -3}')
        return 'mainInfo set success!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
