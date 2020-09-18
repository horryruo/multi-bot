# Multi-bot  1.1 beta
![multi-Telegram BOT](https://img.shields.io/badge/multi-Telegram%20BOT-red?style=flat-square&logo=appveyor)
![Python 3.6](https://img.shields.io/badge/LANGUAGE-Python%203.6%2B-success?style=flat-square&logo=appveyor)

**Send commands to [Telegram](http://telegram.org) BOT for get a _convience way communicate with_ get information about dmm, javlibray, ikoa, magnet, and control cloudflare api compatibility!**  

## Install  
1. Python 3.6+ is Required  
2. `git clone https://github.com/horryruo/multi-bot.git && cd multi-bot` 
3. `chmod +x multi-bot`  
4. `pip3 install -r requirements.txt`  
5. cp config.ini.example config.ini`  
6. &nbsp;Edit config.ini

### Start  
`python3 mybot.py` 

*Please type "/help" to the robot for specific use.*

### Start via screen  

``screen -dmS multi-bot `which python3` mybot.py``  

#### Feature
1. Enter the actor id to get all the cid of the actor in dmm.
2. Query the movie parameters in ikoa (refer to mahuteng)
3. Enter javlibary actor url to get all the actor's number.
4. query the cid information in dmm alone, preview film, preview image
5. Search by keyword in sukebei's magnetism
6. Search in dmm according to keywords and limit up to 30 items.
7. Enter a list of dmm links to list all items.
8. Search current dmm hot and newest movies, limit 30 (beta)
9. Control cloudflare domain resolution

