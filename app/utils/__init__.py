import configparser
import platform
import os, shutil

class Loadconfig():
    if os.path.exists(os.path.abspath(os.path.join("config.ini"))):
        shutil.move(os.path.abspath(os.path.join("config.ini")),os.path.abspath(os.path.join("app", "config","config.ini")))
    configfile = os.path.abspath(os.path.join("app", "config","config.ini"))
    config = configparser.ConfigParser()
    config.read(configfile, encoding='utf-8')
        
    ifproxy = config['default']['ifproxy']
    proxy = config['default']['proxy']
    TOKEN = config['default']['tgtoken']
    userid = config['default']['userid']
    iftb = config['default']['tb']
    system = platform.system()
    
    email = config['cloudflare']['email']
    globalkey = config['cloudflare']['globalkey']
        


        
        
        
