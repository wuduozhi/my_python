#coding=utf-8
#-*-coding:utf-8-*-
#!/usr/bin/env python3
from flask import Flask, request, redirect
import requests
import json
import os
import time

path = os.path.abspath('.')
TOKEN_DIR = os.path.join(path, "access_token.json")
BASE_URL = "https://openapi.yiban.cn/"



def get_mc():
    try:
        with open(TOKEN_DIR) as f: return f.read()
    except:
        with open(TOKEN_DIR, 'w') as f: return

def set_mc(j):
    with open(TOKEN_DIR, 'w') as f: return f.write(j)

class AccessToken(object):
    def __init__(self, code):
        # self.AppID= Config.AppID
        # self.AppSecret = Config.AppSecret
        # self.Redirect_uri = Config.Redirect_uri
       	# self.__state = Config.STATE

		self.AppID = "5b4dbdd7117a710c"
		self.AppSecret = "f9e1877e3c358447877d777d0d9924d3"
		self.Redirect_uri = "http://qnxg.net/ticket/api/yiban"
		self.__state = 'query'


		self.code = code

		__url = BASE_URL + "oauth/authorize?client_id=%s&redirect_uri=%s&state=%s"
		self.init_url = __url % (self.AppID, self.Redirect_uri, self.__state)

		#current user token
		self.__access_token = None
		self.__user_id = None
		self.__end_time = 0

    def _load_file_token(self):
        mc = get_mc()
        if(mc and self.__user_id):
            file_dict = json.loads(mc)
            user_dict = file_dict[self.__user_id]

            #int type
            end_time = int(user_dict["expires"])
            token = user_dict["access_token"]
            #reset
            if(end_time < time.time()):
                self._dump_file_token()
                return self._load_file_token()
            return token, end_time

        else:
            self._dump_file_token()
            return self._load_file_token()

    def _dump_file_token(self):
        url = BASE_URL + "oauth/access_token"
        
        data = {
                "client_id": self.AppID,
                "client_secret": self.AppSecret, 
                "code": self.code, 
                "redirect_uri":self.Redirect_uri
                }
        ctn = json.loads(requests.post(url, data).text)
        self.__user_id = ctn["userid"]
        
        mc = get_mc()
        if(mc):
            file_dict = json.loads(mc)
        else:
            file_dict = {}

        file_dict[self.__user_id] = ctn
        set_mc(json.dumps(file_dict))

    def set_token(self):
        self.__access_token, self.__end_time = self._load_file_token()

    def get_token(self):
        if(self.__end_time < time.time()):
            self.set_token()
        return self.__access_token

    def access_by_token(self, procd, *args, **kwargs):
        def f(*args, **kwargs):
            res = procd(access_token=self.get_token(), **kwargs)
            return res
        return f


class ApiError(AttributeError):
    def __init__(self, attr):
        self.message = "api has no attribute '%s'"%'.'.join(attr)
        self.args = (self.message,)


class ApiFramework(object):

    def __init__(self, attr=[], warning=False):

        self.attr = attr
        self.warning = warning

    def __getattr__(self, s):
        if(self.warning): raise ApiError(self.attr)
        af = ApiFramework(self.attr+[s], warning=self.warning)
        return af

    def __call__(self, *args, **kwargs):
        
        path = self.attr[0:-1]
        method = self.attr[-1]
        url = BASE_URL + "/".join(path)
        res_ctn =None
        if(method == "get"):
            res_ctn = requests.get(url, params=kwargs).text
        elif(method == "post"):
            res_ctn = requests.post(url, data=kwargs).text
        else:
            raise ApiError(self.attr)
        return res_ctn

class Config(object):

	AppID = "5b4dbdd7117a710c"
	AppSecret = "f9e1877e3c358447877d777d0d9924d3"
	Redirect_uri = "http://qnxg.net/ticket/api/yiban"
	STATE = "query"

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello World'

@app.route('/token')
def access_token():
    at = AccessToken(code=None)
    return redirect(at.init_url)



@app.route('/redirect')
def user_info():
    
    #获取令牌code
    __code = request.args.get("code")

    #利用code 和 Config 实例化AccessToken
    at = AccessToken(code=__code)

    #开始使用装饰器@at.access_by_token 和api定义自己的函数
    @at.access_by_token
    def user_me(access_token):
    	return api.user.me.get(access_token=access_token)

    return user_me()

if __name__ == '__main__':
	app.run()