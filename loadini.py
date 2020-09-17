import configparser
def read_config():

    config = configparser.ConfigParser()
    config.read("config.ini", encoding='utf-8')
    ifproxy = config['default']['ifproxy']
    proxy = config['default']['proxy']
    token = config['default']['tgtoken']
    userid = config['default']['userid']
    if ifproxy == 'True':
        ifproxy = True
    elif ifproxy == 'False':
        ifproxy = False
    else:
        print('配置文件proxy项出错')
    return (ifproxy,proxy,token,userid)
    
def read_config_cf():
    config = configparser.ConfigParser()
    config.read("config.ini", encoding='utf-8')
    email = config['cloudflare']['email']
    globalkey = config['cloudflare']['globalkey']
    return (email,globalkey)


if __name__ == '__main__':
    ifproxy,proxy,token = read_config_default()
    print(ifproxy,proxy,token)