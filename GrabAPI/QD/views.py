from django.shortcuts import render  # Added for this step
import datetime
import xlwt
from lxml import etree
import requests
import time
from django.http import JsonResponse,HttpResponse,HttpRequest
import simplejson
import urllib.request
import sys
from bs4 import BeautifulSoup

# Create your views here.
all_info_list = []
url = 'https://www.qidian.com/all'
#伪装请求头
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}
#定义获取爬虫信息的函数
def GetAllInfo(request: HttpRequest):
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
  	#采用xpath方法对网页信息进行搜索
    infos = selector.xpath('//ul[@class="all-img-list cf"]/li') #找到信息的循环点
    i = 0
    for info in infos:
       if i<10:
        id = info.xpath("div[1]/a/@data-bid")[0]
        # id=info.xpath("div[1]/a/@href")[0]
        img = info.xpath("div[1]/a/img/@src")[0]
        title = info.xpath('div[2]/h4/a/text()')[0]
        author = info.xpath('div[2]/p[@class="author"]/a[@class="name"]/text()')[0]
        style1 = info.xpath('div[2]/p[@class="author"]/a[2]/text()')[0]
        style2 = info.xpath('div[2]/p[@class="author"]/a[3]/text()')[0]
        style = style1 + '-' + style2
        complete = info.xpath('div[2]/p[@class="author"]/span/text()')[0]
        introduce = info.xpath('div[2]/p[@class="intro"]/text()')[0].strip()
        info_list = [id,img,title, author, style1,style2, complete, introduce]
        all_info_list.append(info_list) 
        i +=1
    #爬取成功后等待两秒
    time.sleep(2)
    return JsonResponse(all_info_list,safe=False)


#定义获取爬虫信息的函数--爬详细信息
def GetInfoDetail(request: HttpRequest): 
    detailUrl ='https://book.qidian.com/info/'
    id = request.GET.get("id")
    detailUrl +=id
    res = requests.get(detailUrl, headers=headers)
    selector = etree.HTML(res.text)
  	#采用xpath方法对网页信息进行搜索
    infos = selector.xpath('//div[@class="book-information cf"]') #找到信息的循环点
    info2 = selector.xpath('//div[@class="book-intro"]')
    for info in infos:
        #id= info.xpath("div[1]/a/img/@src")[0]
        # id=info.xpath("div[1]/a/@href")[0]
        img = info.xpath("div[1]/a/img/@src")[0]
        title = info.xpath('div[2]/h1/em/text()')[0]
        author = info.xpath('div[2]/h1/span/a[@class="writer"]/text()')[0]
        tag = info.xpath('div[2]/p[@class="tag"]/span[1]/text()')[0]
        style = info.xpath('div[2]/p[@class="tag"]/a[2]/text()')[0]
        intro = info.xpath('div[2]/p[@class="intro"]/text()')[0]
      #  binfos =selector.xpath('//div[@class=book-content-wrap cf"]')
        bookintro = ''
        for bin in info2:
            bookintrolist = bin.xpath('p/text()')
            for l in bookintrolist:
                bookintro +=l
        #style = style1+'-'+style2
       # complete = info.xpath('div[2]/p[@class="author"]/span/text()')[0]
       # introduce = info.xpath('div[2]/p[@class="intro"]/text()')[0].strip()
        info_list = [img,title, author, tag,style, intro,bookintro]
       # all_info_list.append(info_list)
        return JsonResponse(info_list,safe=False)

#获取一个章节目录内容，按100章一抓
def getChapterContent(chapter_list,url,pagesize):
    #try:
       
        bookContentRes = urllib.request.urlopen(url)
        bookContentSoup = BeautifulSoup(bookContentRes.read(), "html.parser")
        chapterName =bookContentSoup.select("h3[class='j_chapterName']")[0].text
        chapterUr =url
       # file.write(bookContentSoup.select("h3[class='j_chapterName']")[0].text + '\n')
       # for p in bookContentSoup.select(".j_readContent p"):
       #     file.write(p.text + '\n')
       
       
   # except BaseException:
        #如果出错了，就重新运行一遍
       # print(BaseException.message)
     #   getChapterContent(chapter_list, url,10)
  #  else:
        chapterNext = bookContentSoup.select("a#j_chapterNext")[0]
        if chapterNext.string != "书末页" and len(chapter_list) < pagesize:
            nextUrl = "https:" + chapterNext["href"]
            list=[chapterName,chapterUr,nextUrl]
            chapter_list.append(list)
            getChapterContent(chapter_list,nextUrl,10)
        return chapter_list 

#获取书内容
def GetContent(request:HttpRequest):
      contenturl = request.GET.get("url")
      #detailUrl +=id
     # bRes =  urllib.request.urlopen("https:" + bookCover['href'])
    # bSoup = BeautifulSoup(bRes.read(), "html.parser")
     # bookContentHref = bSoup.select("a[class='red-btn J-getJumpUrl']")[0]["href"]
    #  getChapterContent("https:" + bookContentHref)
      bookContentRes = urllib.request.urlopen(contenturl)
      bookContentSoup = BeautifulSoup(bookContentRes.read(), "html.parser")
      chapterName =bookContentSoup.select("h3[class='j_chapterName']")[0].text
      chapterUr =url
      contents =''
       # file.write(bookContentSoup.select("h3[class='j_chapterName']")[0].text + '\n')
      for p in bookContentSoup.select(".j_readContent p"):
          contents += p.text + '\n'
      rets = {"Contents":contents}
      return JsonResponse(rets,safe=False)

def GetChapterList(request:HttpRequest):
      detailUrl ='https://book.qidian.com/info/'
      id = request.GET.get("id")
      detailUrl +=id
      bRes =  urllib.request.urlopen(detailUrl)
      bSoup = BeautifulSoup(bRes.read(), "html.parser")
      bookContentHref = bSoup.select("a[class='red-btn J-getJumpUrl']")[0]["href"]
      chapter_list =[]
      chapter_list= getChapterContent(chapter_list,"https:" + bookContentHref,10)
      return JsonResponse(chapter_list,safe=False)