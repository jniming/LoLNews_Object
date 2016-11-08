from django.conf.urls import url

from . import views

# 绑定服务器访问地址指向的页面,这里我们执行view中index函数中的内容
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getNewsDetail/(\w+)/([0-9]+)/$', views.getNewsDetail, name='getNewsDetail'),
	url(r'^getNewsList/([0-9]+)/([0-9]+)/$', views.getNewsList,name='getNewsList'),
	url(r'^getMeetNewsList/([0-9]+)/([0-9]+)/$', views.getMeetNewsList,name='getMeetNewsList'),
	url(r'^getManUrlList/', views.getManUrlList,name='getManUrlList'),

]