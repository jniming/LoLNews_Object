import time
import _gl
from spider.news_spider import NewsSpider
from util.sql_operator import SqlOperator


def task():
	_gl.sql_oper = SqlOperator()
	_gl.sql_oper.connect()
	spider3 = NewsSpider()
	news_type = ['_news','_sysupdate']
	spider3.getManHtml()
	spider3.getInnerHtml()
	spider3.getSysNewsHtml()
	for _type in news_type:
		spider3.grap_news(_type)


while True:
	task()
	time.sleep(10)
