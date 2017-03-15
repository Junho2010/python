#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests, time, datetime, sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BookList:
    def __init__(self):
        self.url = 'https://book.douban.com/'
        self.bookList = []


    def getPage(self, url):
        headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        try:
            page = requests.get(url, headers=headers, timeout=3)
        except:
            print u'访问失败! 请从重新运行程序'
        finally:

            return page
    
    def findInfo(self, pageCode):
        for item in BeautifulSoup(pageCode, 'lxml').find('div', class_='slide-list').find_all('ul', class_='list-col list-col5 list-express slide-item'):
            for tag in item.find_all('li'):
                book =dict()
                book['title'] = tag.find('div', class_='title').text.strip()
                book['img'] = tag.find('div', class_='cover').find('img')['src']
                book['link'] = tag.find('a')['href']
                book['author'] = tag.find('div', class_='author').text.strip()
                book['year'] = tag.find('span', class_='year').text.strip()
                book['publisher'] = tag.find('span', class_='publisher').text.strip()
                book['abstract'] = tag.find('p', class_='abstract').text.strip()
                self.bookList.append(book)


    def savetoMD(self):
        today = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
        file_name = '豆瓣' + today + '推荐书单'
        with open(file_name+'.md', 'w') as file:
            file.write('##'+file_name)
            file.write('\n--------------------')
        file.close()
        
        with open(file_name+'.md', 'a') as file:
            num = 1
            for book in self.bookList:
                file.write('\n\n')
                file.write('##' + str(num) +'. ' + book['title'])
                file.write('\n')
                file.write('![' + book['title'] + ' cover img](' + book['img'] + ')')
                file.write('\n\n')
                file.write('简介\n')
                file.write('--------\n')
                file.write('book.abstract')
                file.write('\n\n')
                file.write('作者:      ' + book['author'] + '\n\n')
                file.write('出版时间:   ' + book['year'] + '\n\n')
                file.write('出版社:     ' + book['publisher'] + '\n\n')
                file.write('[跟多...](' + book['link'] + ')')
                num = num + 1
        file.close()


    def start(self):
        print u"豆瓣书单爬虫准备就绪, 准备爬取数据..."
        page = self.getPage(self.url)
        if page:
            self.findInfo(page.text)
            self.savetoMD()
            print '爬虫已完成工作'
        else:
            print u'没有获取到网页信息!'


if __name__ == '__main__':
    BookList().start()