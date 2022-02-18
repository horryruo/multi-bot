import re,time,json,os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from app.utils import Loadconfig
from bs4 import BeautifulSoup
from app.utils.func_requests import get_html_html
from jinja2 import PackageLoader,Environment


ifproxy = Loadconfig.ifproxy
proxy = Loadconfig.proxy
system = Loadconfig.system

class Javmost():
    def __init__(self,context):
        self.context = context
    def option(self):
        if self.context == []:
            return '''
    请附带搜索内容或命令
      *stream help* ==>  
       /stream v num 等待时间 `单番号视频链接,不能是cid,等待时间不填默认10秒`
       /stream 搜索内容  `搜索内容,不要cid`
            '''
        option = self.context[0]
        args = self.context[1:]
        if option == 'v':
            if args[1:] == []:
                return self.player(args[0])
            else:
                return self.player(args[0],float(args[1]))
        else:
            if len(self.context) == 1:
                searchstr = self.context[0]
            else:
                searchstr = ' '.join(self.context[:])
            return self.search(searchstr)
    def player(self,id,times=3):
        self.chrome = Chrome(True)
        url = 'https://www5.javmost.com/%s'%id
    # 开启无头模式提取视频m3u8路径地址
        self.chrome.dr.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": open(os.path.abspath(os.path.join('app',"bin",'hook.js')), encoding='utf-8').read()})
        self.chrome.dr.get(url)
        videoName = self.chrome.dr.title   # 获取当前页面title值
        print(videoName)
        checkbox = self.chrome.dr.find_element(By.CSS_SELECTOR,"[class='play-btn']")
        self.chrome.dr.execute_script("arguments[0].click();", checkbox)
        time.sleep(times)
        print('获取播放链接')
        request_log = self.chrome.dr.get_log('performance')
        for i in range(len(request_log)):
            message = json.loads(request_log[i]['message'])
            message = message['message']['params']
            # .get() 方式获取是了避免字段不存在时报错
            request = message.get('request')
            if request is None:
                continue
        
            url = request.get('url')
            if url == 'https://www5.javmost.com/ri3123o235r/':
                # 得到requestId
                #print(message['requestId'])
                # 通过requestId获取接口内容
                content = self.chrome.dr.execute_cdp_cmd('Network.getResponseBody', {'requestId': message['requestId']})
                #print(content)
                break
        url = json.loads(content.get('body')).get('data')[0]
        print(url)
        self.chrome.dr.quit()
        return url
    def search(self,id):
        url = 'https://www5.javmost.com/search/%s'%id
        response = get_html_html(url).content
        html = response.decode("utf-8", "ignore")
        soup = BeautifulSoup(html,'lxml')
        body = soup.find('div',attrs = {'class' : 'row'})
        try:
            result = body.find_all('div',attrs = {'class' : 'col-md-4 col-sm-6'})
            title = soup.title.string
        except:
            boxlist = 'no result'
            return boxlist
        boxlist = []
        for i in result:
            boxdict = {}
            card = i.find('div',attrs = {'class' : 'card'}).a
            boxdict['title'] = card.get('alt')
            boxdict['url'] = card.get('href')
            photo = i.find('div',attrs = {'class' : 'card'}).img.get('data-src')
            photo = re.sub(r'//|https://', 'https://',photo)
            boxdict['photo'] = photo
            boxlist.append(boxdict)
        env = Environment(loader=PackageLoader(__name__,"templates"))   # 创建一个包加载器对象
        template = env.get_template('javmost.md')    # 获取一个模板文件
        temp_out = template.render(data = boxlist,title = str(title)) 
            #print(temp_out)  # 渲染
        return temp_out
        #return boxlist

class Chrome(object):
    def __init__(self,is_headless):
        chrome_options = Options()
        if is_headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('lang=zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
        chrome_options.add_argument("disable-blink-features=AutomationControlled")
        chrome_options.add_argument('log-level=1')
        capabilities = webdriver.DesiredCapabilities().CHROME
        capabilities['acceptSslCerts'] = True
        capabilities['goog:loggingPrefs'] = {'browser': 'ALL','performance': 'ALL'}
        if ifproxy == 'true':
            chrome_options.add_argument('proxy-server=' + proxy)

        if system == 'Linux':
            try:
                self.dr = webdriver.Chrome(options=chrome_options,desired_capabilities=capabilities)
            except:
                self.dr = webdriver.Chrome(executable_path=os.path.abspath(os.path.join("app", "bin","chromedriver")),options=chrome_options,desired_capabilities=capabilities)
        elif system == 'Windows':
            self.dr = webdriver.Chrome(executable_path=os.path.abspath(os.path.join("app", "bin","chromedriver.exe")),options=chrome_options,desired_capabilities=capabilities)
        self.dr.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
       
