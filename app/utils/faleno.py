from app.utils.func_requests import get_html_jp
from bs4 import BeautifulSoup
from jinja2 import PackageLoader,Environment
import re
class Faleno(object):
    def __init__(self):
        pass

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
        try:
            ifresult = re.findall(r'に一致する作品は見つかりませんでした',soup)
            noresult = '没有找到匹配的作品'
        except:
            pass
        try:
            if ifresult:
                return noresult
        except:
            pass
        results = soup.find_all('div',attrs = {'class' : 'waku_kanren01'})
        title = soup.find('section',attrs = {'class' : 'bread'}).p.contents[1]
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
        
if __name__ == '__main__':
    faleno = Faleno()
    faleno.search('天使もえ')