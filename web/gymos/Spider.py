# -*- coding:utf-8 -*-
import requests
import sys
from requests.adapters import HTTPAdapter
import re
import json

class Spider:
	def __init__(self,config):
		self.s=requests.session()
		self.config=config
		self.s.mount('http://',HTTPAdapter(max_retries=3))
		self.s.mount('https://',HTTPAdapter(max_retries=3))

	def login(self):
		url=self.config['loginUrl']
		stuid=self.config['stuid']
		password=self.config['password']
		
		postdict = {
		    "userCode":stuid,
		    "password":password,
		    "kaptcha":'testa',
		    "userCodeType":'account'
		}

		headers = {
			'Accept': 'text/html, application/xhtml+xml, */*',
			'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
			'Content-Type': 'application/json',
			'Accept-Encoding': 'gzip, deflate',
			'Referer': 'http://hdjw.hnu.edu.cn/Njw2017/login.html',
			'host':'hdjw.hnu.edu.cn',
			'Connection': 'Keep-Alive',
			'Pragma': 'no-cache'
		}
		page = self.s.post(url,data = json.dumps(postdict), headers = headers, timeout = 3)
		# print page.text

	def query(self):
		url = self.config['queryUrl']
		data = {
		  "xsfscode": "2",
		  "jczy013id": "",
		  "page": {
		    "pageIndex": 1,
		    "pageSize": 40,
		    "orderBy": "[{\"field\":\"cjgl016id\",\"sortType\":\"asc\"}]",
		    "conditions": "{\"conditionGroup\":[{\"link\":\"and\",\"condition\":[]}]}"
		  }
		}

		headers = {
			'Accept': 'application/json, text/plain, */*',
			'app':'PCWEB',  # 需要加这个header,不然不能通过验证
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Content-Type': 'application/json',
			'Accept-Encoding': 'gzip, deflate',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
			'Origin': 'http://hdjw.hnu.edu.cn',
			'Referer': 'http://hdjw.hnu.edu.cn/Njw2017/index.html',
			'Connection': 'Keep-Alive',
			'Pragma': 'no-cache'
		}

		page = self.s.post(url,data = json.dumps(data), headers = headers, timeout = 3).text
		# page = self.s.get(url,headers = headers, timeout = 3).text
		return page

	def getCookie(self):
		'''
		返回cookie 字典格式
		'''
		return requests.utils.dict_from_cookiejar(self.s.cookies)

	def getMapList(self):
		headers={
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Host':'hdjw.hnu.edu.cn',
            'app':"PCWEB",
            'Content-Type':'application/json',
            'locale':'zh_CN',
            'Origin':'http://hdjw.hnu.edu.cn',
            'Referer':'http://hdjw.hnu.edu.cn/Njw2017/index.html',
        }

		url=self.config['listUrl']
		response=self.s.post(url,data='{}',headers=headers)
		data = json.loads(response.text)['data']
		build = []
		for dic in data:
		    tmp = {}
		    tmp['id'] = dic['id']
		    tmp['build'] = dic['name1']
		    build.append(tmp)
		self.list = build
		return build


if __name__ == '__main__':
	config = {
		'stuid':'201626010520',
		'password':'WudUozhI',
		'loginUrl':'http://hdjw.hnu.edu.cn/sys/sign/login',
		'queryUrl':'http://hdjw.hnu.edu.cn/resService/jwxtpt/v1/xsd/cjgl_xsxdsq/findKccjList?resourceCode=XSMH0507&apiCode=jw.xsd.xsdInfo.controller.CjglKccjckController.findKccjList',
		# 'queryUrl':'http://hdjw.hnu.edu.cn/sys/sign/assert.json?resourceCode=resourceCode&apiCode=framework.sign.controller.SignController.asserts',
		'listUrl':'http://hdjw.hnu.edu.cn/resService/jwxtpt/v1/xsd/xsdkxjsck/findJxlList?resourceCode=XSMH0704&apiCode=jw.xsd.xsdInfo.controller.XsdKxjsckController.findJxlList',
	}
	spider = Spider(config)
	spider.login()
	cookies = spider.getCookie()
	build = spider.getMapList()
	# print build
	# print cookies
	grade = spider.query()
	print grade