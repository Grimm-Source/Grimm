from flask import Flask,request
import urllib3
import json
import pymysql
from pymysql import IntegrityError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    
    def get_all(self, sql, args):
        res = None
        try:
            self.connect()
            self.cursor.execute(sql, args)
            res = self.cursor.fetchall()
            self.db.close()
        except Exception as e:
            print("query fail!")
            print("XTYDBG_ERR:", e)
        return res

    def insert(self, sql, args):
        return self.__edit(sql, args)

    def update(self, sql, args):
        return self.__edit(sql, args)

    def delete(self, sql, args):
        return self.__edit(sql, args)

    def __edit(self, sql, args):
        res = None
        try:
            self.connect()
            res = self.cursor.execute(sql, args)
            self.db.commit()
            self.db.close()
        except IntegrityError:
            print('XTYDBG:IntegrityError')
            self.db.rollback()
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
        res = grimmdb.get_one(sql, openid) # it's a bug need to fix gracefully later
        print(res)
        birthDate = (res[1]).isoformat() # because date is not json serializable
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

@app.route('/login', methods=['POST', 'GET'])
def adminlogin():
    if request.method == 'GET':
        return "failure"
    else:
        newdata = json.loads('{}')
        data = request.get_data()
        s_data = str(data, encoding = "utf-8")
        j_data = json.loads(s_data)
        email = j_data['email']
        print('XTYDBG', email)
        sql = "SELECT * from admin where email = %s"
        res = grimmdb.get_one(sql, email)
        print('XTYDBG', res)
        print("XTYDBG", j_data['password'])
        if res is None:
            newdata['status'] = "failure" # per xiaoting's request 2019-Sep-10
            newdata['message'] = "email error"
            ret_data_str = json.dumps(newdata) # convert to json object
            return ret_data_str
        password = res[2]
        if password == j_data['password']:
            newdata['id'] = res[0]
            newdata['email'] = res[1]
            newdata['type'] = res[3]
        else:
            newdata['status'] = "failure" # per xiaoting's request 2019-Sep-10
            newdata['message'] = "password error"
        ret_data_str = json.dumps(newdata) # convert to json object
        return ret_data_str

@app.route('/admins', methods=['POST', 'GET'])
def admins():
    if request.method == 'GET':
        sql = "SELECT * from admin"
        data = None
        res = grimmdb.get_all(sql, data)
        ret_data = []
        for admin in res:
            if admin is not None:
                newdata = json.loads('{}')
                newdata['id']    = admin[0]
                newdata['email'] = admin[1]
                newdata['type']  = admin[3]
                print("XXXXXXX", newdata)
                ret_data.append(newdata)
        print('XTYDBG', ret_data)
        ret_data_str = json.dumps(ret_data)
        return ret_data_str

@app.route('/admin/<int:id>', methods=['POST', 'GET', 'DELETE'])
def update_admin(id):
    if request.method == 'GET':
        sql = "SELECT * from admin where id = %s"
        res = grimmdb.get_one(sql, id)
        if res is not None:
            newdata = json.loads('{}')
            newdata['id'] = res[0]
            newdata['email'] = res[1]
            newdata['type'] = res[3]
            ret_data_str = json.dumps(newdata)
            return ret_data_str
        return "fail"
    elif request.method == "DELETE":
        if id != 520:
            sql = "DELETE from admin where id = %s"
            grimmdb.delete(sql, id)
        return json.dumps({"status": "delete successful"})

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'GET':
        return "OK"
    else:
        data = request.get_data()
        s_data = str(data, encoding = "utf-8")
        j_data = json.loads(s_data)
        newdata = json.loads('{}')
        newdata['email']      = j_data['email']
        newdata['password']   = j_data['password']
        newdata['admintype']  = "normal"
        sql = "INSERT INTO admin (email, password, admintype) VALUES\
               (%(email)s, %(password)s, %(admintype)s)"
        try:
            grimmdb.insert(sql, newdata)
        except Exception as e:
            print('XTYDBG:', e)
        return data

@app.route('/admin/delete', methods=['POST', 'GET'])
def delete_admin():
    if request.method == 'GET':
        return "OK"
    else:
        data = request.get_data()
        s_data = str(data, encoding = "utf-8")
        j_data = json.loads(s_data)
        adminid = j_data['id']
        print("XTYDBG", type(adminid))
        print("XTYDBG", adminid)
        if adminid != 520:
            sql = "DELETE from admin where id = %s"
            grimmdb.delete(sql, adminid)
        return data

