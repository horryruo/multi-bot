import requests
import json
import datetime
import prettytable as pt
from loadini import read_config_cf,read_config
'''
https://api.cloudflare.com/#
'''
allconfig = read_config()
ifproxy = allconfig['ifproxy'] 
proxy = allconfig['proxy'] 

email,globalkey = read_config_cf()
proxies = {'http': 'http://%s'%proxy, 'https': 'http://%s'%proxy}

class CloudFlare(object):
    def __init__(self, email, token):

        
        self.EMAIL = email
        self.TOKEN = token
        self.headers = {"X-Auth-Email": email, "X-Auth-Key": token, "Content-Type": "application/json"}
        self.proxies = proxies
        self.s = requests.session()

    class APIError(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return self.value

    def api_call(self, method, endpoint, params=None):
        url = 'https://api.cloudflare.com/client/v4/' + endpoint
        method = method.lower()
        requests_method = getattr(self.s, method)
        #print(url)
        if ifproxy == 'true':
            response = requests_method(url, headers=self.headers, proxies = self.proxies, data=json.dumps(params) if params else None)
        else:
            response = requests_method(url, headers=self.headers, data=json.dumps(params) if params else None)
        data = response.text
        
        
        try:
            data = json.loads(data)
        except ValueError:
            raise self.APIError('JSON parse failed.')
        if data.get('error') :
            raise self.APIError(data['error'])
        
                
        
        return data

    def get(self, zone_id='', endpoint='', params=None):
        return self.api_call('GET', 'zones/' + zone_id + '/' + endpoint, params)

    def post(self, zone_id='', endpoint='', params=None):
        return self.api_call('POST', 'zones/' + zone_id + '/' + endpoint, params)

    def put(self, zone_id='', endpoint='', params=None):
        return self.api_call('PUT', 'zones/' + zone_id + '/' + endpoint, params)

    def delete(self, zone_id='', endpoint='', params=None):
        return self.api_call('DELETE', 'zones/' + zone_id + '/' + endpoint, params)

    def create_zones(self, z):
        data = {
            "name": z,
            "jump_start": False
        }
        return self.post(params=data)

    def delete_zones(self, zone_id):
        return self.delete(zone_id=zone_id)

    def list_zones(self):
        return self.get()

    def get_zone_by_name(self, z):
        data = self.list_zones()
        for item in data['result']:
            if z == item['name']:
                return item

    def get_zone_id(self, name):
        zone = self.get_zone_by_name(name)
        return zone['id']

    def rec_new(self, zone, _type, name, content, proxied=False, ttl=1):
        zone_id = self.get_zone_id(zone)
        data = {
            "type": _type,
            "name": name,
            "content": content,
            "proxiable": True,
            "proxied": proxied,
            "ttl": ttl
        }
        return self.post(zone_id, 'dns_records', data)

    def get_dns(self, z, name):
        # zone_id = self.get_zone_id(z)
        recs = self.rec_list(z)
        for dns in recs['result']:
            #if dns['name'] == name if name == z else name + "." + z:
            if dns['name'] == name + "." + z:
                return dns

    def rec_list(self, z):
        _id = self.get_zone_id(z)
        return self.get(_id, 'dns_records')

    def rec_detail(self, z, name):
        dns = self.get_dns(z, name)
        return self.get(dns['zone_id'], 'dns_records/' + dns['id'])

    def rec_delete(self, z, name):
        dns = self.get_dns(z, name)
        return self.delete(dns['zone_id'], 'dns_records/' + dns['id'])

    def rec_edit(self, z, _type, name, content, proxied, ttl=1):
        dns = self.get_dns(z, name)
        data = {
            "id": dns['id'],
            "type": _type,
            "name": name,
            "content": content,
            "proxiable": True,
            "proxied": proxied,
            "ttl": ttl,
            "locked": False,
            "zone_id": dns['zone_id'],
            "zone_name": z
        }
        return self.put(dns['zone_id'], 'dns_records/' + dns['id'], data)




class CloudFlare_handler(object):
    def  __init__(self, context):
        self.context = context
        self.cfapi = CloudFlare(email, globalkey)
        
        
    def option(self):
        option = self.context[0]
        args = self.context[1:]
        if option == 'ls':
            return self.lszone()
        elif option == 'dns':
            return self.loaddns(args)
        elif option == 'add':
            return self.adddns(args)
        elif option == 'del':
            return self.deletedns(args)
        elif option == 'edit':
            return self.editdns(args)
        else:
            error = '指令错误'
            return error
    def lszone(self):
        result = self.cfapi.list_zones()
        zone = []
        for item in result['result']:
            zone.append(item['name'])
        zone = '||'.join(zone)
        return zone 
                
    def loaddns(self,args):
        if len(args) == 1:
            args = ''.join(args)
            result = self.cfapi.rec_list(args)
        else:
            error = '参数不符合标准'
            return error
        tb = pt.PrettyTable()
        tb.left_padding_width = 0
        tb.right_padding_width = 0
        #tb.set_style(pt.MSWORD_FRIENDLY)
        tb.field_names = ["name", "type", "records"]
        for id in result['result']:
            tb.add_row([id['name'],id['type'],id['content']])
            #print(str(id['name']),str(id['type']),str(id['content']),str(id['ttl']))
        tbb = tb.get_string()
        return tbb

    def adddns(self,args):

        type = args[0]
        allname = args[1]
        content = args[2]
        part = allname.split('.')
        #print(part)
        name = part[0]
        zone = '.'.join(part[1:])
        
        #print(type,name,zone,content)
        
        try:
            result = self.cfapi.rec_new(zone, type, name, content)
            #print(result)
        except:
            error = '参数不符合标准'
            return  error
        if result['success'] == True:
            result1 = result['result']
            text = '域名{}成功创建{}记录，主机名:{};云朵{}，ttl:{}'.format(result1['name'],result1['type'],result1['content'],result1['proxied'],result1['ttl'])
            return text
        else:
            error = result['errors']
            msg = error[0]['message']
            #print(error,msg)
            return msg
        
    
    def deletedns(self,args):
        allname = args[0]
        part = allname.split('.')
        name = part[0]
        zone = '.'.join(part[1:])
       
        try:
            result = self.cfapi.rec_delete(zone,name)
            print(result)
        except:
            error = '域名不存在或参数不符合标准'
            return  error
        if result['success'] == True:
            result1 = result['result']
            text = '成功删除域名{}，id:{}'.format(allname,result1['id'])
            return text
        
    def editdns(self,args):
        type = args[0]
        allname = args[1]
        content = args[2]
        part = allname.split('.')
        #print(part)
        name = part[0]
        zone = '.'.join(part[1:])
        try:
            dnsold = self.cfapi.get_dns(zone, name)
            proxied = dnsold['proxied']

        except:
            pass
        if args[3:] == []:
            mode = 1 
        else:
            optionmode = args[3:]
            mode = 2
        
        if mode == 2:
            if optionmode[0] == 'cloudon':
                proxied = True
            elif optionmode[0] == 'cloudoff':
                proxied = False
                
        try:
            
            result = self.cfapi.rec_edit(zone, type, name, content,proxied)
            #print(dnsold)
            #print(result)
        except:
            error = '参数不符合标准'
            return  error
        if result['success'] == True:
            result1 = result['result']
            textold = '修改前域名 {} : {} 记录，主机名: {} ;云朵{}，ttl:{}'.format(dnsold['name'],dnsold['type'],dnsold['content'],dnsold['proxied'],dnsold['ttl'])
            text = '======>成功修改域名 {} : {} 记录，修改后主机名: {} ;云朵{}，ttl:{}'.format(result1['name'],result1['type'],result1['content'],result1['proxied'],result1['ttl'])
            text1 = textold + text
            return text1
        else:
            error = result['errors']
            msg = error[0]['message']
            #print(error,msg)
            return msg

if __name__ == '__main__':
    
    
    print('1')
    