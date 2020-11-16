# iMulti-bot  1.4 beta
[![iMulti-Telegram BOT](https://img.shields.io/badge/iMulti-Telegram%20BOT-red?style=flat-square&logo=appveyor)](https://github.com/horryruo/multi-bot/)
[![Python 3.6](https://img.shields.io/badge/LANGUAGE-Python%203.6%2B-success?style=flat-square&logo=appveyor)](https://www.python.org/downloads/)
[![BSD-3](https://img.shields.io/badge/LICENSE-BSD3-brightgreen.svg)](https://github.com/horryruo/multi-bot/blob/master/LICENSE)

**Send commands to [Telegram](http://telegram.org) BOT for get a information way which communicate with about dmm, libray, ikoa, magnet, and control cloudflare api compatibility!**  


## 免责声明：本代码仅用于学习，下载后请勿用于商业用途，本人对此有最终解释权。
## Disclaimer:  This code is only for learning, please do not use it for commercial purposes after downloading, I have the final right of interpretation.

## Update
**2020/11/16** add support find video with selenium(chromedriver 86.0.4240.22)

## Feature
1. Enter the actor id to get all the cid of the actor in dmm.
2. Query the movie parameters in ikoa' video  (refer to mahuteng)
3. Enter javlibary actor url to get all the actor's number.
4. query the cid information in dmm alone, preview film, preview image
5. Search by keyword in sukebei's magnet
6. Search in dmm according to keywords and limit up to 30 items.
7. Enter a list of dmm links to list all items.
8. Search current dmm hot and newest movies, limit 30 (beta)
9. Control cloudflare domain resolution


## Install  
1. Python 3.6+ is Required  
2. `git clone https://github.com/horryruo/multi-bot.git && chmod +x multi-bot` 
3. `cd multi-bot`  
4. `pip3 install -r requirements.txt`
5. install chrome (If you don't need accurate preview video function, you can skip it)  
   centos:`yum install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm`   
   debian or ubuntu:`wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && sudo apt install ./google-chrome-stable_current_amd64.deb`
6. `cp config.ini.example config.ini` 
7. &nbsp;Edit config.ini

### Start  
`python3 mybot.py` 

*Please type "/help" to the robot for specific use.*

### Start via screen  

``screen -dmS multi-bot `which python3` mybot.py``  



