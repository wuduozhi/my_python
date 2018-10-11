# -*- coding:utf-8 -*-
import requests
import sys
from requests.adapters import HTTPAdapter
import re

class GymosSpider:
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
		    "student_num":stuid,
		    "password":password,
		}

		headers = {
			'Accept': 'text/html, application/xhtml+xml, */*',
			'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept-Encoding': 'gzip, deflate',
			'Referer': 'http://gymos.hnu.edu.cn/bdlp_api_fitness_test_student_h5/view/login/loginPage.html',
			'Connection': 'Keep-Alive',
			'Pragma': 'no-cache'
		}
		page = self.s.post(url,data = postdict, headers = headers, timeout = 3)

	def query(self,xn=None):
		url=self.config['queryUrl']
		postdict = {
		    "year_num":xn
		}

		headers = {
			'Accept': 'text/html, application/xhtml+xml, */*',
			'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept-Encoding': 'gzip, deflate',
			'Referer': 'http://gymos.hnu.edu.cn/bdlp_api_fitness_test_student_h5/view/login/loginPage.html',
			'Connection': 'Keep-Alive',
			'Pragma': 'no-cache'
		}
		page = self.s.post(url,data = postdict, headers = headers, timeout = 3).text
		print page

	def getCookie(self):
		'''
		返回cookie 字典格式
		'''
		return requests.utils.dict_from_cookiejar(self.s.cookies)

if __name__ == '__main__':
	config = {
		'stuid':'201626010520',
		'password':'WudUozhI',
		'loginUrl':'http://gymos.hnu.edu.cn/bdlp_api_fitness_test_student_h5/public/index.php/index/Login/login',
		'queryUrl':'http://gymos.hnu.edu.cn/bdlp_api_fitness_test_student_h5/public/index.php/index/Report/getStudentScore'
	}
	spider = GymosSpider(config)
	spider.login()
	cookies = spider.getCookie()
	# print cookies
	spider.query('2017')