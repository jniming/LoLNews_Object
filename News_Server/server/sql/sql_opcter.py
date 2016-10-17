# -*- coding:utf-8 -*-
import json
import pymysql
class SqlOpcter(object):
	def __init__(self):
		self.db=None

	def _connect(self):
		self.db = pymysql.connect(user='allen_test', passwd='123456',
		                          host='180.76.175.209', db='spinder_test',
		                          charset='utf8')  # 链接数据库
		adb = self.db.cursor()
		adb.execute('SET NAMES utf8;')
		adb.execute('SET CHARACTER SET utf8;')
		adb.execute('SET character_set_connection=utf8;')
		adb.close()
	def get_news_list(self,num):
		cur_ = self.db.cursor()
		sql = "select * from _news limit %s" % (num)
		print(sql)
		print(cur_)
		cur_.execute(sql)

		_list = cur_.fetchall()
		_news_ = []
		for n in _list:
			_stu = self.get_news_dir(n)
			_news_.append(_stu)
		json_list = json.dumps(_news_)  # 键值对转为json
		print(json_list)
		cur_.close()
		# try:
		#
		# except:
		# 	return "adb"


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
		# (44L, u'6.20\u4e00\u4e2a\u5927\u62db\u6bc1\u5929\u706d\u5730 \u4e0a\u5355\u4e0d\u9009\u4ed6\u5c31ban', u'10-12', u'http://lol.17173.com/news/10122016/142638448.shtml')
		news_dir['mNewsTitle'] = news[1]
		news_dir['mNewsImgUri'] = news[3]
		news_dir['mNewsTime'] = news[2]
		news_dir['mNewsId'] = news[0]

		return news_dir