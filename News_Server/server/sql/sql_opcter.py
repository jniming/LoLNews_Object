# -*- coding:utf-8 -*-
import json
import pymysql
import time


class SqlOpcter(object):
	def __init__(self):
		self.db=None

	def _connect(self):
		self.db = pymysql.connect(user='root', passwd='root',
		                          host='127.0.0.1', db='test',
		                          charset='utf8')  # 链接数据库
		adb = self.db.cursor()
		adb.execute('SET NAMES utf8;')
		adb.execute('SET CHARACTER SET utf8;')
		adb.execute('SET character_set_connection=utf8;')
		adb.close()
	def get_news_list(self,start,end):
		cur_ = self.db.cursor()
		sql = "select * from _news order BY  mNewsTime DESC limit  %s,%s " % (start,end)
		print(sql)
		print(cur_)
		cur_.execute(sql)

		_list = cur_.fetchall()
		print(_list)
		_news_ = []
		for n in _list:
			_stu = self.get_news_dir(n)
			_news_.append(_stu)
		json_list = json.dumps(_news_)  # 键值对转为json
		print(json_list)
		cur_.close()
		return json_list

	def query_news_info(self, nid):
		cur_ = self.db.cursor()
		sql="select * from _news WHERE mNewsId=%s" %(nid)
		cur_.execute(sql)
		news = cur_.fetchone()
		news_dir = self.get_news_dir(news)
		cur_.close()
		return news_dir

	def get_news_dir(self, news):
		news_dir = dict()
		news_dir['mNewsTitle'] = news[1]
		news_dir['mNewsImgUri'] = news[3]
		news_dir['mNewsTime'] = news[2].strftime("%Y-%m-%d")
		news_dir['mNewsId'] = news[0]
		print(news[2].strftime("%Y-%m-%d"))

		return news_dir