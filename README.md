# iMulti-bot  2.0 beta
[![iMulti-Telegram BOT](https://img.shields.io/badge/iMulti-Telegram%20BOT-red?style=flat-square&logo=appveyor)](https://github.com/horryruo/multi-bot/)
[![Python 3.6](https://img.shields.io/badge/LANGUAGE-Python%203.6%2B-success?style=flat-square&logo=appveyor)](https://www.python.org/downloads/)
[![BSD-3](https://img.shields.io/badge/LICENSE-BSD3-brightgreen.svg)](https://github.com/horryruo/multi-bot/blob/master/LICENSE)

**发送命令到 [Telegram](http://telegram.org) BOT，以获得有关dmm、libray、ikoa、magnet的信息以及控制cloudflare api。**

**Send commands to [Telegram](http://telegram.org) BOT for get a information way which communicate with about dmm, libray, ikoa, magnet, and control cloudflare api compatibility!**  


## 免责声明：本代码仅用于学习，下载后请勿用于商业用途，本人对此有最终解释权。
## Disclaimer:  This code is only for learning, please do not use it for commercial purposes after downloading, I have the final right of interpretation.

## 更新|Update
**2021/1/17**      2.0beta——新增程序内更新，**需再执行**`pip3 install -r requirements.txt`，若不能实现还请继续手动更新。

**2021/1/12**      1.8beta——新增识别图鉴别女朋友功能，预计新增识别二次元图片寻找pixiv图片功能

**2020/12/24**     1.7beta——部分功能优化

**2020/12/17**     1.6beta——新增搜索dmm全站功能

**2020/11/19**     1.5.1beta

**2020/11/16**     1.5beta——增加利用selenium进行提取预览视频链接|add support find video with selenium(chromedriver 86.0.4240.22)

## 功能|Feature

1. 输入演员ID，即可获得该演员在dmm中的所有cid。| Enter the actor id to get all the cid of the actor in dmm.
2. 查询 "ikoa "中的影片参数(利用mahuateng)| Query the movie parameters in ikoa' video  (refer to mahuateng)
3. 输入javlibary演员网址，即可获得所有演员的编号。| Enter javlibary actor url to get all the actor's number.
4. 查询dmm cid信息、预览影片、预览图片。| Query the cid information in dmm alone, preview film, preview image
5. 在sukebei中按关键词搜索。| Search by keyword in sukebei's magnet
6. 根据关键词在dmm中搜索，最多30项。（video区或全站）| Search in dmm according to keywords and limit up to 30 items.
7. 输入dmm链接，列出所有项目。| Enter a list of dmm links to list all items.
8. 搜索当前dmm热门和最新电影，限制30条(测试版)| Search current dmm hot and newest movies, limit 30 (beta)
9. 控制cloudflare域名解析。| Control cloudflare domain resolution
10. 识别图片寻找相似度最高的女朋友。

## 安装|Install  
1. 需要python3.6以上版本| Python 3.6+ is Required  
2. 克隆项目（windows用户可直接github页面下载zip解压使用）| `git clone https://github.com/horryruo/multi-bot.git && chmod +x multi-bot && cd multi-bot`   
3. 安装依赖（pip3这个3取决与你的系统关联的python名字，比如系统python就等于python3，那么就不需要加这个3） | `pip3 install -r requirements.txt`
4. **安装google chrome** ，如不需要准确预览视频地址可不安装(本引擎是获取正确预览视频链接的关键，当没有安装chrome时，会进行正则规律类比获得链接，因此番号奇特以及年代久远的影片可能无法获取正确的链接，windows用户可自行谷歌下载安装最新版chrome) | install chrome (If you don't need accurate preview video function, you can skip it)  
   centos:`yum install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm`   
   debian or ubuntu:`wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && sudo apt install ./google-chrome-stable_current_amd64.deb`
5. 复制一份配置 | `cp config.ini.example config.ini` 
6. telegram内通过 **@BotFather**  创建机器人后获取token（具体也可以谷歌如何创建telegram机器人并获得token，教程很多），然后telegram内 私聊 **@get_id_bot**  获取chat id，获取的这两个都要填到下一步的配置文件里。
7. 根据配置文件描述配置设置（自行谷歌linux如何编辑文件，一般是使用vim或者nano） | &nbsp;Edit config.ini

### 开启|Start  
`python3 mybot.py`   （python3这个3取决与你的系统关联的python名字，比如系统python就等于python3，那么就不需要加这个3）

*具体使用时请向机器人输入"/help"获取命令使用指示。|Please type "/help" to the robot for specific use.*

### 后台运行|Start via screen  
   请先安装screen 
``screen -dmS multi-bot `which python3` mybot.py``  

### 更新|update
  1、直接telegram内发送命令/update根据提示更新（若无法更新请使用方法2）
  2、ctrl+z停止项目，使用screen的先`screen -r multi-bot`进入screen进程再停止。然后在项目文件夹`git pull`即可更新，然后再启动。本方法适用于只配置了config.ini而没有更改其他任何参与git的文件的用户，如果更改过，git pull会冲突，请谷歌如何git merge合并更新或删除项目再clone。

