---
title: Python爬虫学习之一
date: 2016-04-06 22:49:45
tags: Python
categories: Python
---
>这几天发现一个比较适合Python爬虫初学者的网站，我是跟着里边的kingname老师学习，这就当作是一个学习笔记里，有人想去听老师讲课，可以点[这里](http://my.jikexueyuan.com/6128566806/record/)。

<!--more-->
## 单线程爬虫
如何伪装成浏览器呢？
```Python      
    import reques
    header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"}
    html = request.get(url, header = header)
    html.encoding = 'utf-8'
```
在get或者post的时候加入**User-Agent**可以伪装成浏览器。至于怎么获得**User-Agent**?
<font face="Aril" color="blue">chrome->F12->Network->随便点一个接收的信息->Headers->Request Headers</font>。

***
## 解析HTML，获取有用信息

1. 正则表达式
比较笨的办法。适用于网页简单，正则特别好写的情况，不用安装别的库了。
2. 利用DOM解析HTML
BeautifulSoup，request啊什么的都提供了一些功能强大的DOM解析方法，便于使用。
3. 利用XPath解析HTML
这其实也是DOM解析的一种吧？但是在爬一些比较复杂的网页时候，特别好用。

#### XPATH
怎么使用XPath？
```Python
        from lxml import etree
        selector = etree.HTML(html)
        selector.xpath('XPATH')
```
XPath怎么写？
```Python
      //     ：根节点
      /      ：往下层寻找
      /text()：提取文本内容
      /@attr ：提取属性内容

      #提取div的id为first_div的文字内容  
      selector.xpath('//div[@id="first_div"]/text()')
      
      #提取a标签的href属性
      selector.xpath('//a/@href')
```

***
## 多线程爬虫
虽然Python有[GIL](https://zh.wikipedia.org/wiki/GIL)，但是多线程还是可以在一定程度上提升爬取的速度。
```Python
      from multiprocessing.dummy import Pool as ThreadPool
      pools = ThreadPool(__max_core_num__)
      results = pools.map(Spider_function, target_urls)
      pools.join()
      pools.close()
```
**map(func, seq)**函数是Python内置函数，用来接收seq内元素依此执行func后返回的值。