import configparser
import platform
def read_config():

    config = configparser.ConfigParser()
    config.read("config.ini", encoding='utf-8')
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
    config.read("config.ini", encoding='utf-8')
    email = config['cloudflare']['email']
    globalkey = config['cloudflare']['globalkey']
    return (email,globalkey)
    

if __name__ == '__main__':
    ifproxy,proxy,token = read_config_default()
    print(ifproxy,proxy,token)