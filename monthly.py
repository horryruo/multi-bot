#  coding: utf-8
import requests
from re import search, findall
import os 
import threading 
import time
import json
from queue import Queue
import prettytable as pt
from loadini import read_config



allconfig = read_config()
ifproxy = allconfig['ifproxy'] 
proxy = allconfig['proxy'] 

proxies = {'http': 'http://%s'%proxy, 'https': 'http://%s'%proxy}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
           
def monthly(in_q, mon,nomon,noresult,jsondata):
    searchid = in_q.get()
    url = 'https://v2.mahuateng.cf/isMonthly/%s' %searchid
    #print(url)
    if ifproxy == 'true':
        response = requests.get(url,headers=headers,proxies=proxies)
    else:
        response = requests.get(url,headers=headers)
    #print(response.text)
    if response.status_code==200:
        mjson = response.json()
        bitrate = mjson.get('bitrate')
        monthly = mjson.get('monthly')
        data = {}
        data['id'] = searchid
        data['monthly'] = monthly
        data['bitrate'] = bitrate
        jsondata.append(data)
        if monthly == True:
            mon.append(searchid)
        elif monthly == False:
            nomon.append(searchid)
        else:
            noresult.append(searchid)

    in_q.task_done() 
def producer(in_q, searchlist):  # 生产者
    
    for i in searchlist:
       
        in_q.put(i)
def monthly_thread(searchid):
    start = time.time()
    searchlist = searchid.split(',')
    #print(searchlist)
    leng2 = len(searchlist)
    
    mon = []
    nomon = []
    noresult = []
    jsondata = []
    queue = Queue(maxsize=10)
    producer_thread = threading.Thread(target=producer, args=(queue,searchlist))
    producer_thread.daemon = True
    producer_thread.start()

    for i in range(1,int(leng2)+1):
        consumer_thread = threading.Thread(target=monthly, args=(queue,mon,nomon,noresult,jsondata))
        consumer_thread.daemon = True
        consumer_thread.start()
    queue.join()
    #print(mon,nomon)
    leng = len(mon)
    leng1 = len(nomon)
    leng2= len(noresult)
    mon.sort()
    nomon.sort()
    noresult.sort()
    mon = ','.join(mon)
    nomon = ','.join(nomon)
    noresult = ','.join(noresult)
    tb = pt.PrettyTable()
    tb.field_names = ["id", "if?monthly", "bitrate"]
    for id in jsondata:
        tb.add_row([id['id'],id['monthly'],id['bitrate']])
    #tb.align["id", "是否月额", "码率"] = "c"
    #return(mon,leng,nomon,leng1)
    tbb = tb.get_string()
    end = time.time()
    usetime = str(end - start)
    return (mon,leng,nomon,leng1,usetime,tb,tbb,noresult,leng2)

    


def abp(input1):
    
    url = 'https://www.prestige-av.com/images/corner/goods/prestige/tktabp/%s/pb_tktabp-%s.jpg' %(input1,input1)
    req = requests.get(url,headers=headers,proxies=proxies)
    
    filename = 'abp-%s.jpg' %input1
    with open(filename,'wb') as f:
        f.write(req.content)
        f.close()
    

#abp()

if __name__ == "__main__":
    id = 'ssni520,ssni521,ssni802,13gvg00349,jbd00194'
    monthly(id)




