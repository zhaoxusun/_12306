#站点映射
import json

import requests

#获取站点原始数据
from constant import from_station, to_station


def station_init():
    url="https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"
    result=requests.get(url)
    print(result.text)
    print(result.text.split("\'")[1])
    newstr=""
    for char in result.text.split("\'")[1]:
        if not char.islower() and not char.isnumeric():
            newstr+=char
    newstr = newstr.replace("|","").replace("\n","")
    print(newstr)
    str_group=newstr.split("@")
    # for str in str_group:
    #     print(str)
    return str_group


#解析站点原始数据
def station_transform():
    str_group=station_init()
    station_dic ={}
    for str in str_group:
        station_key = ""
        station_value = ""
        for char in str:
            if not char.isupper():
                station_key+=char
            else:
                station_value+=char
        print(station_key)
        print(station_value)
        station_dic[station_key]=station_value
    station_dic.pop("")
    return station_dic


#更新站点数据到文件中
def station_update(path):
    station_dic=station_transform()
    file=open(path, "w", encoding='utf8')
    file.writelines(json.dumps(station_dic, ensure_ascii=False))
    print("车站信息文件"+path+"已更新！")
    print(station_dic)
    file.close()

def get_station(station_key,path):
    file=open(path, "r", encoding='utf-8')
    json_str=json.load(file)
    # print(station_key+":"+json_str[station_key])
    file.close()
    return json_str[station_key]

# station_update("../data/station.json")
# get_station(from_station,"../data/station.json")
# get_station(to_station,"../data/station.json")
