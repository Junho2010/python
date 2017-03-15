# -*- coding:utf-8 -*-
from ScrolledText import ScrolledText
from Tkinter import *
import urllib, re, requests, sys, os, time, threading
reload(sys)
sys.setdefaultencoding('utf-8')     # 设置默认字符集

class budejie:
    
    def __init__(self):
        
        self.threads = []    # 线程队列
        self.lock = threading.Lock()
        # 创建gui界面
        self.master = Tk()
        self.master.title('百思不得姐')
        self.master.geometry('+200+200')    # 坐标
        self.text = ScrolledText(self.master, font=('微软雅黑', 10))    # 滚动条
        self.text.grid(row=0, columnspan=3)
        Label(self.master, text='请输入需要爬取视频的数目', font=('微软雅黑', 10)).grid(row=1, column=0)
        self.e = Entry(self.master)
        self.e.grid(row=1, column=1)
        self.e.insert(10,'1')
        self.button = Button(self.master, text='开始爬取', font=('微软雅黑', 10), command=self.start)
        self.button.grid(row=1, column=2)
        self.varl = StringVar()
        self.label = Label(self.master, font=('微软雅黑', 10), fg='red', textvariable=self.varl)
        self.label.grid(row=2,columnspan=3)
        self.master.mainloop()
        self.varl.set('熊猫说:已经准备好了...')


    def getPage(self, index):
        # requests请求网页源代码
        url = 'http://www.budejie.com/video/' + str(index)
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        try:
            page = requests.get(url, headers={'User-Agent' : user_agent})
            return page
        except:
            return None
        

    def getInfo(self, pageCode, url_num=20):
        # re正则获取视频链接
        pattern = re.compile(r'<div class="j-r-list-c">.*?<a href="/detail-.{8}?.html">(.*?)</a>.*?data-mp4="(.*?)".*?</div>.*?</div>', re.S)
        urlList = re.findall(pattern, pageCode)
        return urlList[0:url_num]    # 切片


    def download(self, url_content):
        # 下载模块
        urllib.urlretrieve(url_content[1], url_content[0][:16] + '.mp4')


    def start(self):
        count = int(self.e.get())
        if count:
            # 创建video文件夹
            if os.path.exists('video') == False:
                os.mkdir('video')
            os.chdir('video')

            page_num = 1
            while count > 0:
                page = self.getPage(page_num)
                page_num = page_num + 1
                if page:
                    url_contents = self.getInfo(page.text, count)
                    count = count - 20
                    for url_content in url_contents:
                        self.text.insert(END, '正在抓取:\t' + url_content[0][0:16] + '\n')
                        th = threading.Thread(target=self.download, args=(url_content, ))
                        th.start()
                        self.threads.append(th)
                        time.sleep(2)

            
            for th in self.threads:
                th.join()
            self.varl.set('熊猫说:视频已经抓取完毕...')

        else:
            print u'没有获取到您输入的数目,请重新输入...'

if __name__ == '__main__':
    budejie().start()