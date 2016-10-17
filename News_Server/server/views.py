import json

from django.http import HttpResponse

# Create your views here.
from server.spider.spider_html import SpiderHtml
from server.sql import gl
from server.sql.sql_opcter import SqlOpcter


def getNewsList(request,start):   #必须默认带request参数,否者无法访问\
	# _num=request.GET.get('num')
	newsList=gl.sql_con.get_news_list(start,20)
	return HttpResponse(newsList)
def getNewsDetail(request,nid):
	print(nid)
	spider=SpiderHtml()
	_newsDetail=spider.get_news_body(nid)
	print(_newsDetail)
	str=dict()
	str["mHtmlCode"]=_newsDetail
	body_=json.dumps(str)
	return HttpResponse(body_)
def index(request):
	return HttpResponse('hello fuck')