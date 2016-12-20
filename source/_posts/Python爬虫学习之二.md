---
title: Python爬虫学习之二
date: 2016-04-09 22:27:19
tags: Python
categories: Python
---
### Scrapy学习
>An open source and collaborative framework for extracting the data you need from websites. In a fast, simple, yet extensible way.

Scrapy是一个开源的、能够快速、简单获取你所需网页数据的的框架，并且它具有良好的可扩展性。

首先，它是一个框架，大部分时候是作为爬虫架构来使用。它与BeautifulSoup，request不同，严格意义上来说后两者是一个用来解析HTML\XML的Python库，爬取工作仍然需要urllib或者其他的库来配合完成；而Scrapy提供了一整套网页爬取的架构，包括：爬取、下载，储存等功能。
<!--more-->
下图很形象的说明了Scrapy的工作原理：
![Scrapy](http://upload-images.jianshu.io/upload_images/1858466-e15a81faf81eb7f2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**ScrapyEngine**：位于`Scrapy/core/engine`，作为整个框架的引擎，驱动Scheduler，Donwload，Spiders。
``` python
          class ExecutionEngine(object):
              def start(self):
                  do something
              def schedule(self, request, spider):
                  do something related to scheduler
              def download(self, request, spider):
                  do something related to downloader
              def spider(self, request, spider):
                  do something related to schedule
              other function
```
**Scheduler**：从`start_urls`依此获取url，交给Downloader下载，并且从Spiders中过去新的url~~(如果有的话)~~。
``` python
          class Scheduler(object):
              def open(self, spider)
                   open spider
              def enqueue_request(self,request):
                   do something
              def next_request(self)
                   get next_request
              other function
```                
**Downloader**：获取Scheduler里的url，从网络中获取url的内容，并将获取内容交给Spiders。
``` python       
        class Downloader(object):
            def fetch(self, request, spider):
                fetching
            def download(self, slot, request, spider):
                download
```
**Spiders**：解析获取页面的内容，通过XPath，获得需要的内容，将这些内容存放到Item定义的Field中~~并交给Pipeline进一步处理~~。
``` python        
        class yourSpider(Spider):
            name = "your spider name, unique"
            domain = "allowed domain"
            start_urls = ["https://www.target.com/",
                           other urls,
                         ]
            rules = [Rule(your rules)]
            def parse(self, response):
                do something
```
**Item**：Scrapy自定义的字典，规定你需要从网页中获取的内容。例如，你想要获得豆瓣排名前二十名的电影的名字、导演、评分，那么可以在Item中定义：
``` python
         from scrapy import Item, Field
         class DoubanItem(Item):
              title = Field()    
              movieInfo = Field()    
              star = Field()    
              quote = Field()
```
**Pipeline**：对Item中的数据做进一步处理，存入数据库or丢弃掉。
``` python
        class DoubanPipeline(object):
            def process_item(self, item, spider):
                do something
```
以上是一个完整的Scrapy爬虫框架，Scrapy已经为我们写好了前三部分(Engine，Scheduler，Downloader)，我们只需要自己写出Spiders，Item，Pipeline就好。

>这里是scrapy的[中文文档](http://scrapy-chs.readthedocs.org/zh_CN/latest/intro/tutorial.html)，如果我说的不清楚，大家可以去看官方文档。