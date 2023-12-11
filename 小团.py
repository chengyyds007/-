"""
time：2023.12.02
定时：一天一次就行了
new Env('彼得小团币')
抓包小程序或者app或者网页的token=Agxxxx  只要token后面的值
环境变量: 名称：bd_mttoken   值：Agxxxxxxxxxx#fingerprint的值
用 # 分割两个参数。没有fingerprint的值只跑签到那些任务。
多账号新建变量或者用 & 分开
并发变量: bd_xtbbf  默认不设置为1

"""
import json
import random
import base64
import os
import string
from datetime import datetime
import requests
import time
from functools import partial
from user_agent import generate_user_agent
import concurrent.futures

# 自定义变量名
blname = 'bd_mttoken'

# 是否打印详细日志 True/False
isprint = False

# 最大状态3大于这个数字就不跑，慎用!!! 如果指纹没问题，设置成100，看能不能跑。
max_zt3 = 10


class Mttb:
    def __init__(self, zh, ck):
        if "#" in ck:
            self.ck = ck.split("#")[0]
            self.fingerprint = ck.split("#")[1].replace("\n", "").replace("\\", "")
        else:
            self.ck = ck
            self.fingerprint = ''
        self.uuid = None
        self.lisss = None
        self.lastGmtCreated = None
        self.qdrwids = [10002, 10024, 10041, 10015, 100]
        self.qdid = None
        self.llid = None
        self.startmsg = ''
        self.endmsg = ''
        self.llids = []
        self.qdactoken = None
        self.num = zh
        self.xtb = None
        self.wcxtb = None
        self.t_h = None
        self.actoken = None
        self.usid = None
        self.name = None
        self.ua = generate_user_agent(os='android')
        self.msg = ""
        self.ids = []
        self.noids = [420, 421, 422, 423, 424, 15169, 15170, 15171, 15172, 15173]
        self.id = None
        self.tid = None
        self.data_list = None
        self.login = None
        self.mtbb = 'meituan'

    def sq_login(self):
        try_count = 5
        while try_count > 0:
            try:
                url = "http://bedee.top:1250/tbyz"
                headers = {'Content-Type': 'application/json'}
                data = {
                    'token': self.ck,
                    'ua': self.ua
                }
                r = requests.post(url, headers=headers, json=data)
                ffmsg = r.json().get('msg', None)
                if '成功' in r.text and self.ck in r.text:
                    rj = r.json()
                    dlzt = rj['msg']
                    self.name = rj['name']
                    self.usid = rj['usid']
                    sj = rj['expirytime']
                    self.uuid = rj['uuid']
                    if self.fingerprint != '':
                        self.startmsg += f'🆔账号{self.num}-{self.name}({self.usid}) ✅{dlzt}\n⏰授权到期时间：{sj}\n✅已添加指纹\n'
                        return True
                    else:
                        self.startmsg += f'🆔账号{self.num}-{self.name}({self.usid}) ✅{dlzt}\n⏰授权到期时间：{sj}\n⛔️未添加指纹\n'
                        return True
                elif self.ck not in r.text:
                    self.startmsg += f'🆔账号{self.num} 登录返回错误，还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(2, 5))
                    continue
                else:
                    print(f'🆔账号{self.num} 登录失败：{ffmsg}\n')
                    return False
            except:
                self.startmsg += f'🆔账号{self.num} 登录异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(2, 5))
                continue

    def km_login(self):
        try_count = 5
        while try_count > 0:
            try:
                url = "http://bedee.top:1252/tbyz"
                headers = {'Content-Type': 'application/json'}
                data = {
                    'token': self.ck,
                    'ua': self.ua,
                    'km': km
                }
                r = requests.post(url, headers=headers, json=data)
                ffmsg = r.json().get('msg', None)
                if '登录成功' in r.text and self.ck in r.text and '卡密次数不足' not in r.text:
                    rj = r.json()
                    dlzt = rj['msg']
                    self.name = rj['name']
                    self.usid = rj['usid']
                    self.uuid = rj['uuid']
                    if self.fingerprint != '':
                        self.startmsg += f'🆔账号{self.num}-{self.name}({self.usid}) ✅{dlzt}\n✅已添加指纹\n'
                    else:
                        self.startmsg += f'🆔账号{self.num}-{self.name}({self.usid}) ✅{dlzt}\n⛔️未添加指纹\n'
                    self.startmsg += f''
                    return True
                elif '卡密次数不足' in r.text or '卡密验证失败' in r.text:
                    rj = r.json()
                    dlzt = rj['msg']
                    self.name = rj['name']
                    self.usid = rj['usid']
                    self.startmsg += f'🆔账号{self.num}-{self.name}({self.usid}) ✅{dlzt}\n'
                    return False
                elif self.ck not in r.text:
                    self.startmsg += f'🆔账号{self.num} 登录返回错误，还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(2, 5))
                    continue
                else:
                    print(f'🆔账号{self.num} 登录失败：{ffmsg}\n')
                    return False
            except:
                self.startmsg += f'🆔账号{self.num} 登录异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(2, 5))
                continue

    def act(self):
        try:
            url = 'https://game.meituan.com/mgc/gamecenter/front/api/v1/login'
            h = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Length': '307',
                'x-requested-with': 'XMLHttpRequest',
                'User-Agent': self.ua,
                'Content-Type': 'application/json;charset=UTF-8',
                'cookie': f'token={self.ck};uuid={self.uuid}'
            }
            sing = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            data = {
                "mtToken": self.ck,
                "deviceUUID": self.uuid,
                "mtUserId": self.usid,
                "idempotentString": sing
            }
            r = requests.post(url, headers=h, json=data)
            if r.json()['data']['loginInfo']['accessToken'] is not None:
                self.actoken = r.json()['data']['loginInfo']['accessToken']
            else:
                print(f'🆔账号{self.num}-{self.name}>>>获取actoken失败：{r.json()}')
        except Exception as e:
            print(f'🆔账号{self.num}-{self.name}>>>获取actoken异常：{e}')
            exit(0)

    def get_ids(self):
        try:
            url = 'https://game.meituan.com/mgc/gamecenter/front/api/v1/mgcUser/task/queryMgcTaskInfo?yodaReady=h5&csecplatform=4&csecversion=2.3.1'
            data = {
                'externalStr': '',
                'riskParams': {
                    'uuid': self.uuid,
                }
            }
            h = {
                'Accept': 'application/json, text/plain, */*',
                'x-requested-with': 'XMLHttpRequest',
                'User-Agent': self.ua,
                'Content-Type': 'application/json;charset=UTF-8',
                'actoken': self.actoken,
                'mtoken': self.ck,
                'cookie': f'token={self.ck};uuid={self.uuid}'
            }
            r = requests.post(url, headers=h, json=data)
            rj = r.json()
            # print(rj)
            if rj['msg'] == 'ok' and r.json()['data']['taskList'] != []:
                self.data_list = r.json()['data']['taskList']
                return True
            else:
                return False
        except Exception as e:
            print(f'🆔账号{self.num}-{self.name}>>>获取任务异常：{e}')
            exit(0)

    def startcxtb(self):
        try_count = 5
        while try_count > 0:
            try:
                url = 'https://game.meituan.com/mgc/gamecenter/skuExchange/resource/counts?sceneId=3&gameId=10102'
                self.t_h = {
                    'User-Agent': self.ua,
                    'actoken': self.actoken,
                    'mtoken': self.ck,
                    'cookie': f'token={self.ck};uuid={self.uuid}'
                }
                r = requests.get(url, headers=self.t_h)
                rj = r.json()
                if rj['msg'] == 'ok':
                    data = rj['data']
                    for d in data:
                        self.xtb = d['count']
                        self.startmsg += f'🎁运行前小团币: {int(self.xtb)}({int(self.xtb) / 1000}元)\n'
                    return True
                else:
                    self.startmsg += f'🆔账号{self.num}-{self.name} 查询运行前团币失败：还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(3, 8))
                    continue
            except:
                self.startmsg += f'🆔账号{self.num}-{self.name} 查询运行前团币异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def endcxtb(self):
        try_count = 5
        while try_count > 0:
            try:
                url = 'https://game.meituan.com/mgc/gamecenter/skuExchange/resource/counts?sceneId=3&gameId=10102'
                # self.t_h = {
                #     'User-Agent': self.ua,
                #     'actoken': self.actoken,
                #     'mtoken': self.ck,
                #     'cookie': f'token={self.ck}'
                # }
                self.t_h = {
                    'Accept': 'application/json, text/plain, */*',
                    'x-requested-with': 'XMLHttpRequest',
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json;charset=UTF-8',
                    'actoken': self.actoken,
                    'mtoken': self.ck,
                    'cookie': f'token={self.ck};uuid={self.uuid}'
                }
                r = requests.get(url, headers=self.t_h)
                rj = r.json()
                if rj['msg'] == 'ok':
                    data = rj['data']
                    for d in data:
                        self.wcxtb = d['count']
                        self.endmsg += f'🎁运行后小团币: {int(self.wcxtb)}({int(self.wcxtb) / 1000}元)\n'
                    return True
                else:
                    self.endmsg += f'🆔账号{self.num}-{self.name} 查询运行后团币失败：还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(3, 8))
                    continue
            except:
                self.endmsg += f'🆔账号{self.num}-{self.name} 查询运行后团币异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def b64(self):
        y_bytes = base64.b64encode(self.tid.encode('utf-8'))
        y_bytes = y_bytes.decode('utf-8')
        return y_bytes

    def get_game(self):
        try_count = 5
        while try_count > 0:
            try:
                self.tid = f'mgc-gamecenter{self.id}'
                self.tid = self.b64()
                url = f'https://game.meituan.com/mgc/gamecenter/common/mtUser/mgcUser/task/finishV2?taskId={self.tid}'
                r = requests.get(url, headers=self.t_h)
                if isprint:
                    print(f'🆔账号{self.num}-{self.name}({self.usid}) 领取{self.id} {r.json()}')
                if r.status_code == 200:
                    if r.json()['msg'] == 'ok':
                        time.sleep(random.randint(1, 3))
                        return True
                    elif '完成过' in r.text:
                        time.sleep(random.randint(1, 3))
                        return True
                    else:
                        if isprint:
                            print(f'🆔账号{self.num}-{self.name}({self.usid}) 任务状态: {r.text}')
                        return False
                else:
                    self.endmsg += f'🆔账号{self.num}-{self.name} {self.id}领取任务失败：还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(3, 8))
                    continue
            except:
                self.endmsg += f'🆔账号{self.num}-{self.name} {self.id}领取任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def post_id(self):
        try_count = 5
        while try_count > 0:
            try:
                url = 'https://game.meituan.com/mgc/gamecenter/front/api/v1/mgcUser/task/receiveMgcTaskReward?yodaReady=h5&csecplatform=4&csecversion=2.3.1&mtgsig={"a1":"1.1","a2":1701400631188,"a3":"1701400631176ACSGOCCe67dcc3e61b3db1bf3f9e3b1c7aaaa886588","a5":"bGQQnm6pBHRw8JiWViBjlF2mdX/wQhqY","a6":"h1.3dVYMwRtIsLOzCuHIWQkUL95NwZiIoT/veP20E5KFH4+X7i4QHxPAMHclLNUmYE1k0+qvn74NazWAy27JG5S4KMhCenJJ77b+6m4PIcTwavW1yWmJ3+j5a7zRmFpWFWTumYfr2V88VYYADCYoClRNkpzoUyvIUZS9VPTheemMuYgQnzVt4Gk/HPpIwy+lwwx5rBXo2ullebl7jg/PG9MbyRk+I3MgsaMRWrZ0arS793T1Blbuon29ajMbgyFmtpJT6wwSxHo15y2NCTwDUJCRRcFsG7LCMLHfnMEScRE2hH5ZtBSj/QTyJf7vaVdNvebH","x0":4,"d1":"c4d27c481bd64a19d0094a2edf043650"}'
                data = {
                    "taskId": self.id,
                    "externalStr": "",
                    "riskParams": {
                        "uuid": self.uuid,
                        "platform": 4,
                        # "platform": 5,
                        "fingerprint": self.fingerprint,
                        "version": "2.0.202",
                        "app": 0,
                        "cityid": "70"
                    }
                }
                r = requests.post(url, headers=self.t_h, json=data)
                if isprint:
                    print(f'🆔账号{self.num}-{self.name}({self.usid}) 完成{self.id} {r.json()}')
                if r.status_code == 200:
                    if r.json()['msg'] == 'ok':
                        time.sleep(random.randint(1, 3))
                        return True
                    elif '异常' in r.text:
                        time.sleep(random.randint(1, 3))
                        return False
                    else:
                        print(f'🆔账号{self.num}-{self.name} {self.id},{r.text}\n')
                        time.sleep(random.randint(1, 3))
                        return False
                else:
                    self.endmsg += f'🆔账号{self.num}-{self.name} {self.id}完成任务异常：还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(3, 8))
                    continue
            except:
                self.endmsg += f'🆔账号{self.num}-{self.name} {self.id}完成任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def coin_login(self):
        """获取签到浏览的actoken"""
        try_count = 5
        while try_count > 0:
            try:
                headers = {
                    'Origin': 'https://awp.meituan.com',
                    'Cookie': f'{self.ck}',
                    'Accept': '*/*',
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json',
                    'Host': 'game.meituan.com',
                    'Connection': 'Keep-Alive',
                }
                params = {
                    'mtUserId': self.usid,
                    'mtDeviceId': self.uuid,
                    'mtToken': self.ck,
                    'nonceStr': 'kvb1xnabe4n1cfg1',
                    'gameType': '10273',
                }
                r = requests.get('https://game.meituan.com/coin-marketing/login/loginMgc', headers=headers,
                                 params=params)
                self.qdactoken = r.json().get('accessToken', None)
                if self.qdactoken is not None:
                    return True
                else:
                    print(r.json())
                    return True
            except:
                self.endmsg += f'🆔账号{self.num}-{self.name} 获取异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def qd(self):
        """签到和浏览任务"""
        try_count = 5
        while try_count > 0:
            try:
                headers = {
                    'Host': 'game.meituan.com',
                    'Connection': 'keep-alive',
                    'x-requested-with': 'XMLHttpRequest',
                    'appName': 'meituan',
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Origin': 'https://awp.meituan.com',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                }
                params = {
                    'yodaReady': 'h5',
                    'csecplatform': '4',
                    'csecversion': '2.3.1',
                }

                data = {
                    # "protocolId": 10002,  # 签到
                    # "protocolId": 10024,  # 1 3 5 要等待时间
                    # "protocolId": 10041,  # 下滑浏览
                    # "protocolId": 10008,  # 获取id
                    # "protocolId": 10014,  # 抽奖
                    # "protocolId": 10015,  # 抽奖前运行
                    "protocolId": self.qdid,
                    "data": {},
                    "riskParams": {
                        "uuid": self.uuid,
                    },
                    "acToken": self.qdactoken,

                }
                if self.qdid == 10024:
                    while True:
                        r = requests.post('https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                                          json=data, params=params)
                        if isprint:
                            print(f'🆔账号{self.num}-{self.name}({self.usid}) {self.qdid}: {r.json()}')
                        if 'interval' in r.text:
                            xxsj = r.json()['data']['timedReward']['interval']
                            time.sleep(xxsj / 1000)
                            time.sleep(random.randint(1, 3))
                        else:
                            time.sleep(random.randint(1, 3))
                            break
                    return True
                elif self.qdid == 10041:
                    while True:
                        r = requests.post('https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                                          json=data,
                                          params=params)
                        if isprint:
                            print(f'🆔账号{self.num}-{self.name}({self.usid}) {self.qdid}: {r.json()}')
                        if 'rewardAmount' in r.text:
                            time.sleep(random.randint(1, 3))
                            continue
                        else:
                            time.sleep(random.randint(1, 3))
                            break
                    return True

                else:
                    r = requests.post('https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                                      json=data,
                                      params=params)
                    if isprint:
                        print(f'🆔账号{self.num}-{self.name}({self.usid}) {self.qdid}: {r.json()}')
                    time.sleep(random.randint(1, 3))
                    return True
            except:
                self.endmsg += f'🆔账号{self.num}-{self.name} {self.qdid}签到任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def get_llids(self):
        try_count = 5
        while try_count > 0:
            try:
                headers = {
                    'Host': 'game.meituan.com',
                    'Connection': 'keep-alive',
                    'x-requested-with': 'XMLHttpRequest',
                    'appName': self.mtbb,
                    'User-Agent': self.ua,
                    'Accept': '*/*',
                    'Origin': 'https://awp.meituan.com',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                }
                params = {
                    'yodaReady': 'h5',
                    'csecplatform': '4',
                    'csecversion': '2.3.1',
                    'mtgsig': {}
                }
                # "protocolId": 10002,  # 签到
                # "protocolId": 10024,  # 1 3 5 要等待时间
                # "protocolId": 10041,  # 下滑浏览
                # "protocolId": 10008,  # 获取id
                # "protocolId": 10014,  # 抽奖
                # "protocolId": 10015,  # 抽奖前运行
                data = {
                    "protocolId": 10008,
                    "data": {},
                    "riskParams": {
                        "uuid": self.uuid,
                    },
                    "acToken": self.qdactoken,
                }

                r = requests.post('https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                                  json=data,
                                  params=params)
                time.sleep(random.randint(1, 3))
                self.lisss = r.json()['data']['taskInfoList']
                return True
            except:
                self.endmsg += f'🆔账号{self.num}-{self.name} {self.qdid}签到任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def get_ll(self):
        try_count = 5
        while try_count > 0:
            try:
                headers = {
                    'Host': 'game.meituan.com',
                    'Connection': 'keep-alive',
                    'x-requested-with': 'XMLHttpRequest',
                    'appName': self.mtbb,
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Origin': 'https://awp.meituan.com',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                }
                params = {
                    'yodaReady': 'h5',
                    'csecplatform': '4',
                    'csecversion': '2.3.1',
                }

                get_data = {
                    "protocolId": 10010,  # 先运行获取任务
                    "data": {
                        "externalStr": {"cityId": "351"},
                        "taskId": self.llid,  # 任务id
                        "taskEntranceType": "normal"
                    },
                    "riskParams": {
                        "uuid": self.uuid,
                    },
                    "acToken": self.qdactoken,
                    "mtToken": self.ck
                }
                r = requests.post(
                    'https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                    json=get_data,
                    params=params
                )
                if isprint:
                    print(f'🆔账号{self.num}-{self.name}({self.usid}) {self.llid} 领取任务 {r.json()}')
                if r.json()['data'] is None:
                    time.sleep(random.randint(1, 3))
                    return False
                else:
                    time.sleep(random.randint(1, 3))
                    return True
            except:
                self.endmsg += f'🆔账号{self.num}-{self.name} {self.llid}获取浏览任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def post_ll(self):
        try_count = 5
        while try_count > 0:
            try:
                headers = {
                    'Host': 'game.meituan.com',
                    'Connection': 'keep-alive',
                    'x-requested-with': 'XMLHttpRequest',
                    'appName': self.mtbb,
                    'User-Agent': self.ua,
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Origin': 'https://awp.meituan.com',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                }
                params = {
                    'yodaReady': 'h5',
                    'csecplatform': '4',
                    'csecversion': '2.3.1',
                }

                post_data = {
                    "protocolId": 10009,  # 再运行完成任务
                    "data": {
                        "externalStr": {"cityId": "351"},
                        "taskId": self.llid,  # 任务id
                        "taskEntranceType": "normal"
                    },
                    "riskParams": {
                        "uuid": self.uuid,
                    },
                    "acToken": self.qdactoken,
                    "mtToken": self.ck
                }

                r = requests.post(
                    'https://game.meituan.com/coin-marketing/msg/post', headers=headers,
                    json=post_data,
                    params=params
                )
                if isprint:
                    print(f'🆔账号{self.num}-{self.name}({self.usid}) {self.llid} 完成任务 {r.json()}\n')
                if r.json()['data'] is None:
                    time.sleep(random.randint(1, 3))
                    return False
                else:
                    time.sleep(random.randint(1, 3))
                    return True
            except:
                self.endmsg += f'🆔账号{self.num}-{self.name} {self.llid}完成浏览任务异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(3, 8))
                continue

    def tj_bchd(self):
        try_count = 5
        while try_count > 0:
            try:
                bchd = int(self.wcxtb) - int(self.xtb)
                url = "https://game.meituan.com/mgc/gamecenter/skuExchange/resources/change/logs?changeType=1&limit=50&sceneId=2&gameId=10139&mtToken=&acToken=&shark=1&yodaReady=h5&csecplatform=4&csecversion=2.3.1"
                headers = {
                    "Host": "game.meituan.com",
                    "Connection": "keep-alive",
                    "x-requested-with": "XMLHttpRequest",
                    "actoken": self.qdactoken,
                    "mtoken": self.ck,
                    "User-Agent": "Mozilla/5.0 (Linux; Android 13; V2055A Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.74 Mobile Safari/537.36 TitansX/11.38.10 KNB/1.2.0 android/13 mt/com.meituan.turbo/2.0.202 App/10120/2.0.202 MeituanTurbo/2.0.202",
                    "Content-Type": "application/json",
                    "Accept": "*/*",
                    "Origin": "https://awp.meituan.com",
                    "Sec-Fetch-Site": "same-site",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://awp.meituan.com/",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"

                }
                r = requests.get(url, headers=headers)
                if 'ok' in r.text:
                    datalist = r.json()['data']
                    coins = 0
                    for data in datalist:
                        coin = data['changeCount']
                        gmtCreated = data['gmtCreated']
                        if gmtCreated >= f"{datetime.now().strftime('%Y-%m-%d')} 00:00:00":
                            coins += coin
                        else:
                            break
                    self.lastGmtCreated = datalist[-1]['gmtCreated']
                    while True:
                        if self.lastGmtCreated >= f"{datetime.now().strftime('%Y-%m-%d')} 00:00:00":
                            url1 = f"https://game.meituan.com/mgc/gamecenter/skuExchange/resources/change/logs?changeType=1&limit=50&sceneId=2&lastGmtCreated={self.lastGmtCreated}&gameId=10139&mtToken=&acToken=&shark=1&yodaReady=h5&csecplatform=4&csecversion=2.3.1"
                            r = requests.get(url1, headers=headers)
                            if 'ok' in r.text:
                                datalist = r.json()['data']
                                for data in datalist:
                                    coin = data['changeCount']
                                    gmtCreated = data['gmtCreated']
                                    if gmtCreated >= f"{datetime.now().strftime('%Y-%m-%d')} 00:00:00":
                                        coins += coin
                                    else:
                                        break
                                self.lastGmtCreated = datalist[-1]['gmtCreated']
                                if self.lastGmtCreated >= f"{datetime.now().strftime('%Y-%m-%d')} 00:00:00":
                                    time.sleep(random.randint(1, 3))
                                    continue
                                else:
                                    self.endmsg += f'🔥本次获得小团币: {bchd}\n💰今日团币: {coins}\n'
                                    return True
                            else:
                                self.endmsg += f'🆔账号{self.num}-{self.name} 获取今日团币异常：还有{try_count - 1}次重试机会\n'
                                try_count -= 1
                                time.sleep(random.randint(2, 5))
                                continue
                        else:
                            self.endmsg += f'🔥本次获得小团币: {bchd}\n💰今日团币: {coins}\n'
                            return True
                    break
                else:
                    self.endmsg += f'🆔账号{self.num}-{self.name} 获取今日团币异常：还有{try_count - 1}次重试机会\n'
                    try_count -= 1
                    time.sleep(random.randint(2, 5))
                    continue
            except:
                self.endmsg += f'🆔账号{self.num}-{self.name} 获取今日团币异常：还有{try_count - 1}次重试机会\n'
                try_count -= 1
                time.sleep(random.randint(2, 5))
                continue

    def get_new_gameid(self):
        if self.get_ids():
            self.ids = []
            zt_3 = []
            for i in self.data_list:
                if i['status'] == 2 and i['id'] not in self.noids:
                    self.ids.append(i['id'])
                if i['status'] == 3 and i['id'] not in self.noids:
                    self.ids.append(i['id'])
                    zt_3.append(i['id'])
                else:
                    pass
            if isprint:
                print(f'🆔账号{self.num}-{self.name}({self.usid}) 获取到{len(self.ids)}个游戏任务！\n{self.ids}')
            if self.ids != [] and len(zt_3) < max_zt3:
                return True
            elif not self.ids:
                return True
            else:
                print(f'🆔账号{self.num}-{self.name}({self.usid}) ⛔️指纹可能错误或者失效了！！！')
                return False
        else:
            return False

    def run_game(self):
        random.shuffle(self.data_list)
        for i in self.data_list:
            self.id = i['id']
            zt = i['status']
            if self.id in self.noids:
                pass
            else:
                if zt == 2:
                    if isprint:
                        print(f'🆔账号{self.num}-{self.name}({self.usid}) id: {self.id} 状态: {zt}')
                    if self.get_game():
                        self.post_id()
                        if isprint:
                            print()
                        continue
                elif zt == 3:
                    if isprint:
                        print(f'🆔账号{self.num}-{self.name}({self.usid}) id: {self.id} 状态: {zt}')
                    self.post_id()
                    if isprint:
                        print()
                    continue
                else:
                    continue

    def get_new_llids(self):
        if self.get_llids():
            self.llids = []
            for i in self.lisss:
                taskTitles = json.loads(i['mgcTaskBaseInfo']['viewExtraJson'])
                buttonName = taskTitles.get('common', None).get('buttonName', '去完成')
                zt = i['status']
                if zt == 2 and buttonName in ['去完成', '去浏览', '去阅读', '去领取']:
                    self.llids.append(i['id'])
                elif zt == 3 and buttonName in ['去完成', '去浏览', '去阅读', '去领取']:
                    self.llids.append(i['id'])
                else:
                    pass
            if isprint:
                print(f'🆔账号{self.num}-{self.name}({self.usid}) 获取到{len(self.llids)}个浏览任务！\n{self.llids}')
            if self.llids:
                return True
            else:
                return False
        else:
            return False

    def run_tbzx(self):
        for i in self.lisss:
            zt = i['status']
            self.llid = i['id']
            taskTitles = json.loads(i['mgcTaskBaseInfo']['viewExtraJson'])
            taskTitle = taskTitles['common']['taskTitle']
            taskDesc = taskTitles['common']['taskDesc']
            buttonName = taskTitles.get('common', None).get('buttonName', '去完成')
            if zt in [2, 3] and self.llid == 15181:
                if isprint:
                    print(
                        f'🆔账号{self.num}-{self.name}({self.usid}) {self.llid}: 状态：{zt} {taskTitle}({taskDesc}) {buttonName}')
                while True:
                    if self.get_ll():
                        if self.post_ll():
                            continue
                        else:
                            break
                    else:
                        break
            elif zt == 2 and buttonName in ['去完成', '去浏览', '去阅读', '去领取']:
                if isprint:
                    print(
                        f'🆔账号{self.num}-{self.name}({self.usid}) {self.llid}: 状态：{zt} {taskTitle}({taskDesc}) {buttonName}')
                if self.get_ll():
                    self.post_ll()
            elif zt == 3 and buttonName in ['去完成', '去浏览', '去阅读', '去领取']:
                if isprint:
                    print(
                        f'🆔账号{self.num}-{self.name}({self.usid}) {self.llid}: 状态：{zt} {taskTitle}({taskDesc}) {buttonName}')
                self.post_ll()
            else:
                continue

    def main(self):
        if km is None:
            self.login = self.sq_login
        else:
            self.login = self.km_login
        if self.login():
            self.act()
            if self.startcxtb():
                if self.fingerprint != '':
                    isgame = self.get_new_gameid()
                    if isgame and self.ids != []:
                        self.startmsg += f'🔔游戏中心获取任务成功！🚀即将运行游戏中心任务和团币中心任务\n'
                        print(self.startmsg)
                        a = 0
                        while True:
                            a += 1
                            if a > 5:
                                return False
                            self.run_game()
                            if self.get_new_gameid() and len(self.ids) != 0:
                                continue
                            else:
                                break
                        if self.coin_login():
                            if self.get_new_llids():
                                self.run_tbzx()
                            self.mtbb = 'meituanturbo'
                            if self.get_new_llids():
                                self.run_tbzx()
                            self.llid = 616
                            if self.get_ll():
                                self.post_ll()
                            for i in self.qdrwids:
                                self.qdid = i
                                self.qd()
                            self.endmsg += f'🆔账号{self.num}-{self.name}({self.usid}) 🎉运行完成\n'
                            if self.endcxtb():
                                if self.tj_bchd():
                                    print(self.endmsg)
                    elif isgame and self.ids == []:
                        self.startmsg += f'✅游戏中心已经全部完成！🚀即将运行团币中心任务\n'
                        print(self.startmsg)
                        if self.coin_login():
                            if self.get_new_llids():
                                self.run_tbzx()
                            self.mtbb = 'meituanturbo'
                            if self.get_new_llids():
                                self.run_tbzx()
                            self.llid = 616
                            if self.get_ll():
                                self.post_ll()
                            for i in self.qdrwids:
                                self.qdid = i
                                self.qd()
                            self.endmsg += f'🆔账号{self.num}-{self.name}({self.usid}) 🎉运行完成\n'
                            if self.endcxtb():
                                if self.tj_bchd():
                                    print(self.endmsg)
                    else:
                        self.startmsg += f'💔游戏中心获取任务失败！🚀即将运行团币中心任务\n'
                        print(self.startmsg)
                        if self.coin_login():
                            if self.get_new_llids():
                                self.run_tbzx()
                            self.mtbb = 'meituanturbo'
                            if self.get_new_llids():
                                self.run_tbzx()
                            self.llid = 616
                            if self.get_ll():
                                self.post_ll()
                            for i in self.qdrwids:
                                self.qdid = i
                                self.qd()
                            self.endmsg += f'🆔账号{self.num}-{self.name}({self.usid}) 🎉运行完成\n'
                            if self.endcxtb():
                                if self.tj_bchd():
                                    print(self.endmsg)
                else:
                    self.startmsg += f'🚀即将运行团币中心任务\n'
                    print(self.startmsg)
                    if self.coin_login():
                        if self.get_new_llids():
                            self.run_tbzx()
                        self.mtbb = 'meituanturbo'
                        if self.get_new_llids():
                            self.run_tbzx()
                        self.llid = 616
                        if self.get_ll():
                            self.post_ll()
                        for i in self.qdrwids:
                            self.qdid = i
                            self.qd()
                        self.endmsg += f'🆔账号{self.num}-{self.name}({self.usid}) 🎉运行完成\n'
                        if self.endcxtb():
                            if self.tj_bchd():
                                print(self.endmsg)
        else:
            print(self.startmsg)


if __name__ == '__main__':
    print = partial(print, flush=True)
    msg = """
🔔当前版本V12.02
更新日志: 
    12.02: 1、自动提取删除指纹的换行。现在需要指纹才能跑游戏中心的任务，注意环境变量格式，没有指纹只跑团币中心任务。
           2、优化团币中心任务判定
           3、新增几个任务，每天多35个！新增一次抽奖。
           4、未提交成功参数设置 max_zt3 = 10 默认如果未提交成功小于10就去做任务。如果大于10个未提交成功的任务，就不会跑游戏中心任务。
    """
    print(msg)

    token = os.environ.get(blname)
    if token is None:
        print(f'⛔️未获取到ck变量：请检查变量是否填写')
        exit(0)
    if '&' in token:
        tokens = token.split("&")
    else:
        tokens = [token]

    bf = os.environ.get("bd_xtbbf")
    if bf is None:
        print(f'⛔️为设置并发变量，默认1')
        bf = 1

    # 运行模式，有卡密填卡密，没卡密默认授权模式
    km = os.environ.get("bd_xtbkm")
    if km is None:
        print(f'✅授权模式运行')
    else:
        print(f'✅卡密模式运行')

    if isprint:
        print(f'✅开启详细日志')
    else:
        print(f'⛔️未开启详细日志')

    print(f'✅获取到{len(tokens)}个账号')
    print(f'🔔设置最大并发数: {bf}\n')

    with concurrent.futures.ThreadPoolExecutor(max_workers=int(bf)) as executor:
        print(f'======================================')
        for num in range(len(tokens)):
            runzh = num + 1
            run = Mttb(runzh, tokens[num])
            executor.submit(run.main)
            time.sleep(random.randint(2, 5))
