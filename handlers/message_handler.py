import itchat
import datetime

from constant import report_to_name


def send_move(report_to_name,message):
    now = datetime.datetime.now()
    users = itchat.search_friends(name=report_to_name)
    print(users)
    userName = users[0]['UserName']
    itchat.send(str(now),toUserName=userName)
    itchat.send(message,toUserName=userName)


if __name__ == "__main__":
    itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录
    send_move(report_to_name,"测试抢票")