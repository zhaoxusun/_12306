import json
import urllib

import requests

from constant import train_date, from_station, to_station, train_no, train_seat_type
from handlers.station_handler import get_station


def get_ticket_data(session,path):
    # 查询余票
    url = "https://kyfw.12306.cn/otn/leftTicket/queryZ"
    from_station_transform=get_station(from_station,path)
    to_station_transform=get_station(to_station,path)
    # data = {
    #     "leftTicketDTO.train_date":train_date,
    #     "leftTicketDTO.from_station":from_station_transform,
    #     "leftTicketDTO.to_station":to_station_transform,
    #     "purpose_codes":"ADULT"
    # }
    query_params="?leftTicketDTO.train_date="+train_date+"&leftTicketDTO.from_station="+from_station_transform+\
                 "&leftTicketDTO.to_station="+to_station_transform+"&purpose_codes=ADULT"
    result = session.get(url+query_params)
    print(result.text)
    return json.loads(result.text)


def get_ticket(ticketdata):
    data=ticketdata.split("|")
    if data[11]=="Y":
        data_dic={
            "预定号":urllib.parse.unquote(data[0]), #预定号
            "train_no":data[2],
            "车次":data[3], #车次
            "始发站":data[4], #始发站
            "终点站":data[5], #终点站
            "起始站":data[6], #起始站
            "目标站":data[7], #目标站
            "出发时间":data[8], #出发时间
            "到达时间":data[9], #到达时间
            "历时":data[10], #历时
            "train_location":data[15],
            "高级软卧":data[21], #高级动卧
            "软卧一等卧":data[23], #软卧
            "软座":data[24], #软座
            "特等座":data[25], #特等座
            "无座":data[26], #无座
            "硬卧二等卧":data[28], #硬卧
            "硬座":data[29], #硬座
            "二等座":data[30], #二等座
            "一等座":data[31], #一等座
            "商务座":data[32], #商务座
            "动卧":data[33] #动卧
        }
        # print(data_dic)
        return data_dic
    else:
        return None


#根据用户配置数据，选择车次
def get_can_order_ticket_by_user_choice(session,path):
    result=get_ticket_data(session,path) #车票查询结果
    ticket_data_group=result["data"]["result"]#车票数据原始数据
    # print(ticket_data_group)
    train_no_group=train_no.split(",")
    for ticket in ticket_data_group:#每一组原始数据
        ticket_dic = get_ticket(ticket)#每一组原始数据处理后的数据
        #选择一个车次
        for no in train_no_group:#每一个用户配置的车次
            if ticket_dic is not None:
                if ticket_dic["车次"] == no:
                    print("选择车次："+no)
                    # print(ticket_dic)
                    return ticket_dic
    print("没有符合条件的车次")
    return None


#程序自动选择车次
def get_can_order_ticket_by_computer_choice(session,path):
    result=get_ticket_data(session,path)
    ticket_data_group=result["data"]["result"]
    # print(ticket_data_group)
    for ticket in ticket_data_group:
        ticket_dic = get_ticket(ticket)
        #选择一个车次
        if ticket_dic is not None:
            print("选择车次："+ticket_dic["车次"])
            return ticket_dic
    print("没有符合条件的车次")
    return None


def get_seat_type_by_ticket_info(ticket_dic):
    if ticket_dic["二等座"] != "":
        print("选择座位类型为二等座！")
        return "O"
    elif ticket_dic["一等座"] !="":
        print("选择座位类型为一等座！")
        return "M"
    elif ticket_dic["商务座"] !="":
        print("选择座位类型为商务座！")
        return "9"
    elif ticket_dic["硬卧二等卧"] !="":
        print("选择座位类型为硬卧二等卧！")
        return "3"
    elif ticket_dic["软卧一等卧"] !="":
        print("选择座位类型为软卧一等卧！")
        return "4"
    elif ticket_dic["高级软卧"] !="":
        print("选择座位类型为高级软卧！")
        return "6"
    elif ticket_dic["硬座"] !="":
        print("选择座位类型为硬座！")
        return "1"
    elif ticket_dic["软座"] !="":
        print("选择座位类型为软座！")
        return "2"
    elif ticket_dic["特等座"] !="":
        print("选择座位类型为特等座！")
        return "9"
    elif ticket_dic["动卧"] !="":
        print("选择座位类型为动卧！")
        return "5"
    elif ticket_dic["无座"] !="":
        if "D" in ticket_dic["车次"] or "C" in ticket_dic["车次"] or "G" in ticket_dic["车次"]:
            print("选择座位类型为无座！")
            return "O"
        else:
            print("选择座位类型为无座！")
            return "1"


def get_train_no(ticket_dic):
    return ticket_dic["train_no"]


def get_train_code(ticket_dic):
    return ticket_dic["车次"]


def get_train_from_station(ticket_dic):
    return ticket_dic["起始站"]


def get_train_to_station(ticket_dic):
    return ticket_dic["目标站"]


def get_train_location(ticket_dic):
    return ticket_dic["train_location"]


# get_can_order_ticket_by_user_choice("../data/station.json")
# get_can_order_ticket_by_computer_choice("../data/station.json")
# a=get_seat_type_by_ticket_info(get_can_order_ticket_by_user_choice("../data/station.json"))
# a=get_seat_type_by_ticket_info(get_can_order_ticket_by_computer_choice("../data/station.json"))


