# iMulti-bot  1.1 beta
[![iMulti-Telegram BOT](https://img.shields.io/badge/iMulti-Telegram%20BOT-red?style=flat-square&logo=appveyor)](https://github.com/horryruo/multi-bot/)
[![Python 3.6](https://img.shields.io/badge/LANGUAGE-Python%203.6%2B-success?style=flat-square&logo=appveyor)](https://www.python.org/downloads/)
[![BSD-3](https://img.shields.io/badge/LICENSE-BSD 3-brightgreen.svg)](https://github.com/horryruo/multi-bot/blob/master/LICENSE)

**Send commands to [Telegram](http://telegram.org) BOT for get a information way which communicate with about dmm, javlibray, ikoa, magnet, and control cloudflare api compatibility!**  

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
2. `git clone https://github.com/horryruo/multi-bot.git && cd multi-bot` 
3. `chmod +x multi-bot`  
4. `pip3 install -r requirements.txt`  
5. `cp config.ini.example config.ini` 
6. &nbsp;Edit config.ini

### Start  
`python3 mybot.py` 

*Please type "/help" to the robot for specific use.*

### Start via screen  

``screen -dmS multi-bot `which python3` mybot.py``  



