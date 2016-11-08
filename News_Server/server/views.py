import json

from django.http import HttpResponse

# Create your views here.
from server.spider.spider_html import SpiderHtml
from server.sql import gl
from server.sql.sql_opcter import SqlOpcter


def getNewsList(request,start,type):   #必须默认带request参数,否者无法访问\
	# _num=request.GET.get('num')
	print(type)
	newsList=gl.sql_con.get_news_list(type,start,20)
	return HttpResponse(newsList)
def getMeetNewsList(request,start,type):   #必须默认带request参数,否者无法访问\
	# _num=request.GET.get('num')
	print(type)
	newsList=gl.sql_con.get_meet_news_list(type,start,20)
	return HttpResponse(newsList)
def getNewsDetail(request,nid,type):
	spider=SpiderHtml()
	_newsDetail=spider.get_news(nid,type)
	str=dict()
	str["mHtmlCode"]=_newsDetail
	body_=json.dumps(str)
	print(body_)
	return HttpResponse(body_)
def index(request):
	return HttpResponse('hello fuck')
def getManUrlList(request):
	data = gl.sql_con.get_Man_Data()  # 周免数据
	inner_data=gl.sql_con.getInnerList() #获取广告轮播数据
	sys_data=gl.sql_con.getSysNewsList() #获取系统公告
	_list = dict()
	_list['mManList']=data
	_list['mInnerList']=inner_data
	_list['mSysList'] = sys_data
	print(_list)
	json_list = json.dumps(_list)  # 键值对转为json
	return HttpResponse(json_list)

