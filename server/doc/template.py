from flask import Flask,request
import urllib3
import json
import time

# import config

app = Flask(__name__)

# wx_appid = config.wx_appid
# wx_secret = config.wx_appid

@app.route('/jscode2session')
def wx_jscode2session():
	js_code = request.args.get("js_code")
	
	url = f'https://api.weixin.qq.com/sns/jscode2session?appid={wx_appid}&secret={wx_secret}&js_code={js_code}&grant_type=authorization_code'
	print('request url:', url)
	http = urllib3.PoolManager()
	response = http.request('GET', url)
	
	if response.status == 200:		
		response_data = response.data
		
		json_data = json.loads(response_data)
		json_data['server_errcode'] = 0
		
		# json_data['is_register'] = False
		json_data['is_register'] = False
		
		ret_data_str = json.dumps(json_data)
		print('response_data: ', ret_data_str)
	else:
		json_data = json.loads('{"server_errcode": -1}')
		ret_data_str = json.dumps(json_data)
	return ret_data_str
	
@app.route('/register')
def register():
	data = json.loads('{}')
	data['userName'] = request.args.get("userName")
	data['phoneNum'] = request.args.get("phoneNum")
	
	return json.dumps(data)

@app.route('/profile/<int:open_id>', methods=['GET'])
def getProfile(open_id):
	time.sleep(1)#fake time
	return json.dumps({
        "name": "何君尧",
        "nickName": "小手冰凉的小何何",
        "birthday":"1968-01-01",
        "gender":0,
        "idNum":"310111196801010450",
        "mobile":"13918013475",
        "address":"上海市人民路1号101室",
        "phone": "13919191383",
        "emergencyName": "何耀军",
        "emergencyPhone": "13919191385",
        "disableNum":"310111196801010450A1",
        "userType": "normal"
	})

@app.route('/profile', methods=['POST'])
def updateProfile():
	return request.data
	
if __name__ == '__main__':
	app.run()