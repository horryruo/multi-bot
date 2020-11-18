# iMulti-bot  1.5 beta
[![iMulti-Telegram BOT](https://img.shields.io/badge/iMulti-Telegram%20BOT-red?style=flat-square&logo=appveyor)](https://github.com/horryruo/multi-bot/)
[![Python 3.6](https://img.shields.io/badge/LANGUAGE-Python%203.6%2B-success?style=flat-square&logo=appveyor)](https://www.python.org/downloads/)
[![BSD-3](https://img.shields.io/badge/LICENSE-BSD3-brightgreen.svg)](https://github.com/horryruo/multi-bot/blob/master/LICENSE)

**发送命令到 [Telegram](http://telegram.org) BOT，以获得有关dmm、libray、ikoa、magnet的信息以及控制cloudflare api。**

**Send commands to [Telegram](http://telegram.org) BOT for get a information way which communicate with about dmm, libray, ikoa, magnet, and control cloudflare api compatibility!**  


## 免责声明：本代码仅用于学习，下载后请勿用于商业用途，本人对此有最终解释权。
## Disclaimer:  This code is only for learning, please do not use it for commercial purposes after downloading, I have the final right of interpretation.

## 更新|Update
**2020/11/16**     1.5beta---增加利用selenium进行提取资源|add support find video with selenium(chromedriver 86.0.4240.22)

## 功能|Feature
 
1. 输入演员ID，即可获得该演员在dmm中的所有cid。| Enter the actor id to get all the cid of the actor in dmm.
2. 查询 "ikoa "中的影片参数(利用mahuteng)| Query the movie parameters in ikoa' video  (refer to mahuteng)
3. 输入javlibary演员网址，即可获得所有演员的编号。| Enter javlibary actor url to get all the actor's number.
4. 查询dmm cid信息、预览影片、预览图片。| Query the cid information in dmm alone, preview film, preview image
5. 在sukebei中按关键词搜索。| Search by keyword in sukebei's magnet
6. 根据关键词在dmm中搜索，最多限制30项。| Search in dmm according to keywords and limit up to 30 items.
7. 输入dmm链接，列出所有项目。| Enter a list of dmm links to list all items.
8. 搜索当前dmm热门和最新电影，限制30条(测试版)| Search current dmm hot and newest movies, limit 30 (beta)
9. 控制cloudflare域名解析。| Control cloudflare domain resolution


## 安装|Install  
1. 需要python3.6以上版本| Python 3.6+ is Required  
2. 克隆项目| `git clone https://github.com/horryruo/multi-bot.git && chmod +x multi-bot && cd multi-bot`   
3. 安装依赖 | `pip3 install -r requirements.txt`
4. 安装google chrome ，如不需要准确预览影片地址可不安装 | install chrome (If you don't need accurate preview video function, you can skip it)  
   centos:`yum install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm`   
   debian or ubuntu:`wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && sudo apt install ./google-chrome-stable_current_amd64.deb`
5. 复制一份配置 | `cp config.ini.example config.ini` 
6. 根据配置文件描述配置设置 | &nbsp;Edit config.ini

### 开启|Start  
`python3 mybot.py` 

*具体使用时请向机器人输入"/help"获取命令使用指示。|Please type "/help" to the robot for specific use.*

### 后台运行|Start via screen  
   请先安装screen 
``screen -dmS multi-bot `which python3` mybot.py``  



