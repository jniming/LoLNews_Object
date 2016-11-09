# -*- ecoding:utf-8 -*-
import urllib


import bs4
import time

import _gl
from util import grap_uri
from util import table_name


class VideoSpider(object):
	def _init_(self):
		pass
	def _load_html(self, uri):
		try:
			req = urllib.request.Request(uri)
			resp = urllib.request.urlopen(req)
			content =resp.read().decode('gb2312', 'ignore').encode('utf-8')  # 对网页进行解码,再进行编码,防止出现中文乱码
			return content
		except:
			# time.sleep(random.randint(10, 15))
			return None
	def grap_video(self,type):
		def _get_video_url(news_type):
			url = None
			if news_type == table_name.video_table[0]:
				url = grap_uri.video_link[0]
			if news_type == table_name.video_table[1]:
				url = grap_uri.video_link[1]
			if news_type == table_name.video_table[2]:
				url = grap_uri.video_link[2]
			if news_type == table_name.video_table[3]:
				url = grap_uri.video_link[3]
			return url

		url=_get_video_url(type)
		while True:
			have_data=self.pare_data(url,type)
			url = self._get_next_page_url(url)
			if have_data is False or url is None:
				return
	def pare_data(self,url,type):
		html = self._load_html(url)
		if html is not None:
			try:
				soup = bs4.BeautifulSoup(html, "html.parser")
				video = soup.find('div', class_='page-video')
				footer = soup.find('div', class_='global-footer')
				v_list = video.findAll('div', class_='v-list')  # 所有视频列表
				for v in v_list:
					item = dict()
					v_url_div = v.find('a', class_='v-list-item')
					v_title = str(v_url_div['title'])
					v_content_url = str(v_url_div['href'])  # N内容地址
					tiem_aut = v.find('div', class_='v-meta-entry')
					v_img = v.find('img')
					v_img_url = v_img['src']
					v_url_div = tiem_aut.findAll('span')
					_time = self.getTime(v_url_div[0].string)
					author = str(v_url_div[1].string)
					item['v_title'] = v_title
					item['v_time'] = str(_time)
					item['v_img_url'] = str(v_img_url)
					item['v_content_url'] = v_content_url
					item['v_author'] = author
					bool = _gl.sql_oper.is_video_exist(type, item['v_content_url'])
					if bool is False:
						_gl.sql_oper.insert_video_in_table(type, item)
					else:
						print("数据存在")
			except:
				return False
		else:
			return False

	def getTime(self, date):
		ye = time.strftime('%Y')
		format_time = str(ye) + '-' + str(date)
		print(format_time)
		return format_time


	def _get_next_page_url(self,url):
		#http://lol.17173.com/banben/list/index_1.shtml
		#http://v.17173.com/lol/2016/new/new.shtml
		fromt_url=str(url)
		_url_=None
		url_start_str=''
		url_array=fromt_url.split('/')
		end_str=url_array[len(url_array)-1]
		nPos=end_str.find("_")
		# print(len(end_str and 'z'))
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