@app.route('/activity', methods=['POST', 'GET'])
def activity():
    if request.method == 'GET':
        return "OK"
    else:
        data = request.get_data()
        print('XTYDBG', type(data))
        s_data = str(data, encoding = "utf-8")
        print('XTYDBG', type(s_data))
        j_data = json.loads(s_data)
        print('XTYDBG', type(j_data))
        print('XTYDBG', j_data)
        newdata = json.loads('{}')
        newdata['adminId']      = j_data['adminId']
        newdata['title']        = j_data['title']
        newdata['location']     = j_data['location']
        newdata['activitydate'] = j_data['date']
        newdata['duration']     = j_data['duration']
        newdata['content']      = j_data['content']
        newdata['notice']       = j_data['notice']
        newdata['others']       = j_data['others']
        sql = "INSERT INTO activity (adminId, title, location, activitydate, duration, content, notice, others) VALUES\
               (%(adminId)s, %(title)s, %(location)s, %(activitydate)s, %(duration)s, %(content)s, %(notice)s, %(others)s)"
        try:
            grimmdb.insert(sql, newdata)
        except Exception as e:
            print('XTYDBG:', e)
        return data


@app.route('/activity/<int:id>', methods=['POST', 'GET', 'DELETE'])
def update_activity(id):
    if request.method == "GET":
        print("XTYDBG", id)
        print("XTYDBG", type(id))
        sql = "SELECT * from activity where id = %s"
        try:
            res = grimmdb.get_one(sql, id)
        except Exception as e:
            print("XTYDBG", e)
        if res is not None:
            newdata  = json.loads('{}')
            datetime = (res[4]).isoformat()
            newdata['id']         = res[0]
            newdata['adminId']    = res[1]
            newdata['title']      = res[2]
            newdata['location']   = res[3]
            newdata['date']       = datetime
            newdata['duration']   = res[5]
            newdata['content']    = res[6]
            newdata['notice']     = res[7]
            newdata['others']     = res[8]
            ret_data_str = json.dumps(newdata)
            print(ret_data_str)
            print("XTYDBG: update activity successful")
            return(ret_data_str)
        else:
            print('XTYDBG: update activity fail')
            return "fail"
    elif request.method == "DELETE":
        sql = "DELETE from activity where id = %s"
        try:
            grimmdb.delete(sql, id)
            return json.dumps({"status": "delete successful"})
        except Exception as e:
            print("*********XTYDBG activity delete failure", e)
            return "failure" # need to define a better protocol to communicate with frontend       
    else:
        data = request.get_data()
        print('XTYDBG', type(data))
        s_data = str(data, encoding = "utf-8")
        print('XTYDBG', type(s_data))
        j_data = json.loads(s_data)
        print('XTYDBG', type(j_data))
        print('XTYDBG', j_data)
        newdata = json.loads('{}')
        newdata['adminId']      = j_data['adminId']
        newdata['title']        = j_data['title']
        newdata['location']     = j_data['location']
        newdata['activitydate'] = j_data['date']
        newdata['duration']     = j_data['duration']
        newdata['content']      = j_data['content']
        newdata['notice']       = j_data['notice']
        newdata['others']       = j_data['others']
        newdata['id']           = j_data['id']
        sql = "UPDATE activity SET adminId=%(adminId)s, title=%(title)s, location=%(location)s, activitydate=%(activitydate)s,\
               duration=%(duration)s, content=%(content)s, notice=%(notice)s, others=%(others)s where id = %(id)s"
        try:
            grimmdb.insert(sql, newdata)
        except Exception as e:
            print('XTYDBG:', e)
        return data
       
        


@app.route('/activity/delete', methods=['POST', 'GET', 'DELETE'])
def delete_activity():
    if request.method == 'DELETE':
        data = request.get_data()
        s_data = str(data, encoding = "utf-8")
        print('XTYDBG', type(s_data))
        print('XTYDBG', s_data)
#activityid = int.from_bytes(data, "big") - 48 # it is big right? TDB, it failed at 2-digits
        activityid = int(s_data)
        print("***********XTYDBG", 'delete successful', activityid)
        sql = "DELETE from activity where id = %s"
        try:
            grimmdb.delete(sql, activityid)
            print("***********XTYDBG", 'delete successful', activityid)
            return json.dumps({"status": "delete successful"})
        except Exception as e:
            print("*********XTYDBG activity delete failure", e)
            return "failure" # need to define a better protocol to communicate with frontend


@app.route('/activities', methods=['POST', 'GET'])
def get_activities():
    if request.method == 'GET':
        sql = "SELECT * from activity"
        data = None
        res = grimmdb.get_all(sql, data)
#        newdata = json.loads('{}')
        print('XTYDBG', res)
        ret_data = []
        for activity in res:
            if activity is not None:
                datetime = (activity[4]).isoformat()
                newdata = json.loads('{}') # need to create the object each loop
                newdata['id']           = activity[0]
                newdata['adminId']      = activity[1]
                newdata['title']        = activity[2]
                newdata['location']     = activity[3]
                newdata['date']         = datetime
                newdata['duration']     = activity[5]
                newdata['content']      = activity[6]
                newdata['notice']       = activity[7]
                newdata['others']       = activity[8]
                print("XXXXXXX", newdata)
                ret_data.append(newdata)
        print('XTYDBG', ret_data)
        ret_data_str = json.dumps(ret_data)
        return ret_data_str
    else:
        return('XTYDBG: set sucessful')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
