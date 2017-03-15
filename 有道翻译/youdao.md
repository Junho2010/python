`python version: 2.7`
平常都是用终端敲， 有时候不会的词语也懒得打开词典了，干脆搞了个简单的查词命令.思路也很简单，直接调用有道的api，解析下返回的json就ok了,只用到了python原生的库。

这里是列表文本将上面代码粘贴后命名为youdao.py
这里是列表文本修改名称`mv youdao.py youdao`, 然后加上可执行权限`chmod a+x youdao`
这里是列表文本拷贝到`/usr/local/bin`。 `cp youdao /usr/local/bin`