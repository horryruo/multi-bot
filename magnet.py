#  coding: utf-8
import requests
import re 
import json
import time
from queue import Queue
import threading 
from function_requests import get_html_html
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from jinja2 import PackageLoader,Environment
def sukebei_findindex(searchid):
    url = 'https://sukebei.nyaa.si/?q={}'.format(searchid)
    r = get_html_html(url)
    html = r.html.html
    #titleall = r.html.find('td:nth-child(2)>a:nth-child(1)')
    #maglink = r.html.find('td:nth-child(3)>a:nth-last-child(1)')
    #sizeall = r.html.find('td:nth-child(4)')
    soup = BeautifulSoup(html,'lxml')
    titleall = soup.find('tbody').find_all('a',href=re.compile('view'))
    title = re.findall(r'<a href=\"(/view/\d+)\" title=\"(.*?)\">.*?</a>',str(titleall))
    searchdata = {}
    urlint = 0
    for i in title:
        searchdata[i[1]] = 'https://sukebei.nyaa.si' + i[0]
        urlint += 1
    #magnetall = soup.find('tbody').find_all('a',href=re.compile('magnet'))
    #magnet = re.findall(r'''<a href=\"(magnet:\?xt=urn:btih:.*?)\"><i class=\"fa fa-fw fa-magnet\"></i></a>''',str(magnetall))
    #searchdata['magnet'] = magnet
    #sizeall = soup.find('tbody').find_all('td',attrs = {'class' : 'text-center'})
    #size = re.findall(r'<td class=\"text-center\">([\d.]*?) ([GiBMiBBytes]*?)</td>',str(sizeall))
    return (searchdata, urlint)
    
def producer(in_q, titledata):
    for i in titledata:
        in_q.put(titledata[i])


def sukebei_one(in_q, jsondata):
    url = in_q.get()
    #url = 'https://sukebei.nyaa.si/view/3039545'
    time.sleep(2)
    r = get_html_html(url)
    html = r.html.html
    soup = BeautifulSoup(html,'lxml')
    onedata = {}
    nolike = 0
    onedata['url'] = url
    try:
        title = soup.find('h3', attrs={'class' : 'panel-title'}).string.replace('\n','').replace('\t','').replace('+','').replace(' ','').replace('[','').replace(']','')
        onedata['title'] = title
        
    except:
        onedata['title'] = '---'
        nolike = 1
    try:
        magnetall = soup.find('div', attrs={'class' : 'panel-footer clearfix'})
        magnet = re.findall(r'''(magnet:\?xt=urn:btih:.*?)\"><i class=\"fa fa-magnet fa-fw\">''',str(magnetall))[0]
        onedata['magnet'] = magnet
    except:
        onedata['magnet'] = '---'
        nolike = 1
    try:
        sizeall = soup.find('div', attrs={'class' : 'panel-body'})
        size = re.findall(r'<div class=\"col-md-1\">File size:</div>[\s\S]*?div class=\"col-md-5\">(.*?)</div>',str(sizeall))
        onedata['size'] = size[0]
    except:
         onedata['size'] = '---'
         nolike = 1
    try:
        fileindexall = soup.find('div', attrs={'class' : 'torrent-file-list panel-body'})
        fileindex_1 = re.findall(r'<li><i class=\"fa fa-file\"></i>(.*?) <span class=\"file-size\">\(.*?\)</span></li>',str(fileindexall))
        fileindex = ','.join(fileindex_1)
        onedata['fileindex'] = fileindex
    except:
        onedata['fileindex'] = '---'
        nolike = 1
    try:
        strfileindex = ''.join(fileindex_1)
    except:
        pass
    try:
        nolike_list = ["第一会所","宣传","論壇","澳门皇冠赌场"]
        for i in nolike_list:
            if i in strfileindex:
                nolike = 1
                break
    except:
        nolike = 1
    if nolike == 0:
        #print(onedata)
        jsondata.append(onedata)

    in_q.task_done() 

def sukebei_thread(searchid):
    start = time.time()
    #searchlist = searchid.split(',')
    #print(searchlist)
    #leng2 = len(searchlist)
    titledata, urlint = sukebei_findindex(searchid)
    queue = Queue()
    jsondata = []
    producer_thread = threading.Thread(target=producer, args=(queue,titledata))
    #producer_thread.daemon = True
    producer_thread.start()
    
    for i in range(1,int(urlint)+1):
        consumer_thread = threading.Thread(target=sukebei_one, args=(queue, jsondata))
        consumer_thread.daemon = True
        consumer_thread.start()
    queue.join()
    end = time.time()
    usetime = str(end - start)
    return (jsondata,usetime)
def template_magnet(alldataa,usetimee,searchidd):
    #print(ciddataa_performers)
    env = Environment(loader=PackageLoader('magnet','templates'))    # 创建一个包加载器对象
    template = env.get_template('magnet.md')    # 获取一个模板文件
    temp_out = template.render(alldata = alldataa,usetime = usetimee, searchid = searchidd) 
    #print(temp_out)  # 渲染
    return (temp_out)

def sukebei(searchid):
    alldata, usetime = sukebei_thread(searchid)
    temp_out = template_magnet(alldata, usetime,searchid)
    return temp_out

if __name__ == "__main__":
    print(sukebei('SSNI-848'))
    
