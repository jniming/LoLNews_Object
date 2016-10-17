# -*- coding:utf-8 -*-

import pymysql
import time


class SqlOperator(object):
	def _init_(self):
		self.db = None
		pass

	def connect(self):
		print("数据库连接")
		try:
			self.db = pymysql.connect(user='root', passwd='root',
			                          host='127.0.0.1', db='test',
			                          charset='utf8')  # 链接数据库
			dbc = self.db.cursor()
			self.db.ping(True)
			dbc.execute('SET NAMES utf8')
			dbc.execute('SET CHARACTER SET utf8;')
			dbc.execute('SET character_set_connection=utf8;')
			self._create_tables()
			print("创建表成功")
			dbc.close()
		except:
			return None

	def _create_tables(self):  # 创建表
		cursor = self.db.cursor()
		new_table_list = ['_news', '_update']
		for table in new_table_list:
			sql = """create table if not exists %s(
            mNewsId int auto_increment,
            mNewsTitle varchar(255),
            mNewsTime TIMESTAMP ,
            mNewsImgUri varchar(255),
            primary key (mNewsId))""" % (table)
			print(sql)
			cursor.execute(sql)
		cursor.close()

	def insert_news_in_table(self, news_type, item):  # 新闻表信息插入
		table = self._get_news_by_type(news_type)
		_cur = self.db.cursor()
		_str = pymysql.escape_string(item['title'])  # 格式化改字符串,
		_url = pymysql.escape_string(item['url'])  # 格式化改字符串,
		sql = "insert into %s(mNewsTitle,mNewsImgUri,mNewsTime) values ('%s','%s','%s')" % (table, _str, _url,str(item['time']) )
		print(sql)
		_cur.execute(sql)
		self.db.commit()
		_cur.close()

	def _get_news_by_type(self, news_type):
		table = None
		if news_type == '_news':
			table = '_news'
		if news_type == '_update':
			table = '_update'
		return table

	def is_news_exist(self, news_type, url):
		table = self._get_news_by_type(news_type)
		_url = pymysql.escape_string(url)  # 格式化改字符串
		sql = "select * from %s where mNewsImgUri='%s' " % (table, _url)
		print(sql)
		cur = self.db.cursor()
		cur.execute(sql)
		_is_ex_news = cur.fetchone()  # 判断数据是否存在
		cur.close()
		return _is_ex_news is not None


