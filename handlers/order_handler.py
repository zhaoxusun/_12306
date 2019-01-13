from datetime import datetime
import json
import time

import requests

from constant import passenger_name, passenger_id, passenger_phone, train_date, from_station, to_station
from handlers.ticket_handler import get_train_no, get_train_code, get_train_from_station, get_train_to_station, \
    get_seat_type_by_ticket_info, get_train_location, get_can_order_ticket_by_user_choice


#下单
def order(session,ticket_dic):

    url="https://kyfw.12306.cn/otn/login/checkUser"
    data={
        "_json_att":""
    }
    result = session.post(url)
    print(result.text)

    url="https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
    data={
        "secretStr":ticket_dic["预定号"],
        "train_date":train_date,
        "back_train_date":train_date,
        "tour_flag":"dc",
        "purpose_code":"ADULT",
        "query_from_station_name":from_station,
        "query_to_station_name":to_station,
        "undefined":""
    }
    result = session.post(url,data=data)
    # print(result.text)
    if "您还有未处理的订单" in result.text:
        print("下单成功或者12306在排队购买，脚本继续保持抢票，去12306官网确认吧，如果订单待支付状态，手动结束脚本即可")
        return "下单成功，不提醒用户"

    url="https://kyfw.12306.cn/otn/leftTicket/init"
    data={
        "linktypeid":"dc"
    }
    session.get(url,data=data)
    seat_type=get_seat_type_by_ticket_info(ticket_dic)

    url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
    data={
        "_json_att:":""
    }
    result = session.post(url,data=data)
    # print(result.text)
    token = result.text.split("globalRepeatSubmitToken")[1].split(";")[0].replace(" ", "").replace("=", "").replace("\'", "")
    key_check_isChange=result.text.split("key_check_isChange")[1].split(",")[0].replace(" ", "").replace(":", "").replace("\'","")
    left_ticket = result.text.split("leftTicketStr")[1].split(",")[0].replace(" ", "").replace(":", "").replace("\'","")

    url = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
    data = {
        "REPEAT_SUBMIT_TOKEN": token
    }
    result = session.post(url, data=data)
    # if str(json.loads(result.text)["data"]["noLogin"]) == "true":
    #     print("用户登录状态已经过期，需要重新登录")
    #     return False
    if passenger_name not in result.text:
        print("乘客信息不在您的常旅客名单中，请在12306网站中添加后再下单")
        return "乘客信息不在您12306用户的常旅客名单中"

    url="https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
    passengerTicketStr=seat_type+",0,1,"+passenger_name+",1,"+passenger_id+","+passenger_phone+",N"
    oldPassengerStr=passenger_name+",1,"+passenger_id+",1_"
    data={
        "cancel_flag":"2",
        "passengerTicketStr":passengerTicketStr,
        "bed_level_order_num":"000000000000000000000000000000",
        "oldPassengerStr":oldPassengerStr,
        "tour_flag":"dc",
        "randCode":"",
        "whatsSelect":"1",
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":token
    }
    print(data)
    result = session.post(url,data=data)
    result_json=json.loads(result.text)
    print(result_json["status"])
    # if str(result_json["status"]) != "True":
    #     print("下单失败-原因1")
    #     return False

    url="https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
    train_time=train_date.split("-")
    train_time=datetime(int(train_time[0]), int(train_time[1]), int(train_time[2])).strftime("%a %b %d %Y 00:00:00 GMT+0800 (中国标准时间)")
    data={
        "train_date": train_time,
        "train_no": get_train_no(ticket_dic),
        "stationTrainCode": get_train_code(ticket_dic),
        "seatType": get_seat_type_by_ticket_info(ticket_dic),
        "fromStationTelecode": get_train_from_station(ticket_dic),
        "toStationTelecode": get_train_to_station(ticket_dic),
        "leftTicket": left_ticket,
        "purpose_codes": "00",
        "train_location": get_train_location(ticket_dic),
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":token
    }
    print(data)
    result = session.post(url, data=data)
    # result_json=json.loads(result.text)
    print(result.text)
    # if str(result_json["status"]) != "True":
    #     print("下单失败-原因2")
    #     return False

    url="https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
    passengerTicketStr=seat_type+",0,1,"+passenger_name+",1,"+passenger_id+","+passenger_phone+",N"
    oldPassengerStr=passenger_name+",1,"+passenger_id+",1_"
    data={
        "passengerTicketStr": passengerTicketStr,
        "oldPassengerStr": oldPassengerStr,
        "randCode": "",
        "whatsSelect": "1",
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": token,
        "purpose_codes": "00",
        "leftTicketStr": left_ticket,
        "key_check_isChange":key_check_isChange,
        "dwAll":"N",
        "seatDetailType":"000",
        "roomType":"00",
        "choose_seats":"",
        "train_location":get_train_location(ticket_dic)
    }
    result = session.post(url,data=data)
    result_json=json.loads(result.text)
    print(data)
    print(result.text)
    # if result_json["status"] != "True":
    #     print("下单失败-原因3")
    #     return False

    return "下单成功，去12306系统查看下吧"
# *****************************下边代码暂时不需要***************************



    # url="https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime",
    # random=str(round(time.time() * 1000))
    # data={
    #     "random":random,
    #     "tourFlag":"dc",
    #     "_json_att": "",
    #     "REPEAT_SUBMIT_TOKEN": token
    # }
    # result = requests.get(url,params=data)
    # result_json=json.loads(result.text)
    # print(data)
    # print(result.text)
    # if str(result_json["status"]) != "True":
    #     print("下单失败-原因4")
    #     return False

    # url="https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime",
    # random=str(round(time.time() * 1000))
    # data={
    #     "random":random,
    #     "tourFlag":"dc",
    #     "_json_att": "",
    #     "REPEAT_SUBMIT_TOKEN": token
    # }
    # result = requests.get(url,params=data)
    # result_json=json.loads(result.text)
    # print(data)
    # print(result.text)
    # if str(result_json["status"]) != "True":
    #     print("下单失败-原因5")
    #     return False
    # order_id = result_json["data"]["orderId"]
    #
    # url="https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
    # data={
    #     "orderSequence_no":order_id,
    #     "_json_att": "",
    #     "REPEAT_SUBMIT_TOKEN": token
    # }
    # result = session.post(url,data=data)
    # result_json=json.loads(result.text)
    # print(data)
    # print(result.text)











