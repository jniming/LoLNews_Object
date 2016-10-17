# -*- coding:utf-8 -*-
import time
import _gl
from spider.news_spider import NewsSpider
from util.sql_operator import SqlOperator

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(onstart)


def app():
    _gl.sql_oper = SqlOperator()
    _gl.sql_oper.connect()
    spider3 = NewsSpider()
    news_type = ['_news']
    for _type in news_type:
        spider3.grap_news(_type)

def onstart():
    while True:
        app()
        time.sleep(10)


