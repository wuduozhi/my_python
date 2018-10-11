# -*- coding:utf-8 -*-
import requests
import sys
from requests.adapters import HTTPAdapter
import re
import json
from Spider import Spider

class GradeSpider(Spider):
	def __init__(self,config):
		super(GradeSpider,self).__init__(config)
		super(GradeSpider,self).login()


	def query(self):
		queryUrl = self.config['queryUrl']
		data = {
			"xsfscode":"",
			"jczy013id":"",
			"page":{
				"pageIndex":1,
				"pageSize":20,
				"orderBy":"[{\"field\":\"cjgl016id\",\"sortType\":\"asc\"}]",
				"conditions":"{\"conditionGroup\":[{\"link\":\"and\",\"condition\":[]}]}"
			}
		}

		headers = {
			'Accept': 'text/html, application/xhtml+xml, */*',
			'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
			'Content-Type': 'application/json;charset=UTF-8',
			'Accept-Encoding': 'gzip, deflate',
			'Origin': 'http://hdjw.hnu.edu.cn',
			'Referer': 'http://hdjw.hnu.edu.cn/Njw2017/index.html',
			'Connection': 'Keep-Alive',
			'Pragma': 'no-cache'
		}

		page = self.s.post(url,data = json.dumps(data), headers = headers, timeout = 3).text

		return page

if __name__ == '__main__':
	config = {
		'stuid':'201626010520',
		'password':'WudUozhI',
		'loginUrl':'http://hdjw.hnu.edu.cn/sys/sign/login',
		'queryUrl':'http://hdjw.hnu.edu.cn/resService/jwxtpt/v1/xsd/cjgl_xsxdsq/findKccjList?resourceCode=XSMH0507&apiCode=jw.xsd.xsdInfo.controller.CjglKccjckController.findKccjList'
	}
	spider = GradeSpider(config)
	# spider.login()
	# cookies = spider.getCookie()
	grade = spider.query()
	print grade