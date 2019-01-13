
# -*- coding: utf-8 -*-
import json
from urllib import parse
from io import BytesIO
import base64


import requests
from PIL import Image

from constant import login_username, login_password, login_realname


def login(session,headers):
    # 打开登录页面
    url = "https://kyfw.12306.cn/otn/login/init"
    session.get(url, headers=headers)
    # 发送验证码
    if not captcha(session,headers):
        return False

    # 发送登录信息
    data = {
        "username":login_username,
        "password":login_password,
        "appid":"otn"
    }
    url = "https://kyfw.12306.cn/passport/web/login"
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        result = json.loads(response.text)
        print(result.get("result_message"))
        # print(result.get("result_code"))
        if result.get("result_code") != 0:
            return False

    data = {
        "appid":"otn"
    }
    url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        result = json.loads(response.text)
        print(result.get("result_message"))
        newapptk = result.get("newapptk")

    data = {
        "tk":newapptk
    }
    url = "https://kyfw.12306.cn/otn/uamauthclient"
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print(response.text)

    url = "https://kyfw.12306.cn/otn/index/initMy12306"
    response = session.get(url, headers=headers)
    if response.status_code == 200 and response.text.find(login_realname) != -1:
        # result=session.get("https://kyfw.12306.cn/otn/confirmPassenger/initDc")
        # print(result.text)
        # print(result.text.split("globalRepeatSubmitToken")[1].split(";")[0].replace(" ","").replace("=","").replace("\'",""))
        return True
    return False


def captcha(session,headers):
    # 请求数据是不变的，随机数可以使用random.random()
    data = {
        "login_site": "E",
        "module": "login",
        "rand": "sjrand",
        "0.17231872703389062": ""
    }

    # 获取验证码
    param = parse.urlencode(data)
    url = "https://kyfw.12306.cn/passport/captcha/captcha-image?{}".format(param)
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        # 获取验证码并打开，然后...手动找一下坐标吧，我开始就说了不涉及自动识别验证码的
        file = BytesIO(response.content)
        img = Image.open(file)
        img.save("image.jpg")

    with open("image.jpg", "rb") as imageFile:
        str = base64.b64encode(imageFile.read()).decode()
        # print(str)

    data = {
        "base64": str
    }

    response = requests.post("http://60.205.200.159/api", data=None, json=data)
    result = json.loads(response.text)
    print((result["check"]))

    data = {
        "type": "D",
        "logon": 1,
        "check": result["check"],
        "img_buf": str,
        "=": ""
    }

    response = requests.post("http://check.huochepiao.360.cn/img_vcode", data=None, json=data)
    result = json.loads(response.text)
    answer = result["res"].replace("(", "").replace(")", "")
    print("验证码坐标识别："+answer)

    # 发送验证码
    data = {
        "answer": answer,
        "login_site": "E",
        "rand": "sjrand"
    }

    url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
    response = session.post(url, headers=headers, data=data)
    if response.status_code == 200:
        result = json.loads(response.text)
        # print(result.get("result_message"))
        # 请求成功以后返回的code是4，这个看请求信息就知道了
        return True if result.get("result_code") == "4" else False
    return False






if __name__ == "__main__":
    if login():
        print("Success")
    else:
        print("Failed")
