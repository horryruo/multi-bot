import configparser
import platform
import os, shutil
if os.path.exists(os.path.abspath(os.path.join("config.ini"))):
    shutil.move(os.path.abspath(os.path.join("config.ini")),os.path.abspath(os.path.join("app", "config","config.ini")))
configfile = os.path.abspath(os.path.join("app", "config","config.ini"))
def read_config():
    config = configparser.ConfigParser()
    config.read(configfile, encoding='utf-8')
    ifproxy = config['default']['ifproxy']
    proxy = config['default']['proxy']
    token = config['default']['tgtoken']
    userid = config['default']['userid']
    tb = config['default']['tb']
    system = platform.system()
    allconfig = {}
    allconfig['ifproxy'] = ifproxy
    allconfig['tb'] = tb
    allconfig['proxy'] = proxy
    allconfig['token'] = token
    allconfig['userid'] = userid
    allconfig['system'] = system
    return allconfig
    
def read_config_cf():
    config = configparser.ConfigParser()
    config.read(configfile, encoding='utf-8')
    email = config['cloudflare']['email']
    globalkey = config['cloudflare']['globalkey']
    return (email,globalkey)
    

if __name__ == '__main__':
    allconfig = read_config()
    print(allconfig)
    #print(os.path.abspath(os.path.join("app", "config","config.ini")))
    #print(os.path.join(os.getcwd(),"app", "config","config.ini"))