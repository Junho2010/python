# -*- coding:utf-8 -*-
# !/usr/bin/env python
'''

    File Name: PersonalizedSignature.py
    Description: 一键签名
    Author: csy
    date: 2017/2/28
'''

from Tkinter import *
import ttk
import tkMessageBox
import urllib, urllib2
import re
from PIL import Image

def getImg():
    name = nameEnt.get().encode('utf-8')
    style = styleCom.get().encode('utf-8')
    styleDict = {
        '个性签' : 'jfcs.ttf',
        '连笔签' : 'qmt.ttf',
        '潇洒签' : 'bzcs.ttf',
        '草体签' : 'lfc.ttf',
        '和文签' : 'haku.ttf',
        '商务签' : 'zql.ttf',
        '可爱签' : 'yqk.ttf'
    }
    if not name:
        tkMessageBox.showinfo('温馨提示', '请输入名字后再继续!')
    else:
        url = 'http://www.uustv.com/'
        values = {
            'word' : name,
            'sizes' : '60',
            'fonts' : styleDict[style],
            'fontcolor' :  '#000000'
        }
        data = urllib.urlencode(values)
        pageCode = urllib2.urlopen(url, data = data).read()
        reg = re.compile(r'<div class="tu">﻿<img src="(.*?)"/></div>', re.S)
        imgUrl = url + re.findall(reg, pageCode)[0]
        urllib.urlretrieve(imgUrl, './%s+%s.gif' %(name, style))    # Windows系统请转化成gbk码
        try:
            img = Image.open('./{}+{}.gif' .format(name, style))
            img.show()
            img.close()
        except:
            print '请自行打开图片'

if __name__ == '__main__':
    root = Tk()
    root.title('python签名设计')
    root.geometry('+500+200')
    Label(root, text='姓名:', font=('微软雅黑', 14)).grid(row=0, column=0)
    nameEnt = Entry(root, font=('微软雅黑', 14))
    nameEnt.grid(row=0, column=1)

    Label(root, text='样式:', font=('微软雅黑', 14)).grid(row=1, column=0)
    styleCom = ttk.Combobox(root, values=['个性签', '连笔签', '潇洒签', '草体签', '和文签', '商务签', '可爱签'])
    styleCom.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values']
    styleCom.grid(row=1, column=1)

    Button(root, text='一键设计签名', font=('微软雅黑', 14), width='14', height='1', command=getImg).grid(row=2, column=1)

    mainloop()