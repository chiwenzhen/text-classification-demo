# coding=utf-8
import sys
import urllib2
import urllib
import time
import json
from pyquery import PyQuery as pyq
from lxml import etree
from bs4 import BeautifulSoup
# import MySQLdb


class Article:
    def __init__(self, a_title, a_text, a_author, a_url, a_time, a_tags):
        self.a_title = a_title
        self.a_text = a_text
        self.a_author = a_author
        self.a_url = a_url
        self.a_time = a_time
        self.a_tags = a_tags


class Crawler:
    def __init__(self, name, url):
        self.name = name
        self.root_url = url
        self.count = 0

    def crawl(self, end_time, start_time=None):
        pass

    def save(self):
        pass


# 虎嗅
class HuxiuCrawler(Crawler):
    def __init__(self):
        Crawler.__init__(self, "虎嗅", "http://www.huxiu.com")

    def crawl(self, start_time, end_time):
        # 初次加载的内容
        html = urllib2.urlopen("https://www.huxiu.com/startups.html").read()
        # doc = pyq(html)
        # print doc
        # content = doc(".mod-info-flow")
        # divs = content.find("div.mod-b.mod-art")
        # for div in divs.items():
        #     href = div.find(".transition").attr("href")
        #     url = self.root_url + href
        #     article = self.parse_html(url)
        #     if start_time <= article.time or article.time <= end_time:
        #         self.save(article)
        #     else:  # 如果当前文章时间不符合要求，则停止搜索后面所有文章
        #         break

        out_of_date = False
        soup = BeautifulSoup(html, "lxml")
        divs = soup.select("div .mod-b.mod-art")
        for div in divs:
            if out_of_date:
                break
            href = div.div.a["href"]
            url = self.root_url + href
            article = self.parse_html(url)
            if start_time <= article.a_time or article.a_time <= end_time:
                self.count += 1
                self.save(article)
            else:  # 如果当前文章时间不符合要求，则停止搜索后面所有文章
                out_of_date = True
        div_get_more = soup.find(name="div", class_="get-mod-more transition js-get-mod-more-list")


        # 点击加载更多
        page = 1
        req_url = 'http://www.huxiu.com/v2_action/article_list'
        params = {'huxiu_hash_code': '8108c2df22264a5769c3a50798622c16', 'page': 1, 'catid': 2}
        while True:
            if out_of_date:
                break
            page += 1
            params['page'] = page
            req_data = urllib.urlencode(params)
            try:
                # request = urllib2.Request(url=req_url, data=req_data)
                # response = urllib2.urlopen(request).read()
                # result = json.loads(response)
                # divs = pyq(result['data']).find("div.mod-b.mod-art")
                # for div in divs.items():
                #     href = div.find(".transition").attr("href")
                #     url = self.root_url + href
                #     article = self.parse_html(url)
                #     if True:
                #     # if start_time <= article.time <= end_time:
                #         self.save(article)
                #     else:  # 如果当前文章时间不符合要求，则停止搜索后面所有文章
                #         out_of_date = True
                #         break

                request = urllib2.Request(url=req_url, data=req_data)
                response = urllib2.urlopen(request).read()
                result = json.loads(response)
                soup = BeautifulSoup(result['data'], "lxml")
                divs = soup.find_all(name="div", class_="mod-b mod-art")
                for div in divs:
                    href = div.div.a["href"]
                    url = self.root_url + href
                    article = self.parse_html(url)
                    if True:
                    # if start_time <= article.time <= end_time:
                        self.count += 1
                        self.save(article)
                    else:  # 如果当前文章时间不符合要求，则停止搜索后面所有文章
                        out_of_date = True
                        break
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

    def save(self, article):
        print(str(self.count) + " " + article.a_time + " " + article.a_title + " " + article.a_url)

    # 分析html, 返回Article对象
    def parse_html(self, a_url):
        html = urllib2.urlopen(a_url).read()
        # doc = pyq(etree.fromstring(html))  # etree负责完善不完整的html
        # doc = pyq(html)
        # content = doc(".article-wrap")
        # title = content(".t-h1").text()
        # author = content(".article-author").find(".author-name").text()
        # time = content(".article-author").find(".article-time").text()
        # plist = map(lambda x: x.text(), content.find(".article-content-wrap").find("p").items())
        # text = reduce(lambda x, y: x + "\n" + y, plist, "")
        # alist = map(lambda x: x.text(), content.find(".tag-box ").find("a").items())
        # tags = reduce(lambda x, y: x + " " + y, alist, "")
        # article = Article(title=title, text=text, article_time=time, author=author, url=url, tags=tags)

        soup = BeautifulSoup(html, "lxml")
        article_wrap = soup.find(name="div", class_="article-wrap")
        #标题
        a_title = article_wrap.h1.string.encode('utf-8')
        # 作者，时间
        article_author = article_wrap.find(name="div", class_="article-author")
        a_author = article_author.span.a.string.encode('utf-8')
        a_time = article_author.find(name="span", class_="article-time").string.encode('utf-8')
        # 正文
        a_text = ""
        plist = article_wrap.find(name="div", class_="article-content-wrap").find_all(name="p")
        for p in plist:
            if p.string is not None:
                a_text = a_text + p.string.encode('utf-8') + "\n"
        # 标签
        a_tags = ""
        div_tag_box = article_wrap.find(name="div", class_="tag-box ")
        if div_tag_box is not None:
            alist = div_tag_box.ul.find_all(name="a")
        else:
            alist = []

        for a in alist:
            if a.li.string is not None:
                a_tags = a_tags + a.li.string.encode('utf-8') + " "

        article = Article(a_title=a_title, a_text=a_text, a_time=a_time, a_author=a_author, a_url=a_url, a_tags=a_tags)
        return article


# 时间转换：从字符串形式转浮点数，比如time_str2num("2011-09-28 10:00:00", "%Y-%m-%d %H:%M:%S")返回1317091800.0
def time_str2num(str_time, str_format):
    time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    huxiu = HuxiuCrawler()
    huxiu.crawl("2016-08-15 00:00:00", "2016-08-16 23:59:59")