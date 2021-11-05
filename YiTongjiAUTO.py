# -*- coding: utf-8 -*-
# @Time    : 2021/11/5 11:06
# @Author  : Barry Wang
# @FileName: YiTongJiAUTO.py
# @Software: YiTongJiAUTO
# @Github  : https://github.com/BarryWangQwQ

import sys
import json
import requests
import datetime
import threading


# 健康日报对象
class Health_Reporter:
    def __init__(self,
                 token=None,
                 province=None,
                 city=None,
                 country=None,
                 lng=None,
                 lat=None,
                 fever=False,
                 infected=False):
        self.token = token
        self.province = province
        self.city = city
        self.country = country
        self.lng = lng
        self.lat = lat
        self.fever = fever
        self.infected = infected
        # 接口header
        self.headers = {
            "Content-Type": "application/json;charset=utf-8",
            "ncov-access-token": self.token,  # 用户唯一且不变的token 例如: "68e932c30032****9c01f6f5"
        }
        # 打卡信息
        self.data = {
            "address": {
                "province": self.province,  # 省份代码   例如: （北京省）-> "110000"
                "city": self.city,  # 市区代码   例如: （北京市）-> "110100"
                "county": self.country,  # 县级代码   例如: （延庆区）-> "110119"
                "autoFetch": True,
                "lng": self.lng,  # 当前地区的经度  例如: 延庆 -> "115.88800815442164"
                "lat": self.lat  # 当前地区的纬度  例如: 延庆 -> "40.37037323579328"
            },
            "self_suspected": False,  # 自己是否疑似患新型肺炎（隔离中等待医院检验结果）
            "self_confirmed": False,  # 自己是否确诊患新型肺炎（医院已出具确诊证明）
            "fever": self.fever,  # 是否有发热 True/False
            "description": "",
            "infected": self.infected,  # 是否被感染 True/False
            "at_home": True,  # 是否今日在家
            "contacted": False,  # 是否接触过疑似或确诊病例
            "custom": {
                "iywet": "否",  # 14日内是否有过中、高风险地区旅行史
                "ikaeu": "否",  # 所在社区是否有确诊病例
                "npafq": "否",  # 是否处于观察期（14天）
                "zplnj": "大二",  # 所在年级
                "vezjy": "36.5",  # 今天的体温是多少摄氏度
                "toxwn": "否",  # 是否有呕吐、腹泻等症状（诺如病毒感染典型症状）
                "ozjvm": "否",  # 身体是否出现皮疹、水疱（水痘症状）
                "dxqon": "否",  # 是否处于居家健康观察状态
                "gzvwa": "否",  # 是否处于新冠肺炎密切接触者居家隔离状态
                "wvbnm": "否",  # 当日核酸检测是否为阳性
                "stqig": "否",  # 目前是否身处中高风险地区
                "goeza": "是",  # 是否已接种第一剂疫苗
                "shnjm": "是"  # 是否已接种第二剂疫苗
            },
        }

    # 打卡
    def report(self):
        # 获取当前日报id
        def get_DailyCode(headers, data):
            link = 'https://www.ioteams.com/ncov/api/users/dailyReport'
            req = requests.post(link, headers=headers, data=json.dumps(data))
            response = req.json()
            if response["msg"] == "您今天已经创建过日报，无法再次创建":
                return None
            else:
                # print(response)
                id = response['data']['data']['_id']
                # print(id)
                return id

        id = get_DailyCode(self.headers, self.data)
        if id is not None:
            url = 'https://www.ioteams.com/ncov/api/users/dailyReports/{}'
            try:
                requests.put(eval(url.format(id)),
                             headers=eval(json.dumps(self.headers)),
                             data=eval(json.dumps(self.data)))
            except:
                pass
            print(datetime.datetime.now().strftime('\n[%Y/%m/%d %H:%M:%S]') +
                  "Token:" +
                  self.token +
                  " -> 打卡成功.\n>>", end='')
        else:
            print(datetime.datetime.now().strftime('\n[%Y/%m/%d %H:%M:%S]') +
                  " Token:" +
                  self.token +
                  " -> 此ID今日已打卡, 无需重复执行.\n>>", end='')
            pass


