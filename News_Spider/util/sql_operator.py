# -*- coding:utf-8 -*-

import pymysql

from util import table_name


class SqlOperator(object):
	def _init_(self):
		self.db = None
		pass

	def Sconnect(self):
		print("数据库连接")
		try:
			# self.db = pymysql.connect(user='allen_test', passwd='123456',
			#                           host='180.76.175.209', db='spinder_test',
			#                           charset='utf8')  # 链接数据库
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
		new_table_list = table_name.news_table
		for table in new_table_list:
			sql = """create table if not exists %s(
            mNewsId int auto_increment,
            mNewsTitle varchar(128),
            mNewsTime TIMESTAMP ,
            mNewsImgUri varchar(128),
            primary key (mNewsId))""" % (table)
			cursor.execute(sql)

		table_man=table_name.main_table[0]   #周免英雄表
		sql = """create table if not exists %s(
		            mManId int auto_increment,
		            mManImgUrl varchar(128),
		            primary key (mManId))""" % (table_man)
		cursor.execute(sql)

		inner_table=table_name.main_table[1]   # 广告轮播表
		inner_sql="""create table if not exists %s(
		            mInnerId int auto_increment,
		            mImgUrl varchar(128),
		            mLinkUrl varchar(128),
		            primary key (mInnerId))""" % (inner_table)
		cursor.execute(inner_sql)

		sys_table= table_name.main_table[2]   # 系统公告
		sys_sql="""create table if not exists %s(
		            mSysId int auto_increment,
		            mSysTitle varchar(128),
		            mSysLink varchar(128),
		            mSysTime TIMESTAMP,
		            primary key (mSysId))""" % (sys_table)
		cursor.execute(sys_sql)
		meet_table_list=table_name.meet_table
		for _table in  meet_table_list:
			sql = """create table if not exists %s(
			            mNewsId int auto_increment,
			            mNewsTitle varchar(128),
			            mNewsTime TIMESTAMP ,
			            mNewsImgUri varchar(128),
			            primary key (mNewsId))""" % (_table)
			cursor.execute(sql)


		for _table in  table_name.video_table:   #视频表
			sql = """create table if not exists %s(
			            v_id int auto_increment,
			            v_title varchar(128),
			            v_time TIMESTAMP ,
			            v_img_url varchar(128),
			            v_content_url varchar(128),
			            v_author varchar(50),
			            primary key (v_id))""" % (_table)
			cursor.execute(sql)

		cursor.close()

	def insert_news_in_table(self, news_type, item):  # 新闻表信息插入
		table = self._get_news_by_type(news_type)
		_cur = self.db.cursor()
		_str = pymysql.escape_string(item['title'])  # 格式化改字符串,
		_url = pymysql.escape_string(item['url'])  # 格式化改字符串,
		sql = "insert into %s(mNewsTitle,mNewsImgUri,mNewsTime) values ('%s','%s','%s')" % (table, _str, _url,str(item['time']) )
		_cur.execute(sql)
		self.db.commit()
		_cur.close()

	def insert_video_in_table(self, news_type, item):  # 视频表信息插入
		table = self._get_video_by_type(news_type)
		_cur = self.db.cursor()
		sql = "insert into %s(v_title,v_time,v_img_url,v_content_url,v_author) values ('%s','%s','%s','%s','%s')" % (table, item['v_title'], item['v_time'],item['v_img_url'],item['v_content_url'],item['v_author'])
		_cur.execute(sql)
		self.db.commit()
		_cur.close()

	def _get_news_by_type(self, news_type):
		table = None
		if news_type == table_name.news_table[0]:
			table = table_name.news_table[0]
		if news_type == table_name.news_table[1]:
			table = table_name.news_table[1]
		if news_type == table_name.news_table[2]:
			table = table_name.news_table[2]
		if news_type == table_name.meet_table[0]:
			table = table_name.meet_table[0]
		if news_type == table_name.meet_table[1]:
			table = table_name.meet_table[1]
		return table
	def _get_video_by_type(self, news_type):
		table = None
		if news_type == table_name.video_table[0]:
			table = table_name.video_table[0]
		if news_type == table_name.video_table[1]:
			table = table_name.video_table[1]
		if news_type == table_name.video_table[2]:
			table = table_name.video_table[2]
		if news_type == table_name.video_table[3]:
			table = table_name.video_table[3]
		return table

	def is_news_exist(self, news_type, url):
		table = self._get_news_by_type(news_type)
		_url = pymysql.escape_string(url)  # 格式化改字符串
		sql = "select * from %s where mNewsImgUri='%s' " % (table, _url)
		cur = self.db.cursor()
		cur.execute(sql)
		_is_ex_news = cur.fetchone()  # 判断数据是否存在
		cur.close()
		return _is_ex_news is not None

	def is_video_exist(self, video_type, url):
		table = self._get_video_by_type(video_type)
		_url = pymysql.escape_string(url)  # 格式化改字符串
		sql = "select * from %s where v_content_url='%s' " % (table, _url)
		cur = self.db.cursor()
		cur.execute(sql)
		_is_ex_news = cur.fetchone()  # 判断数据是否存在
		cur.close()
		return _is_ex_news is not None






	def insert_man_img(self,url):   # 免费英雄数据
		sql = "insert into %s (mManImgUrl) values ('%s')" % (table_name.main_table[0],url)
		cur = self.db.cursor()
		cur.execute(sql)
		self.db.commit()
		cur.close()
	def dete_man_table(self):
		sql="DELETE FROM %s" %(table_name.main_table[0])
		cur = self.db.cursor()
		cur.execute(sql)
		self.db.commit()
		cur.close()

	def insert_Inner_url(self,item):
		sql = "insert into %s (mImgUrl,mLinkUrl) values ('%s','%s')" % (table_name.main_table[1],item['mImgUrl'],item['mLinkUrl'])
		cur = self.db.cursor()
		cur.execute(sql)
		self.db.commit()
		cur.close()
	def insert_SysNews_url(self,item):
		is_exit=self._query_sysNews_isexit(item['mSysLink'])
		if is_exit is False:
			sql = "insert into %s (mSysTitle,mSysLink,mSysTime) values ('%s','%s','%s')" % (table_name.main_table[2],
			item['mSysTitle'], item['mSysLink'], item['mSysTime'])
			cur = self.db.cursor()
			cur.execute(sql)
			self.db.commit()
			cur.close()



	def _query_sysNews_isexit(self,url):
		sql = "select * from %s where mSysLink='%s' " % (table_name.main_table[2], url)
		cur = self.db.cursor()
		cur.execute(sql)
		_is_ex_news = cur.fetchone()  # 判断数据是否存在
		cur.close()
		return _is_ex_news is not None


	def dete_inner_table(self):
		sql="DELETE FROM %s" % (table_name.main_table[1])
		cur = self.db.cursor()
		cur.execute(sql)
		self.db.commit()
		cur.close()






