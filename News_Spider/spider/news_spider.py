# -*- ecoding:utf-8 -*-
import random
import time
import urllib.request
import bs4

import _gl
from util import grap_uri


class NewsSpider(object):
    def _init_(self):
        pass

    def _load_html(self, uri):
        try:
            req = urllib.request.Request(uri)
            resp = urllib.request.urlopen(req)
            content = resp.read().decode('utf-8', 'ignore').encode('utf-8')  # 对网页进行解码,再进行编码,防止出现中文乱码
            return content.decode('utf-8')
        except:
            time.sleep(random.randint(10, 15))
            return None

    def parse_data(self, uri, news_type):
        print("开始解析网页")
        _continue = True
        content = self._load_html(uri)
        while content is None :
            return None
        soup = bs4.BeautifulSoup(content, "html.parser")
        ul = soup.find('ul', class_='comm-list art-list-txt js-list1')
        _news_a = ul.findAll('div', class_='tit')
        item = dict()  # dict() 类似于java中的list
        for a in _news_a:
            h_time = a.find('span', class_='time');
            if h_time is not None:
                news_time = h_time.string
                item['time'] = news_time
            title_h = a.find('a', class_='c-black')
            if title_h is not None:
                news_uri = title_h['href']
                news_title = title_h.string
                item['url'] = news_uri
                item['title'] = news_title
                # 下面进行数据实体化
            if _gl.sql_oper.is_news_exist(news_type, item['url']) is False:
                print("数据不存在")
                _gl.sql_oper.insert_news_in_table(news_type, item)
            else:
                print("数据存在")
                _continue = False
                break

        return _continue

    # def _getnews_and_uri(self,news_a):

    #     return date,tite


    def grap_news(self, news_type):
        def get_uri(news_type):  # 获取爬取得网站
            url = None
            if news_type == '_news':
                url = grap_uri.news_uri
            if news_type == '_update':
                url = ''
            return url;

        news_url = get_uri(news_type);
        while True:
            should_counin = self.parse_data(news_url, news_type)
            print('本页--'+news_url)
            news_url = self.get_next_page_uri(news_url)
            print('下一页--'+news_url)
            if should_counin is None:
                return None
            else:
                if should_counin is False or news_url is None:
                    continue


    def get_next_page_uri(self, url):
        _index = url.find('zixun')
        print(_index)
        _pos_str = url[_index:]
        _auto_str = url[:_index]
        print(_pos_str)
        pos = _pos_str.rindex('.')
        print(pos)
        if pos is 5:
            _st = _pos_str[:pos]
            st_ = _pos_str[pos:]
            replce_uri = _auto_str + _st + '_1' + st_
            return replce_uri
        else:
            _st = _pos_str[:pos]
            print(_st)
            st_ = _pos_str[pos:]
            _st_t = _st.rindex('_')
            # page=_st+1
            # page=_st[_st_t + 1:]+1
            # print(page)
            # print(_st_t)
            _page_ix = int(_st[_st_t + 1:])


            _st_rep = _st.replace(str(_page_ix), str(_page_ix + 1))
            replce_uri = _auto_str + _st_rep + st_
            return replce_uri
        return None