# 定时打卡服务
class Service:
    def __init__(self):
        self.describe()
        self.taskList = []
        self.status = False
        self.timeSet = "00:00:00"
        print(datetime.datetime.now().strftime('\n[%Y/%m/%d %H:%M:%S]') + " 已初始化打卡服务. (输入help可查看命令提示)\n", end='')

    def main(self, task_list: list):
        days = ""
        print(datetime.datetime.now().strftime('\n[%Y/%m/%d %H:%M:%S]') + " 已部署定时打卡服务.\n", end='')
        while self.status:
            if datetime.datetime.now().strftime('%H:%M:%S') == self.timeSet and \
                    days != datetime.datetime.now().strftime('%d'):
                for obj in task_list:
                    obj.report()
                days = datetime.datetime.now().strftime('%d')

    def run(self):
        self.status = True
        thread = threading.Thread(target=self.main, args=(self.taskList,))
        thread.start()

    def set(self, time: str):
        self.timeSet = time
        print(datetime.datetime.now().strftime('\n[%Y/%m/%d %H:%M:%S]') +
              " 服务执行周期已设定为每日%s.\n" % time, end='')

    def add(self,
            token=None,
            province=None,
            city=None,
            country=None,
            lng=None,
            lat=None,
            fever=False,
            infected=False):
        self.taskList.append(
            Health_Reporter(
                token,
                province,
                city,
                country,
                lng,
                lat,
                fever,
                infected))
        print(datetime.datetime.now().strftime('\n[%Y/%m/%d %H:%M:%S]') + " 已添加%s到任务队列.\n" % token, end='')

    def show(self):
        id = 0
        print(datetime.datetime.now().strftime('\n[%Y/%m/%d %H:%M:%S]') +
              " 任务队列中已存在%d条记录:\n" % len(self.taskList), end='')
        for obj in self.taskList:
            print("队列ID: %d" % id, "(Token %s)\n" % obj.token, end='')
            id += 1

    def delete(self, id: int):
        try:
            token = self.taskList[id].token
            self.taskList.pop(id)
            print(datetime.datetime.now().strftime('\n[%Y/%m/%d %H:%M:%S]') +
                  " ID:{0} Token {1} 已从任务队列中移除.\n".format(id, token), end='')
        except IndexError:
            print(datetime.datetime.now().strftime('\n[%Y/%m/%d %H:%M:%S]') +
                  " ID:%d out of range.\n" % id, end='')

    def stop(self):
        self.status = False
        print(datetime.datetime.now().strftime('\n[%Y/%m/%d %H:%M:%S]') + " 已停止打卡服务.\n", end='')
        sys.exit()

    @staticmethod
    def help():
        print("""命令提示: 
        run -> 部署服务
        stop -> 关闭/停止服务
        time set -> 设置打卡时间
        add -> 向队列添加新的打卡对象
        show -> 查看已记录的打卡队列
        delete -> 删除打卡对象
        describe -> 查看程序自述
        """)

    @staticmethod
    def describe():
        print("""
        YiTongJiAUTO 2.0 Beta
        仅供学习, 请按时打卡, 及时反应真实状况, 盼疫情早日结束.
        Author  : Barry Wang 
        @Github : https://github.com/BarryWangQwQ
        """)


if __name__ == '__main__':
    service = Service()  # 初始化服务

    '''
    # 初始化打卡对象
    barry = Health_Reporter("68e932c30032****9c01f6f5",  # Token
                            "110000",  # 省份代码
                            "110100",  # 市区代码
                            "110119",  # 县级代码
                            "115.88800815442164",  # 经度
                            "40.37037323579328")  # 纬度

    # 加入任务列表
    service.taskList.append(barry)
    '''

    while True:
        i = input(">> ")
        if i == "run":
            service.run()
        elif i == "stop":
            service.stop()
        elif i == "time set":
            i = input("time (H:M:S) >> ")
            service.set(i)
        elif i == "add":
            token = input("token (str) >> ")
            province = input("province (int) >> ")
            city = input("city (int) >> ")
            country = input("country (int) >> ")
            lng = input("lng (float) >> ")
            lat = input("lat (float) >> ")
            fever = bool(input("fever (True/False) >> "))
            infected = bool(input("infected (True/False) >> "))
            service.add(token,
                        province,
                        city,
                        country,
                        lng,
                        lat,
                        fever,
                        infected)
        elif i == "show":
            service.show()
        elif i == "delete":
            id = int(input("id (int) >> "))
            service.delete(id)
        elif i == "help":
            service.help()
        elif i == "describe":
            service.describe()
