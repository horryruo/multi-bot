from app.utils.func_requests import get_html_jp
from bs4 import BeautifulSoup
from jinja2 import PackageLoader,Environment
import re
class Faleno(object):
    def __init__(self,context):
        self.context = context

    def option(self):
        option = self.context[0]
        args = self.context[1:]
        if option == 'act':
            if args[:] == []:
                return self.actress()
            else:
                if len(args) == 1:
                    searchstr = args[0]
                else:
                    searchstr = ' '.join(args[:])
                return self.actress_work(searchstr)
        elif option == 'new':
            return self.new_work()
        elif option == 'work':
            return self.work(args[0])
        elif self.context == None:
            return '请附带搜索内容或命令'
        else:
            if len(self.context) == 1:
                searchstr = self.context[0]
            else:
                searchstr = ' '.join(self.context[:])
            return self.search(searchstr)
    def video(self,id):
        url = 'https://faleno.jp/top/works/%s'%id
        response = get_html_jp(url,verify=False)
        soup = BeautifulSoup(response,'lxml')
        video = soup.find('a',attrs = {'class' : 'pop_sample'}).get('href')
        return (video)
    def photo(self,id):
        url = 'https://faleno.jp/top/works/%s'%id
        response = get_html_jp(url,verify=False)
        soup = BeautifulSoup(response,'lxml')
        photos = soup.find_all('a',attrs = {'class' : 'pop_img'})
        photo = []
        for i in photos:
            photo.append(i.get('href'))
        return (photo)
    def search(self,word,searchmode='temp'):
        url = 'https://faleno.jp/top/?s=%s'%word
        response = get_html_jp(url,verify=False)
        soup = BeautifulSoup(response,'lxml')
        title = soup.find('section',attrs = {'class' : 'bread'}).p.contents[1]
        try:
            ifresult = re.findall(r'に一致する作品は見つかりませんでした',str(soup))
            noresult = "{}(没有找到相应内容的作品):{}".format(ifresult,title)
            if 'に一致する作品は見つかりませんでした' in ifresult:
                return noresult
        except Exception as e:
            print(e)
        results = soup.find_all('div',attrs = {'class' : 'waku_kanren01'})
        #print(title)
        boxlist = []
        for i in results:
            boxdict = {}
            liv = i.find('a')
            imgs = i.find('img')
            url = liv.get('href')
            boxdict['url'] = url
            name = imgs.get('alt')
            boxdict['name'] = name
            img = imgs.get('src')
            boxdict['img'] = img
            boxlist.append(boxdict)
        if searchmode=='search':
            return boxlist
        if searchmode=='temp':
            env = Environment(loader=PackageLoader(__name__,"templates"))   # 创建一个包加载器对象
            template = env.get_template('faleno.md')    # 获取一个模板文件
            temp_out = template.render(data = boxlist,title = str(title)) 
            #print(temp_out)  # 渲染
            return (temp_out)
    #单作品页面
    def work(self,id):
        url = 'https://faleno.jp/top/works/%s'%id
        response = get_html_jp(url,verify=False)
        soup = BeautifulSoup(response,'lxml')     
        box = {}          
        img = soup.find('a',attrs = {'class' : 'pop_sample'}).img.get('src')
        box['img'] = img
        title = soup.find('a',attrs = {'class' : 'pop_sample'}).img.get('alt')
        text = soup.find('div',attrs = {'class' : 'box_works01_text'}).p.string
        box['text'] = text
        file = soup.find_all('li',attrs = {'class' : 'clearfix'})
        box['url'] = url
        for i in file:
            box[i.find(text=True).strip()] = i.p.string
        env = Environment(loader=PackageLoader(__name__,"templates"))   # 创建一个包加载器对象
        template = env.get_template('faleno_work.md')    # 获取一个模板文件
        temp_out = template.render(data = box,title = str(title)) 
        #print(temp_out)  # 渲染
        return (temp_out)
    #全部演员页面
    def actress(self):
        url = 'https://faleno.jp/top/actress/'
        response = get_html_jp(url,verify=False)
        soup = BeautifulSoup(response,'lxml')
        title = soup.find('section',attrs = {'class' : 'bread'}).p.contents[1]
        group = soup.find_all('li',attrs = {'data-mh' : 'group01'})
        groups = []
        for i in group:
            box = {}
            links = i.a.get('href')
            name = i.find('div',attrs = {'class' : 'text_name'})
            id = re.findall(r'<div class="text_name">(.*)<span>(.*)</span></div>',str(name))[0]
            actress = id[0]
            eng_name = id[1]
            box['links'] = links
            box['name'] = actress
            box['eng'] = eng_name
            groups.append(box)
        env = Environment(loader=PackageLoader(__name__,"templates"))   # 创建一个包加载器对象
        template = env.get_template('faleno_actress.md')    # 获取一个模板文件
        temp_out = template.render(data = groups,title = str(title)) 
            #print(temp_out)  # 渲染
        return (temp_out)
#单演员页面
    def actress_work(self,name):
        name = name.replace(' ','_').lower()
        url = 'https://faleno.jp/top/actress/%s/'%name
        response = get_html_jp(url,verify=False)
        soup = BeautifulSoup(response,'lxml')
        profile = {}
        title = soup.title.string
        bar = soup.find('div',attrs = {'class' : 'bar02'}).h1
        barr = re.findall(r'<h1>(.*)<span>(.*)</span></h1>',str(bar))[0]
        img = soup.find('div',attrs = {'class' : 'box_actress02_left'}).img.get('src')
        files = soup.find('div',attrs = {'class' : 'box_actress02_right'}).find_all('li',attrs = {'class' : 'clearfix'})
        box = {}
        for i in files:
            box[i.find(text=True).strip()] = i.p.string
        body = soup.find('div',attrs = {'class' : 'box_kanren01'})
        results = body.find_all('div',attrs = {'class' : 'waku_kanren01'})
        boxlist = []
        for i in results:
            boxdict = {}
            liv = i.find('a')
            imgs = i.find('img')
            url = liv.get('href')
            boxdict['url'] = url
            name = imgs.get('alt')
            boxdict['name'] = name
            img = imgs.get('src')
            boxdict['img'] = img
            boxlist.append(boxdict)
        env = Environment(loader=PackageLoader(__name__,"templates"))   # 创建一个包加载器对象
        template = env.get_template('faleno.md')    # 获取一个模板文件
        temp_out = template.render(data = boxlist,title = str(title)) 
        #print(temp_out)  # 渲染
        return (temp_out)
#新作品页面
    def new_work(self):
        url = 'https://faleno.jp/top/work/'
        response = get_html_jp(url,verify=False)
        soup = BeautifulSoup(response,'lxml')
        title = soup.title.string
        body = soup.find('div',attrs = {'class' : 'box_kanren01'})
        results = body.find_all('div',attrs = {'class' : 'waku_kanren01'})
        boxlist = []
        for i in results:
            boxdict = {}
            liv = i.find('a')
            imgs = i.find('img')
            url = liv.get('href')
            boxdict['url'] = url
            name = imgs.get('alt')
            boxdict['name'] = name
            img = imgs.get('src')
            boxdict['img'] = img
            boxlist.append(boxdict)
        env = Environment(loader=PackageLoader(__name__,"templates"))   # 创建一个包加载器对象
        template = env.get_template('faleno.md')    # 获取一个模板文件
        temp_out = template.render(data = boxlist,title = str(title)) 
        #print(temp_out)  # 渲染
        return (temp_out)
        
if __name__ == '__main__':
    faleno = Faleno()
    faleno.search('天使もえ')
