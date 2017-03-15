# -*- coding:utf-8 -*-
# !/usr/bin/env python
'''

    File Name: youdao.py
    Description: 实现命令行有道翻译
    Author: csy
    date: 2017/2/27

'''
import sys, urllib, urllib2, json


def getPageCode(query_str=''):
    query_str = query_str.strip("'").strip('"').strip()    # 移除',",空格
    if not query_str:
        query_str = 'python'
    print u'翻译内容:', query_str

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    data = {
        'type': 'ZH_CN2EN',
        'i': query_str,
        'doctype': 'json',
        'xmlVersion': '1.8',
        'keyfrom': 'fanyi.web',
        'ue': 'UTF-8',
        'action': 'FY_BY_CLICKBUTTON',
        'typoResult': 'true'
    }
    data = urllib.urlencode(data).encode('utf-8')

    response = urllib2.urlopen(url, data=data, timeout=3)
    pageCode = response.read().decode('utf-8')
    return pageCode


def parse(pageCode):
    d = json.loads(pageCode)
    try:
        if d.get('errorCode') == 0:
            print u'翻译结果:\n', d['translateResult'][0][0]['tgt']
            print u'智能结果:'
            for explain in d['smartResult']['entries']:
                if explain:
                    print explain
        else:
            print u'无法翻译'
    except:
        print u'翻译出错,请输入合法单词'


def main():
    try:
        s = sys.argv[1]    # 获取命令行上的参数
    except:
        s = 'python'
    parse(getPageCode(s))


if __name__ == '__main__':
    main()
