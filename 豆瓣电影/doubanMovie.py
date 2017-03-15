# -*- coding:utf-8 -*-

import urllib2, sys, Queue, sys, threading,time
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
'''

    File Name: douban.py
    Description: 爬取豆瓣电影Top250
    Author: csy
    date: 2017/2/28

'''

class doubanMovie:

    def __init__(self):
        self.threads = []
        self.douban_url = 'https://movie.douban.com/top250?start={page}&filter='
        self.top = 1
        self.titleData = Queue.Queue()

    def worker(self, url):
        pageCode = self.getPage(url).read().decode('utf-8').encode('utf-8')
        self.find_title(pageCode)
        time.sleep(1)

    def getPage(self, url):
        try:
            page = urllib2.urlopen(url, timeout=3)
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print u"The server couldn't fulfill the request."
                print u"Error code: %s" % e.code
            elif hasattr(e, 'reason'):
                print u"We failed to reach a server. Pleasa check your url and read reason."
                print u"Reason: %s" % e.reason
        return page


    def find_title(self, pageCode):
        for info in BeautifulSoup(pageCode, 'lxml').find_all('div', class_='info'):
            title = 'Top%s'%(self.top) + info.find('span', class_='title').text
            self.titleData.put(title)
            self.titleData.task_done()
            # print title
            self.top += 1


    def start(self):
        print u"豆瓣电影爬虫准备就绪, 准备爬取数据..."
        for index in xrange(10):
            url = self.douban_url.format(page=index*25)
            thread = threading.Thread(target=self.worker, args=(url, ))
            self.threads.append(thread)
        
        for thread in self.threads:
            thread.start()
            thread.join()

        with open('./doubanMovie.text', 'w') as f:
            while not self.titleData.empty():
                title = self.titleData.get() + '\n'
                f.writelines(title)
        f.close()

if __name__ == '__main__':
    doubanMovie().start()
