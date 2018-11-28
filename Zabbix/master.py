# from Zabbix.models import Zabbix as Zabbix_models
import requests, json
from Lemon.settings import ZABBIX_SETTING

class ZabbixMaster(object):

    def __init__(self):
        super(ZabbixMaster, self).__init__()
        self.headers = {
            "Content-Type": "application/json-rpc"
        }
        print(ZABBIX_SETTING)
        self.url = ZABBIX_SETTING['home_url'] + '/zabbix/web/api_jsonrpc.php'
        self.username = ZABBIX_SETTING['username']
        self.password = ZABBIX_SETTING['password']
        # self.get_token()

    # 获取zabbix token
    def get_token(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 1
        }
        print(data)
        print(self.url)
        response = requests.post(url=self.url, data=json.dumps(data), headers=self.headers)
        # print(response.json())
        return response.json()['result']

    # 拼接数据格式

    def format_alerts(self, alerts):
        # print(alerts)
        alerts_list = []
        for alert in alerts['result']:
            alerts_dict = {
                'hostname': alert['hosts'][0]['name'] ,
                'lastvalue': alert['items'][0]['lastvalue'],
                'priority': alert['priority']
            }

            if(alert['items'][0]['units'] == 'B'):
                alerts_dict['description'] = alert['description'] + "（" + str(int(alert['items'][0]['lastvalue']) / 1000000).split('.')[0] + " MB" + "）"
            elif(alert['items'][0]['units'] == '%'):
                alerts_dict['description'] = alert['description'] + "（" + str(alert['items'][0]['lastvalue']).split('.')[0] + " %" + "）"
            else:
                alerts_dict['description'] = alert['description'] + alert['items'][0]['units']
            alerts_list.append(alerts_dict)
        print(alerts_list)
        return alerts_list

    # 获取当前报警
    def get_alerts(self):
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": ["description", "last_change_time", "priority", "lastchange"],
                "filter": {
                    "value": 1,
                    "status": 0
                },
                "sortfield": "lastchange",
                "selectHosts": ["name"],
                "selectItems": ["lastvalue", "units"]
                #"selectItems": "extend"
            },
            "auth":  self.get_token(),
            "id": 1
        }
        response = requests.post(url=self.url, data=json.dumps(data), headers=self.headers)
        print(json.dumps(response.json()))
        # print(len(response.json()['result']))
        # print(response.json())
        # self.format_alerts(response.json())
        return self.format_alerts(response.json())

#
# Z = ZabbixMaster()
# Z.get_alerts()