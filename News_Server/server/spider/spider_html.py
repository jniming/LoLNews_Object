# -*- coding:utf-8 -*-
import urllib.request
from hmac import new

import bs4
import pymysql
import time

from server.sql import gl


class SpiderHtml(object):



	def __init__(self):
		self.fname_prefix = "fn"
		self.__user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

	def _load_news_detail_html(self,url):
		req=urllib.request.Request(url)
		req.add_header('User-Agent', self.__user_agent)
		reqsp=urllib.request.urlopen(req)
		content=reqsp.read()
		return content.decode("utf-8")

	def get_news(self,nid,type):
		news = gl.sql_con.query_news_info(nid, type)
		news_url=news["mNewsImgUri"]
		print(news_url)
		find_index=news_url.find('banben')  #查询是否包含版本字段
		print(find_index)
		if find_index >0:   # 包含
			return  self._get_news_body_type_two(news)
		else:
			return self._get_news_body(news)





	def _get_news_body(self,news):
		_body=self._load_news_detail_html(news["mNewsImgUri"])
		if _body is None:
			return None
		soup = bs4.BeautifulSoup(_body, "html.parser")
		msg_info = soup.find('div', class_='gb-final-mod-article')
		h3_str=msg_info.findAll("h3")
		len(h3_str)
		dete_h3=None
		if len(h3_str) is not 0:
			dete_h3 = h3_str[len(h3_str)-1]
		div_body=msg_info.findAll('div')
		msg_time = "<h5 style='text-align: center;font-size: 12px'>发布时间:" + news["mNewsTime"] + "</h5>"
		title="<h2 style='text-align: center;'>"+news["mNewsTitle"]+msg_time+"</h2><hr style='height:1px;border:none;border-top:1px solid #888'></hr>"
		# title['style'] = 'text-align: center;font-size: 10px'
		body_html = "<body style='max-width:100%;height:auto;'>" + str(title) + str(msg_info) + "</body>"
		ass_style = "<style>img{max-width:100%;height:auto;}</style>"
		html = "<html><head>" + ass_style + "</head>" + body_html + "</html>"
		print(html)
		html=html.replace(str(div_body[1]),"",1)
		print(html)

		# _index=html.index(str(div_body[1]))
		# retain_html=html[:_index]
		# print(str(div_body[1]))
		# end_html=html[_index+len(str(div_body[1])):]
		# print(end_html)
		# retain_html+=end_html



		# if dete_h3 is not None:
		# 	h3_index=html.index(str(dete_h3))
		# 	print(h3_index)
		# 	html=html[:h3_index]
		return str(html)     #返回字符串,注意要用str()格式化html代码


	def _get_news_body_type_two(self,news):
		_body = self._load_news_detail_html(news["mNewsImgUri"])
		if _body is None:
			return None
		soup = bs4.BeautifulSoup(_body, "html.parser")

		msg_info = soup.find('div', class_='content')
		msg_time = "<h5 style='text-align: center;font-size: 12px'>发布时间:" + news["mNewsTime"] + "</h5>"
		title = "<h2 style='text-align: center;'>" + news[
			"mNewsTitle"] + msg_time + "</h2><hr style='height:1px;border:none;border-top:1px solid #888'></hr>"
		# title['style'] = 'text-align: center;font-size: 10px'
		body_html = "<body style='max-width:100%;height:auto;'>" + str(title) + str(msg_info) + "</body>"
		# ass_style = "<style>img{max-width:100%;height:auto;}</style>"
		ass_style = "<meta name='viewport' content='width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no' />"
		html = "<html><head>" + ass_style + "</head>" + body_html + "</html>"

		return str(html)  # 返回字符串,注意要用str()格式化html代码













