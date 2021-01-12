from function_requests import post_photo
import json, re
from bs4 import BeautifulSoup
from jinja2 import PackageLoader,Environment

def girl():
    url = 'https://xslist.org/search/pic'
    image = {'pic':open('user_photo.jpg','rb'),'lg':'en'}
    html = post_photo(url,image)
    soup = BeautifulSoup(html,'lxml')
    try:
        ifresult = re.findall(r'(pic not has face)', html)
        noresult = 'pic not has face'
        if noresult in ifresult:
            return noresult
    except:
        pass

    searchbody = soup.find_all('li',attrs = {'class' : 'clearfix'})
    boxlist = []
    for i in searchbody:
        boxdict = {}
        if i:
            title = re.findall(r'<a href=\".*?\" target=\"_blank\" title=\".*?\">(.*?)</a>',str(i))[0]
            links = re.findall(r'<a href=\"(.*?)\" target=\"_blank\" title=\".*?\">.*?</a>',str(i))[0]
            #img = re.findall(r'img src=\"(.*?)\"',str(i))[0]
            boxdict['title'] = title
            boxdict['links'] = links
            #boxdict['img'] = img
            boxlist.append(boxdict)

    env = Environment(loader=PackageLoader('identify','templates'))    # 创建一个包加载器对象
    template = env.get_template('face_girl.md')    # 获取一个模板文件
    temp_out = template.render(resultdata = boxlist) 
    #print(temp_out)  # 渲染
    return temp_out

def acg():
    url = 'https://saucenao.com/search.php'
    image = {'file': open('user_photo.jpg', 'rb'), 'url': '', 'frame': 1, 'hide': 0, 'database': 999}
    html = post_photo(url,image)
    soup = BeautifulSoup(html,'lxml')


    searchbody = soup.find_all('div',attrs = {'class' : 'result'})
    #print(searchbody)
    boxlist = []
    for i in searchbody:
        boxdict = {}
        if i:
            title = re.findall(r'<div class=\"resulttitle\"><strong>(.*?)</strong>',str(i))
            similar = re.findall(r'<div class=\"resultsimilarityinfo\">(.*?)</div>',str(i))
            pixivlink = re.findall(r'<strong>Pixiv ID: </strong><a href=\"(.*?)\" class=\"linkify\">.*?</a>',str(i))
            pixivid = re.findall(r'<strong>Pixiv ID: </strong><a href=\".*?\" class=\"linkify\">(.*?)</a>',str(i))
            painter = re.findall(r'<strong>Member: </strong><a href=\".*?\" class=\"linkify\">(.*?)</a>',str(i))
            painterlink = re.findall(r'<strong>Member: </strong><a href=\"(.*?)\" class=\"linkify\">.*?</a>',str(i))
            boxdict['title'] = title
            boxdict['similar'] = similar
            boxdict['pixivlink'] = pixivlink
            boxdict['pixivid'] = pixivid
            boxdict['painter'] = painter
            boxdict['painterlink'] = painterlink
            boxlist.append(boxdict)
    
    print(boxlist)
if __name__ == "__main__":
    #girl()
    acg()