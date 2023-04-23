import hashlib
import json
from time import sleep
import requests
import os


def login(phone, passwd):
    print(phone)
    _url = 'https://opapi.nnraytheon.com/u-mobile/pwdLogin'
    _data = {
        "countryCode": 86,
        "telNum": phone,
        "pwdEncry": hashlib.md5(bytes(passwd, encoding='utf-8')).hexdigest()
    }
    headers = {
        "Host": "opapi.nnraytheon.com",
        "token": "",
        "appid": "nnMobileIm_6z0g3ut7",
        "timestamp": "1675096362942",
        "signtype": "1",
        "sign": "",
        "version": "108",
        "reqchannel": "2",
        "deviceid": "d4uud558697ada1ec",
        "appname": "leigod_accelerator",
        "osversion": "12",
        "longitude": "0.0",
        "latitude": "0.0",
        "platform": "2",
        "registercanal": "common",
        "busitype": "nn_aksjfdasoifnkls",
        "content-type": "application/json; charset=UTF-8",
        "content-length": "87",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.9.3"
    }
    login_status = requests.post(url=_url, data=json.dumps(_data), headers=headers).json()
    print(login_status['retMsg'])
    if login_status['retMsg'] != '该用户不存在':
        # print(login_status['retData']['userId'])
        headers['token'] = login_status['retData']['token']
        _data = {
            "taskIds": [
                24,
                16,
                29,
                30
            ],
            "userId": login_status['retData']['userId']
        }
        get_num = \
            requests.post(url='https://opapi.nnraytheon.com/nn-assist/taskPoints/findUserTaskInfo', data=json.dumps(_data),
                          headers=headers).json()['retData']
        #print(get_num)
        for i in get_num:
            for e in range(10):
                #print(e)
                # print(i['taskId'])
                _data = {
                    "point": 1,
                    "taskId": i['taskId'],
                    "taskName": "",
                    "userId": login_status['retData']['userId']
                }
                result = requests.post(url='https://opapi.nnraytheon.com/nn-assist/taskPoints/pointCallBack',
                                       data=json.dumps(_data), headers=headers).json()
                print(result['retMsg'])
                if result['retMsg'] == '当天完成任务已上限':
                    break
                else:
                    sleep(0)
                    pass


login(os.environ['nn_user'], os.environ['nn_pwd'])
#print(os.environ['nn_user'])
#input()
