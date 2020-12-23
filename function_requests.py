import requests
from cfscrape import get_cookie_string
from traceback import format_exc
from time import sleep
from re import search, findall
from requests_html import HTMLSession
from loadini import read_config

allconfig = read_config()
ifproxy = allconfig['ifproxy'] 
proxy = allconfig['proxy'] 

proxies = {'http': 'http://%s'%proxy, 'https': 'http://%s'%proxy}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
headers_jp = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Accept-Language': 'ja;q=0.9',
    'cookie' : 'age_check_done=1',
    }
headers_jp_phone = {
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
    'Accept-Language': 'ja;q=0.9',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    }
def get_html(url):
    if ifproxy == 'true':
        rqs = requests.get(url,headers=headers,proxies=proxies)
    else:
        rqs = requests.get(url,headers=headers)
    rqs.encoding = 'utf-8'
    html = rqs.text
    return html

def get_html_html(url):
    session = HTMLSession()
    session.headers.update(headers)
    #session = requests.session()
    if ifproxy == 'true':
        rqs = session.get(url,proxies=proxies)
    else:
        rqs = session.get(url)
    #rqs.encoding = 'utf-8'
    #html = rqs.decode("utf8", "ignore")
    return rqs

def get_html_jp(url):
    session = requests.session()
    if ifproxy == 'true':
        rqs = session.get(url,headers=headers_jp,proxies=proxies).content
    else:
        rqs = session.get(url,headers=headers_jp).content
    #rqs.encoding = 'utf-8'
    html = rqs.decode("utf8", "ignore")
    return html

def get_html_jp_html(url):
    session = HTMLSession()
    session.headers.update(headers_jp)
    #session = requests.session()
    if ifproxy == 'true':
        rqs = session.get(url,proxies=proxies)
    else:
        rqs = session.get(url)
    #rqs.encoding = 'utf-8'
    #html = rqs.decode("utf8", "ignore")
    return rqs

def get_html_jp_cookies(url):
    cookie_value, user_agent = get_cookies_jp(url)
    headers_cookies_jp = {'User-Agent': user_agent, 'Cookie': cookie_value, 'Accept-Language': 'ja;q=0.9'}
    if ifproxy == 'true':
        rqs = requests.get(url,headers=headers_cookies_jp,proxies=proxies)
    else:
        rqs = requests.get(url,headers=headers_cookies_jp)
    rqs.encoding = 'utf-8'
    html = rqs.text
    return html

def get_cookies_jp(url):

    for retry in range(10):
        try:
            if ifproxy == 'true':
                cookie_value, user_agent = get_cookie_string(url, proxies=proxies, timeout=15)
            else:

                cookie_value, user_agent = get_cookie_string(url, timeout=15)
            #print('通过5秒检测！\n')
            return (cookie_value, user_agent)
        except:
            # print(format_exc())
            #print('通过失败，重新尝试...')
            continue
# 获取一个library_cookie，返回cookie
def steal_library_header(url):
    #print('\n正在尝试通过', url, '的5秒检测...如果超过20秒卡住...重启程序...')
    for retry in range(10):
        try:
            if ifproxy == 'true':
                cookie_value, user_agent = get_cookie_string(url, proxies=proxies, timeout=15)
            else:

                cookie_value, user_agent = get_cookie_string(url, timeout=15)
            #print('通过5秒检测！\n')
            return {'User-Agent': user_agent, 'Cookie': cookie_value}
        except:
            # print(format_exc())
            #print('通过失败，重新尝试...')
            continue
    print('>>通过javlibrary的5秒检测失败：', url)



# 搜索javlibrary，或请求javlibrary上jav所在网页，返回html
def get_library_html(url, header):
    for retry in range(10):
        try:
            if ifproxy == 'true':
                rqs = requests.get(url, headers=header, proxies=proxies, timeout=(6, 7), allow_redirects=False)

            else:
                rqs = requests.get(url, headers=header, timeout=(6, 7), allow_redirects=False)
            
        except:
            print('    >打开网页失败，重新尝试...')
            continue
        rqs.encoding = 'utf-8'
        rqs_content = rqs.text
        # print(rqs_content)
        if search(r'JAVLibrary', rqs_content):        # 得到想要的网页，直接返回
            return rqs_content
        elif search(r'jav.*?', rqs_content):           # 搜索车牌后，javlibrary跳转前的网页
            url = url[:23] + search(r'(\?v=jav.*?)"', rqs_content).group(1)    # rqs_content是一个非常简短的跳转网页，内容是目标jav所在网址
            if len(url) > 70:                          # 跳转车牌特别长，cf已失效
                header = steal_library_header(url[:23])  # 更新header后继续请求
                continue
            #print('    >获取信息：', url)
            continue                                  # 更新url后继续get
        elif search(r'Compatible', rqs_content):     # cf检测
            header = steal_library_header(url[:23])    # 更新header后继续请求
            continue
        else:                                         # 代理工具返回的错误信息
            print('    >打开网页失败，空返回...重新尝试...')
            continue
    
    