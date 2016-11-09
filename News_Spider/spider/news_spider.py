# -*- ecoding:utf-8 -*-
import random
import time
import urllib.request
import bs4

import _gl
from util import grap_uri
from util import table_name


class NewsSpider(object):
	def _init_(self):

		pass

	def _load_html(self, uri):
		try:
			req = urllib.request.Request(uri)
			resp = urllib.request.urlopen(req)
			content = resp.read().decode('utf-8', 'ignore').encode('utf-8')  # 对网页进行解码,再进行编码,防止出现中文乱码
			return content
		except:
			# time.sleep(random.randint(10, 15))
			return None

	def parse_data(self, uri, news_type):
		_continue = True
		content = self._load_html(uri)
		while content is None:
			return None
		soup = bs4.BeautifulSoup(content, "html.parser")
		try:
			ul = soup.find('ul', class_='comm-list art-list-txt js-list1')
			_news_a = ul.findAll('div', class_='tit')
			item = dict()  # dict() 类似于java中的list
			for a in _news_a:
				h_time = a.find('span', class_='time');
				if h_time is not None:
					news_time = h_time.string
					item['time'] = self.getTime(news_time)
				title_h = a.find('a', class_='c-black')
				if title_h is not None:
					news_uri = title_h['href']
					news_title = title_h.string  # .string 获取标签内的内容
					uri_inde=str(news_uri).find('lol.17173.com')
					if uri_inde is -1:
						return None

					item['url'] = news_uri
					item['title'] = news_title
				# 下面进行数据实体化
				if _gl.sql_oper.is_news_exist(news_type, item['url']) is False:
					_gl.sql_oper.insert_news_in_table(news_type, item)

		except:
			return None

		return _continue

	def grap_news(self, news_type):
		def get_uri(news_type):  # 获取爬取得网站   ['_now_news', '_system_news', '_yule_news']
			url = None
			if news_type == table_name.news_table[0]:
				url = grap_uri.news_uri
			if news_type == table_name.news_table[1]:
				url = grap_uri.sysupdate_uri
			if news_type == table_name.news_table[2]:
				url = grap_uri.recreation_uri
			if news_type == table_name.meet_table[0]:
				url = grap_uri.inter_meet_url
			if news_type == table_name.meet_table[1]:
				url = grap_uri.system_meet_url
			return url

		news_url = get_uri(news_type);
		while True:
			should_counin = self.parse_data(news_url, news_type)

			news_url = self._get_next_page_url(news_url)
			if should_counin is None:
				return None
			else:
				if should_counin is False or news_url is None:
					continue


	def _get_next_page_url(self,url):
		#http://lol.17173.com/banben/list/index_1.shtml
		fromt_url=str(url)
		_url_=None
		url_start_str=''
		url_array=fromt_url.split('/')
		end_str=url_array[len(url_array)-1]
		nPos=end_str.find("_")
		for ay in url_array:
			if ay.find(end_str) ==-1:
				url_start_str = url_start_str + ay + '/'



		if nPos < 0:   #不包含,说明为首页
			end_str_array=end_str.split('.')
			step_str=end_str_array[0]  #标志字符串
			_url_=url_start_str+step_str+"_1."+end_str_array[1]
		else:   #包含,说明不是第一页
			end_str_array = end_str.split('.')
			step_str_array = end_str_array[0].split('_')
			index_str=step_str_array[1]
			index_int=int(str(index_str))
			next_page_int=index_int+1;
			_url_=url_start_str+step_str_array[0]+'_'+str(next_page_int)+"."+end_str_array[1]
		return _url_





	def getTime(self, date):
		ye = time.strftime('%Y')
		format_time = str(ye) + '-' + str(date)
		return format_time

	def getManHtml(self):  # 获取周免英雄
		# _gl.sql_oper.dete_man_table()
		content = self._load_html(grap_uri.super_man)
		while content is None:
			return None
		soup = bs4.BeautifulSoup(content, "html.parser")
		hero_group = soup.findAll('div', class_='hero-group')
		_gl.sql_oper.dete_man_table()
		li = hero_group[len(hero_group) - 1].findAll('li')
		for man in li:
			img_html = man.find('img')
			man_url_html = img_html['src']
			_gl.sql_oper.insert_man_img(str(man_url_html))

	def getInnerHtml(self):  # 获取广告资源

		content = self._load_html(grap_uri.inner_url)
		while content is None:
			return None
		soup = bs4.BeautifulSoup(content, "html.parser")
		hero_group = soup.findAll('div', class_='focus-item')
		_gl.sql_oper.dete_inner_table()
		item = dict()
		for inner in hero_group:
			a_html = inner.find('a')
			link_url = a_html['href']
			img_html = inner.find('img')
			img_url = img_html['src']
			item['mImgUrl'] = str(img_url)
			item['mLinkUrl'] = str(link_url)
			_gl.sql_oper.insert_Inner_url(item)

	def getSysNewsHtml(self):  # 获取系统公告资源
		content=None;
		try:
			req = urllib.request.Request(grap_uri.sysNews_url)
			resp = urllib.request.urlopen(req)
			content = resp.read().decode('gb2312', 'ignore').encode('utf-8')  # 对网页进行解码,再进行编码,防止出现中文乱码
		except:
			return None
		# content = self._load_html(grap_uri.sysNews_url)
		# co=content.decode('utf-8', 'ignore')
		while content is None:
			return None
		soup = bs4.BeautifulSoup(content, "html.parser")
		hero_group = soup.find('ul', class_='newslistbox')
		_li_html = hero_group.findAll('li', class_="news-lst")
		item = dict()
		for li in _li_html:
			a_html = li.find('a',target="_blank")
			sys_news_title=a_html.string
			# sy=sys_news_title.decode('gb2312')
			sys_time_html = li.find('span', class_="date")
			sys_time = sys_time_html.string
			sys_link = a_html['href']
			item['mSysTime'] = str(sys_time)
			item['mSysLink'] = str(sys_link)
			item['mSysTitle'] = str(sys_news_title)
			_gl.sql_oper.insert_SysNews_url(item)
