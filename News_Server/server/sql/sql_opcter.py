# -*- coding:utf-8 -*-
import json
import pymysql
import time

from server.sql import table_name


class SqlOpcter(object):
	def __init__(self):
		self.db=None

	def _connect(self):
		# self.db = pymysql.connect(user='allen_test', passwd='123456',
		#                           host='180.76.175.209', db='spinder_test',
		#                           charset='utf8')  # 链接数据库
		self.db = pymysql.connect(user='root', passwd='root',
		                          host='127.0.0.1', db='test',
		                          charset='utf8')  # 链接数据库
		adb = self.db.cursor()
		adb.execute('SET NAMES utf8;')
		adb.execute('SET CHARACTER SET utf8;')
		adb.execute('SET character_set_connection=utf8;')
		adb.close()


	def get_news_list(self,type,start,end):
		table=self._get_news_type_table(type)
		print(table)
		cur_ = self.db.cursor()
		sql = "select * from %s order BY  mNewsTime DESC limit  %s,%s " % (table,start,end)
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

	def get_meet_news_list(self,type,start,end):
		table=self._get_meet_news_type_table(type)
		print(table)
		cur_ = self.db.cursor()
		sql = "select * from %s order BY  mNewsTime DESC limit  %s,%s " % (table,start,end)
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
	def _get_meet_news_type_table(self,type):
		ty=int(type)
		if ty==0:   #综合攻略
			return table_name.meet_table[0]
		if ty==1:  #版本攻略
			return table_name.meet_table[1]

		return None
	def _get_news_type_table(self,type):
		ty=int(type)
		if ty==0:   #电竞新闻
			return table_name.news_table[0]
		if ty==1:  #娱乐八卦
			return table_name.news_table[2]
		if ty==2:  #版本动态
			return table_name.news_table[1]
		if ty==3:  #综合攻略2
			return table_name.meet_table[0]
		if ty==4:  #版本动态
			return table_name.meet_table[1]
		return None


	def query_news_info(self, nid,type):
		table=self._get_news_type_table(type)
		cur_ = self.db.cursor()
		sql="select * from %s WHERE mNewsId=%s" %(table,nid)
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
	def get_Man_Data(self):  # 获取周免数据
		cur_ = self.db.cursor()
		sql = "select * from %s" %(table_name.main_table[0])
		print(sql)
		cur_.execute(sql)
		mans = cur_.fetchall()
		print(mans)
		_man = []
		for man in mans:
			_manBean = dict()
			_manBean['mManUrlId']=man[0]
			_manBean['mManUrl'] = man[1]
			_man.append(_manBean)
		cur_.close()
		return _man
	def getInnerList(self):   #获取广告轮播数据
		cur_ = self.db.cursor()
		sql = "select * from  %s" %(table_name.main_table[1])
		cur_.execute(sql)
		mans = cur_.fetchall()
		_man = []
		for man in mans:
			_manBean = dict()
			_manBean['mInnerId'] = man[0]
			_manBean['mImgUrl'] = man[1]
			_manBean['mLinkUrl'] = man[2]
			_man.append(_manBean)
		cur_.close()
		return _man

	def getSysNewsList(self):   #获取系统公告数据
		cur_ = self.db.cursor()
		sql = "select * from %s order BY  mSysTime DESC limit 10" %(table_name.main_table[2])
		cur_.execute(sql)
		mans = cur_.fetchall()
		_man = []
		for man in mans:
			_manBean = dict()
			_manBean['mSysId'] = man[0]
			_manBean['mSysTitle'] = man[1]
			_manBean['mSysLink'] = man[2]
			_manBean['mSysTime'] = man[3].strftime("%m-%d")
			_man.append(_manBean)
		cur_.close()
		return _man
