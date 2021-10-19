# iMulti-bot  3.2 beta
[![iMulti-Telegram BOT](https://img.shields.io/badge/iMulti-Telegram%20BOT-red?style=flat-square&logo=appveyor)](https://github.com/horryruo/multi-bot/)
[![Python 3.6](https://img.shields.io/badge/LANGUAGE-Python%203.6%2B-success?style=flat-square&logo=appveyor)](https://www.python.org/downloads/)
[![BSD-3](https://img.shields.io/badge/LICENSE-BSD3-brightgreen.svg)](https://github.com/horryruo/multi-bot/blob/master/LICENSE)

**发送命令到 [Telegram](http://telegram.org) BOT，以获得有关dmm、libray、ikoa、magnet的信息以及控制cloudflare api。**

**Send commands to [Telegram](http://telegram.org) BOT for get a information way which communicate with about dmm, libray, ikoa, magnet, and control cloudflare api compatibility!**  


## 免责声明：本代码仅用于学习，下载后请勿用于商业以及违反使用者所在地法律用途，本人对此有最终解释权。
## Disclaimer:  This code is only for learning. Please do not use it for commercial purposes or violate the laws of the user’s location after downloading. I have the final right of interpretation.
<details>
<summary>
更新日志|Update log</summary>

**2021/10/19**     3.2beta——faleno增加部分没什么大用处的功能，在/help查看

**2021/10/18**     3.1beta——修复部分bug，新增从faleno获取video，photo(直接内嵌在原来到命令中)，以及搜索faleno

**2021/9/29**      添加了docker启动的方案，尚不完善，有bug请提issue，有能精简镜像的方法(目前400mb，包含了chrome,python,依赖库，具体看Dockerfile)也可以pr，具体安装方法请看下面。

**2021/9/27**      切换了main分支，更新时需要手动切换:先运行`git fetch` ,`git checkout -b main origin/main`,后`git branch`查看确认处在main分支，最后删除master分支`git branch -d master`

**2021/8/10**      3.0beta——重构程序结构(配置文件config.ini移动到了app/config/config.ini,直接启动程序会自动移动)，使得更加美观，更新chromedriver(92.0.4515.107),小bug修复，无大功能更新。

**2021/1/17**      2.0beta——新增程序内更新，**需再执行**`pip3 install -r requirements.txt`，若不能实现还请继续手动更新。

**2021/1/12**      1.8beta——新增识别图鉴别女朋友功能，预计新增识别二次元图片寻找pixiv图片功能

**2020/12/24**     1.7beta——部分功能优化

**2020/12/17**     1.6beta——新增搜索dmm全站功能

**2020/11/19**     1.5.1beta

**2020/11/16**     1.5beta——增加利用selenium进行提取预览视频链接|add support find video with selenium(chromedriver 86.0.4240.22)</details>

<details>
<summary>功能|Feature</summary>

1. 输入演员ID，即可获得该演员在dmm中的所有cid。| Enter the actor id to get all the cid of the actor in dmm.
2. 查询 "ikoa "中的影片参数(利用mahuateng)| Query the movie parameters in ikoa' video  (refer to mahuateng)
3. 输入javlibary演员网址，即可获得所有演员的编号。| Enter javlibary actor url to get all the actor's number.
4. 查询dmm cid信息、预览影片、预览图片。| Query the cid information in dmm alone, preview film, preview image
5. 在sukebei中按关键词搜索。| Search by keyword in sukebei's magnet
6. 根据关键词在dmm中搜索，最多30项。（video区或全站）| Search in dmm according to keywords and limit up to 30 items.
7. 输入dmm链接，列出所有项目。| Enter a list of dmm links to list all items.
8. 搜索当前dmm热门和最新电影，限制30条(测试版)| Search current dmm hot and newest movies, limit 30 (beta)
9. 控制cloudflare域名解析。| Control cloudflare domain resolution
10. 识别图片寻找相似度最高的女朋友。</details>

## 安装|Install  
1. 需要python3.6以上版本| Python 3.6+ is Required  
2. 克隆项目（windows用户可直接github页面下载zip解压使用）| `git clone https://github.com/horryruo/multi-bot.git && chmod +x multi-bot && cd multi-bot`   
3. 安装依赖（pip3这个3取决与你的系统关联的python名字，比如系统python就等于python3，那么就不需要加这个3） | `pip3 install -r requirements.txt`
4. **安装google chrome** ，如不需要准确预览视频地址可不安装(本引擎是获取正确预览视频链接的关键，当没有安装chrome时，会进行正则规律类比获得链接，因此番号奇特以及年代久远的影片可能无法获取正确的链接，windows用户可自行谷歌下载安装最新版chrome) | install chrome (If you don't need accurate preview video function, you can skip it)  
   centos:`yum install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm`   
   debian or ubuntu:`wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && sudo apt install ./google-chrome-stable_current_amd64.deb`
5. 复制一份配置 | `cp app/config/config.ini.example app/config/config.ini` 
6. telegram内通过 **@BotFather**  创建机器人后获取token（具体也可以谷歌如何创建telegram机器人并获得token，教程很多），然后telegram内 私聊 **@get_id_bot**  获取chat id，获取的这两个都要填到下一步的配置文件里。
7. 根据配置文件(在app/config/config.ini)描述配置设置（自行谷歌linux如何编辑文件，一般是使用vim或者nano） | &nbsp;Edit `vi app/config/config.ini`
8. 开启程序  `python3 mybot.py`   （python3这个3取决与你的系统关联的python名字，比如系统python就等于python3，那么就不需要加这个3）
9. 后台运行（请先安装screen ）  ``screen -dmS multi-bot `which python3` mybot.py``  
*具体使用时请向机器人输入"/help"获取命令使用指示。|Please type "/help" to the robot for specific use.*


## docker
（如果有能力自己安装python，安装chrome的，还是用上面的方法，本方法只适用于本来就喜欢用docker的人）
1. 你需要安装docker `curl -sSL https://get.docker.com/ | sh `,   `systemctl start docker`,   `systemctl enable docker`
2. 克隆项目`git clone https://github.com/horryruo/multi-bot.git && chmod +x multi-bot && cd multi-bot`   
3. 复制一份配置 | `cp app/config/config.ini.example app/config/config.ini` 
4. telegram内通过 **@BotFather**  创建机器人后获取token（具体也可以谷歌如何创建telegram机器人并获得token，教程很多），然后telegram内 私聊 **@get_id_bot**  获取chat id，获取的这两个都要填到下一步的配置文件里。
5. 根据配置文件(在app/config/config.ini)描述配置设置（自行谷歌linux如何编辑文件，一般是使用vim或者nano） | &nbsp;Edit `vi app/config/config.ini`
6. 开始运行 `docker run -d --name=multi-bot -v 你的项目目录:/bot horryruo/multi-bot` (命令中“你的项目目录”直接替换成你第三步克隆所在的绝对路径，假设克隆在/root/multi-bot,那么就是`docker run -d --name=multi-bot -v /root/multi-bot:/bot horryruo/multi-bot`)
 
 **看到这里你也发现了，如果你是第一次使用docker，并不比上面容易多少，甚至很多步骤都是差不多的，所以不熟悉的情况下还是建议使用上面的方法。**
### 如何更新程序 |update program
  1. 直接telegram内发送命令/update根据提示更新，更新完后/restart重启程序（若无法更新请使用方法2）
  
  2. ctrl+z停止项目，使用screen的先`screen -r multi-bot`进入screen进程再停止。然后在项目文件夹`git pull`即可更新，然后再启动。本方法适用于只配置了config.ini而没有更改其他任何参与git的文件的用户，如果更改过，git pull会冲突，输入`git reset --hard origin/main ` （本条命令将放弃本地所有更改）后再进行git pull。
   
  3. 用docker部署的更新依旧是来到克隆目录下`git pull`或者程序内更新后`docker restart multi-bot`即可，因为docker镜像只打包了运行环境，项目文件直接映射在宿主机上。
