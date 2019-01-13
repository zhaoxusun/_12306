import itchat
import requests
from fake_useragent import UserAgent
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from constant import report_to_name
from handlers.login_handler import login
from handlers.message_handler import send_move
from handlers.order_handler import order
from handlers.ticket_handler import get_can_order_ticket_by_user_choice, get_can_order_ticket_by_computer_choice


# def auto_order(path):
#     session = requests.session()
#     session.verify = False
#     disable_warnings(InsecureRequestWarning)
#     ua = UserAgent(verify_ssl=False)
#     headers = {
#         "User-Agent": ua.random,
#         "Host":"kyfw.12306.cn",
#         "Referer":"https://kyfw.12306.cn/otn/passport?redirect=/otn/"
#     }
#     # 按照用户配置车次查余票
#     ticket_dic=get_can_order_ticket_by_user_choice(session,path)
#     if ticket_dic is not None:
#         #登录
#         login_success=False
#         while login_success is False:
#             login_success=login(session,headers)
#     else:
#         # 用户配置车次无票，查询剩余车次余票
#         ticket_dic=get_can_order_ticket_by_computer_choice(session,path)
#         if ticket_dic is not None:
#             #登录
#             login_success = False
#             while login_success is False:
#                 login_success = login(session, headers)
#         else:
#             print("没有查到可定余票，下单失败！")
#             return False
#     #下单
#     print(ticket_dic["预定号"])
#     order(session, ticket_dic)

itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录


def auto_order_forever(path):
    session = requests.session()
    session.verify = False
    disable_warnings(InsecureRequestWarning)
    ua = UserAgent(verify_ssl=False)
    headers = {
        "User-Agent": ua.random,
        "Host":"kyfw.12306.cn",
        "Referer":"https://kyfw.12306.cn/otn/passport?redirect=/otn/"
    }

    order_success=""
    while True:
        try:
            #保持登录状态
            url = "https://kyfw.12306.cn/otn/login/checkUser"
            data = {
                "_json_att": ""
            }
            result = session.post(url).text
            if "false" in result or "False" in result:#检测是否登录状态，如果标识位flag为false，则处于未登录状态
                login_success=False
                while login_success is False:
                    login_success=login(session,headers)

            # 按照用户配置车次查余票
            ticket_dic=get_can_order_ticket_by_user_choice(session,path)
            if ticket_dic is None:
                ticket_dic=get_can_order_ticket_by_computer_choice(session,path)
                if ticket_dic is None:
                    print("没有查到可定余票，下单失败！")
                    return False
            #下单
            print(ticket_dic["预定号"])
            order_success=order(session, ticket_dic)
            if order_success == "下单成功，去12306系统查看下吧":
                send_move(report_to_name, "下单成功，去12306系统查看下吧")  # 微信消息通知
        except Exception as e:
            print(e)
            print("再次尝试抢票......")
    return order_success


if __name__ == "__main__":
    auto_order_forever("data/station.json")



