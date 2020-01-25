import werobot
import requests
import time
from aip import AipFace
import base64
from io import BytesIO
import json
import os
import simplejson
import requests
import json
import base64
import json
from bs4 import BeautifulSoup
import requests
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
robot = werobot.WeRoBot(token='11223344')


def nCoV(message):
    res = requests.get("http://3g.dxy.cn/newh5/view/pneumonia")

    def get_data(res):

        soup = BeautifulSoup(res.content, 'html.parser')
        data = soup.find(id="getAreaStat").string
        data = data.strip("try { window.getAreaStat = ").strip("}catch(e){}")
        data = json.loads(data)
        return data

    def get_data2(res):

        soup = BeautifulSoup(res.content, 'html.parser')
        data = soup.select('div[class="mapTop___2VZCl"]')[0].get_text()
        data = data.replace("传染源", "\n传染源")
        data = data.replace("病毒: 新型冠状病毒", "\n病毒: 新型冠状病毒")
        data = data.replace("传播途径", "\n传播途径")
        data = data.replace("是否变异", "\n是否变异")
        data = data.replace("疫情是否扩散", "\n疫情是否扩散")
        return data

    def get_data3(res):

        soup = BeautifulSoup(res.content, 'html.parser')
        url = soup.select('img[class="mapImg___3LuBG"]')[0].get("src")
        return url

    def query(city_name):
        flag = 0
        data = get_data(res)
        for i in data:
            if i["provinceName"] == city_name or i["provinceShortName"] == city_name:
                data = i
                flag = 1
                break
            elif city_name == "实时":
                data = get_data2(res)
                return data+"\n\n实时疫情图:\n"\
                    + get_data3(res)
            elif city_name == "憨憨王宇洋":
                return "憨憨王诗齐"
            elif "王宇洋" in city_name:
                return city_name.replace("王宇洋", "王诗齐")
        if flag == 0:
            return "没有查询到该城市\n现支持以下城市查询: \n" + "".join([i["provinceName"]+"\n" for i in data])
        else:
            city_name = city_name
            comment = data["comment"]
            confirmedCount_all = str(data["confirmedCount"])+"人 "
            tmp = []
            for i in data['cities']:
                cityName = i["cityName"]
                confirmedCount = str(i["confirmedCount"])+"人 "
                suspectedCount = str(i["suspectedCount"])+"人 "
                curedCount = str(i["curedCount"])+"人 "
                deadCount = str(i["deadCount"]) + "人 "

                tmp.append(cityName + ":" + "确诊:" +
                           confirmedCount+"疑似:"+suspectedCount+"治愈:" + curedCount + "死亡:"+deadCount+"\n")

            return "您查询的城市是：" + city_name + "\n" \
                + city_name + "确诊的人数为" + confirmedCount_all + "\n" \
                + comment+"\n\n" \
                + "".join(tmp)\
                + "\n" \
                + get_data2(res)\
                + "\n\n实时疫情图:\n"\
                + get_data3(res)

    return query(message)


@robot.handler
def nCov(message):
    #a = json.loads(str(meaasge_robot(message.content)))
    #a = a['results'][0]['values']['text']
    print(message.content)
    return nCoV(message.content)


@robot.subscribe
def subscribe(message):
    return '''Hello World!
And nice to meet you.
:)
'''


# 让服务器监听在 0.0.0.0:10084
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 10084
robot.run()
