#  coding: utf-8
import requests
import re 
import os
import time
import threading 
from queue import Queue
from function_requests import steal_library_header
from loadini import read_config



ifproxy,proxy,token,users = read_config()
proxies = {'http': 'http://%s'%proxy, 'https': 'http://%s'%proxy}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
def javlib_page(inurl):
    url = inurl + '&page={}'
    headers1 = steal_library_header(url)
    if ifproxy == True:
        req = requests.get(inurl, headers=headers1, proxies=proxies)
    else:
        req = requests.get(inurl, headers=headers1)

    req.encoding = 'utf-8'
    html = req.text
    actor = re.findall(r'<div class="boxtitle">(.*?)所演出的影片</div>',html)
    page = re.findall(r'<a class="page last" href=".*page=(.+)"',html)
    actor = actor[0]
    if page==[]:
        page = 1
    else:
        page = page[0]
    
    return(url, page, headers1, actor)
def javlib(in_q, out_q, headers):
    
    #print('正在获取%s的番号列表，共%d页' %(actor,int(page)))
    #print(in_q.get())
    while in_q.empty() is not True:
        if ifproxy == True:
            req = requests.get(url=in_q.get(), headers=headers, proxies=proxies)
        else:
            req = requests.get(url=in_q.get(), headers=headers)
        req.encoding = 'utf-8'
        html = req.text
        list = re.findall(r'<div class=\"id\">(.*?)</div>',html)
                #print(list)
        #for id in list:
            #if id not in alllist:
                #alllist.append(id)
            #else:
                #continue
        
        
        #print(list)
        out_q.put(list)
        in_q.task_done() 
def producer(in_q, url_arg, page):  # 生产者
    #ready_list = []
    #print('传入页数' + page)
    #print(url_arg)
    #while in_q.full() is False:
    for i in range(1, int(page)+1):
        url = url_arg.format(i)
            #print(url)
        #if url not in ready_list:
            #ready_list.append(url)
        in_q.put(url)
        

def thread_javlib(inurl):
    url, page, headers, actor = javlib_page(inurl)
    start = time.time()
    queue = Queue(maxsize=10)  
    result_queue = Queue()
    producer_thread = threading.Thread(target=producer, args=(queue, url, page))
    producer_thread.daemon = True
    producer_thread.start()
    for index in range(int(page)+1):
        consumer_thread = threading.Thread(target=javlib, args=(queue, result_queue, headers))
        consumer_thread.daemon = True
        consumer_thread.start()
    #print('开启线程数:' + str(threading.active_count()))
    queue.join()
    result = []
    list = []
    for i in range(1, int(page)+1):
        while result_queue.empty() is not True: 
            list += result_queue.get()
    result1 = []
    for i in list:
        if i not in result1:
            result1.append(i)
    result = ','.join(result1)
    leng = len(result1)
    end = time.time()
    result1 = '''%s的番号有%s页%s个：\n%s''' % (actor,page,leng,result)
    #print('总耗时：%s' % (end - start))
    usetime = '耗时:' + str(end - start) + '秒'
    return(result1,usetime)









if __name__ == '__main__':
    
    inurl = 'http://?/cn/vl_star.php?s=aebq4'
    url, page, headers, actor = javlib_page(inurl)
    #print('传出页数' + page)
    start = time.time()
    queue = Queue(maxsize=10)  
    result_queue = Queue()
    #print('queue 开始大小 %d' % queue.qsize())
    #print(threading.active_count()) 

    producer_thread = threading.Thread(target=producer, args=(queue, url, page))
    producer_thread.daemon = True
    producer_thread.start()
    
    #print(queue.get())
    for index in range(int(page)+1):
        #print(threading.active_count())
        consumer_thread = threading.Thread(target=javlib, args=(queue, result_queue, headers))
        consumer_thread.daemon = True
        consumer_thread.start()
    print('开启线程数:' + str(threading.active_count()))
    queue.join()
    
    result = []
    list = []
    for i in range(1, int(page)+1):
        while result_queue.empty() is not True: 
            list += result_queue.get()
            
    
    result = ','.join(list)
    end = time.time()
    #print(queue.get())
    print('''%s的番号有%s页：\n%s''' % (actor,page,result))
    #result = str(actor) + '在图书馆的番号有:\n' + str(result1)
    print('总耗时：%s' % (end - start))
    #print('queue 结束大小 %d' % queue.qsize())
    #print('result_queue 结束大小 %d' % result_queue.qsize())
    #inurl = 'https://www.g46e.com/cn/vl_star.php?s=azfuu'
    #result = javlib(inurl)
    #print(result)
    #inurl = input('url=')
    #alllist,actor = javlib(str(inurl))
    #save(alllist,actor)
    #urlbus = 'https://www.javbus.com/star/n5q'
    #alllist,actor = javbus(urlbus)
    #save(alllist,actor)


