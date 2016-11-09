import time
import _gl
from spider.news_spider import NewsSpider
from spider.video_spider import VideoSpider
from util import table_name
from util.sql_operator import SqlOperator



def task():

	_gl.sql_oper = SqlOperator()
	_gl.sql_oper.Sconnect()

    #--------------------获取主页内容_____________________#
	spider3 = NewsSpider()
	spider3.getManHtml()  #获取周免英雄
	spider3.getInnerHtml()   #获取benner
	spider3.getSysNewsHtml()  #获取系统公告
	v_spider=VideoSpider()
	# --------------------获取新闻内容_____________________#
	for _type in table_name.news_table:
		spider3.grap_news(_type)

    # --------------------获取攻略内容内容_____________________#
	for _type in table_name.meet_table:
		spider3.grap_news(_type)

	for _type in table_name.video_table:
		v_spider.grap_video(_type)









while True:
	task()
	time.sleep(10)
