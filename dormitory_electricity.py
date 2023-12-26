"""
根据学号查询宿舍号及绑定的宿舍的电量使用情况,并且使用pushplus+和QQ邮箱推送消息
time：2023.12.26
cron: 0 */4 * * *
new Env('宿舍电量通报');
"""

import json
import os
import requests
from urllib.parse import quote
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# from notify import send

# 通知服务
push_config = {
    'HITOKOTO': False,                  # 启用一言（随机句子）

    # bark IP 或设备码，例：https://api.day.app/DxHcxxxxxRxxxxxxcm/
    'BARK_PUSH': '',
    'BARK_ARCHIVE': '',                 # bark 推送是否存档
    'BARK_GROUP': '',                   # bark 推送分组
    'BARK_SOUND': '',                   # bark 推送声音
    'BARK_ICON': '',                    # bark 推送图标
    'BARK_LEVEL': '',                   # bark 推送时效性
    'BARK_URL': '',                     # bark 推送跳转URL

    'CONSOLE': True,                    # 控制台输出

    'DD_BOT_SECRET': '',                # 钉钉机器人的 DD_BOT_SECRET
    'DD_BOT_TOKEN': '',                 # 钉钉机器人的 DD_BOT_TOKEN

    'FSKEY': '',                        # 飞书机器人的 FSKEY

    'GOBOT_URL': '',                    # go-cqhttp
                                        # 推送到个人QQ：http://127.0.0.1/send_private_msg
                                        # 群：http://127.0.0.1/send_group_msg
    'GOBOT_QQ': '',                     # go-cqhttp 的推送群或用户
                                        # GOBOT_URL 设置 /send_private_msg 时填入 user_id=个人QQ
                                        #               /send_group_msg   时填入 group_id=QQ群
    'GOBOT_TOKEN': '',                  # go-cqhttp 的 access_token

    'GOTIFY_URL': '',                   # gotify地址,如https://push.example.de:8080
    'GOTIFY_TOKEN': '',                 # gotify的消息应用token
    'GOTIFY_PRIORITY': 0,               # 推送消息优先级,默认为0

    'IGOT_PUSH_KEY': '',                # iGot 聚合推送的 IGOT_PUSH_KEY

    'PUSH_KEY': '',                     # server 酱的 PUSH_KEY，兼容旧版与 Turbo 版

    'DEER_KEY': '',                     # PushDeer 的 PUSHDEER_KEY
    'DEER_URL': '',                     # PushDeer 的 PUSHDEER_URL

    'CHAT_URL': '',                     # synology chat url
    'CHAT_TOKEN': '',                   # synology chat token

    'PUSH_PLUS_TOKEN_1': '',              # push+ 微信推送的用户令牌
    'PUSH_PLUS_USER_1': '',               # push+ 微信推送的群组编码

    'QMSG_KEY': '',                     # qmsg 酱的 QMSG_KEY
    'QMSG_TYPE': '',                    # qmsg 酱的 QMSG_TYPE

    'QYWX_ORIGIN': '',                  # 企业微信代理地址

    'QYWX_AM': '',                      # 企业微信应用

    'QYWX_KEY': '',                     # 企业微信机器人

    # tg 机器人的 TG_BOT_TOKEN，例：1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ
    'TG_BOT_TOKEN': '',
    'TG_USER_ID': '',                   # tg 机器人的 TG_USER_ID，例：1434078534
    'TG_API_HOST': '',                  # tg 代理 api
    'TG_PROXY_AUTH': '',                # tg 代理认证参数
    'TG_PROXY_HOST': '',                # tg 机器人的 TG_PROXY_HOST
    'TG_PROXY_PORT': '',                # tg 机器人的 TG_PROXY_PORT

    # 智能微秘书 个人中心的apikey 文档地址：http://wechat.aibotk.com/docs/about
    'AIBOTK_KEY': '',
    'AIBOTK_TYPE': '',                  # 智能微秘书 发送目标 room 或 contact
    'AIBOTK_NAME': '',                  # 智能微秘书  发送群名 或者好友昵称和type要对应好

    'SMTP_SERVER': 'smtp.qq.com',  # SMTP 发送邮件服务器，形如 smtp.qq.com:465
    'SMTP_SERVER_PORT': '465',  # SMTP 发送邮件服务器端口，465
    'SMTP_SSL': 'false',  # SMTP 发送邮件服务器是否使用 SSL，填写 true 或 false
    'SMTP_EMAIL_1': '',  # SMTP 收发件邮箱，通知将会由自己发给自己
    'SMTP_PASSWORD_1': '',  # SMTP 登录密码，也可能为特殊口令，视具体邮件服务商说明而定
    'SMTP_NAME_1': '',  # SMTP 收发件人姓名，可随意填写
    'PUSHME_KEY': '',                   # PushMe 酱的 PUSHME_KEY

    'CHRONOCAT_QQ': '',                 # qq号
    'CHRONOCAT_TOKEN': '',              # CHRONOCAT 的token
    'CHRONOCAT_URL': '',                # CHRONOCAT的url地址

    'WEBHOOK_URL': '',                  # 自定义通知 请求地址
    'WEBHOOK_BODY': '',                 # 自定义通知 请求体
    'WEBHOOK_HEADERS': '',              # 自定义通知 请求头
    'WEBHOOK_METHOD': '',               # 自定义通知 请求方法
    'WEBHOOK_CONTENT_TYPE': ''          # 自定义通知 content-type
}
notify_function = []
# fmt: on

# 首先读取 面板变量 或者 github action 运行变量
for k in push_config:
    if os.getenv(k):
        v = os.getenv(k)
        push_config[k] = v


def pushplus_bot(title: str, content: str, url="http://www.pushplus.plus/send") -> None:
    """
   使用push+推送消息。
   """
    PUSH_PLUS_USER = push_config.get("PUSH_PLUS_USER_1")
    PUSH_PLUS_TOKEN = push_config.get("PUSH_PLUS_TOKEN_1")
    data = {
        "token": PUSH_PLUS_TOKEN,
        "title": title,
        "content": content,
        "topic": PUSH_PLUS_USER,
    }
    body = json.dumps(data).encode(encoding="utf-8")
    response = requests.post(url, data=body, headers={
                             'Content-Type': "application/json"}).json()
    print("PUSHPLUS 推送{0}！".format('成功' if response["code"] == 200 else '失败'))


def smtp(title: str, content: str) -> None:
    msg_from = push_config.get("SMTP_EMAIL_1")  # 发送方邮箱
    passwd = push_config.get("SMTP_PASSWORD_1")

    to = ['send_message@qq.com', '1415753409@qq.com']  # 接受方邮箱

    # 设置邮件内容
    # MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    # 正文内容
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    # 设置邮件主题
    msg['Subject'] = title
    msg['nickname '] = push_config.get("SMTP_NAME")

    # 发送方信息
    msg['From'] = msg_from
    try:
        # 开始发送
        # 通过SSL方式发送，服务器地址和端口
        s = smtplib.SMTP_SSL(push_config.get("SMTP_SERVER"),
                             push_config.get("SMTP_SERVER_PORT"))
        # 登录邮箱
        s.login(msg_from, passwd)
        # 开始发送
        s.sendmail(msg_from, to, msg.as_string())
        print("SMTP 邮件 推送成功！")
    except Exception as e:
        print(f'SMTP 邮件 推送失败！{e}')


def get_response(url: str, headers: dict, payload: str) -> dict:
    """
   发送请求并返回json响应。
   """
    response = requests.request("POST", url, headers=headers, data=payload)
    # 序列化JSON数据。indent参数设置缩进，确保格式化的输出，ensure_ascii参数为False禁用对特殊字符的转义
    data = json.loads(response.text)["body"].replace('\\"', '"').strip('"')
    # json_data = json.loads(data)
    # print(json.dumps(json_data,indent=4,ensure_ascii=False))
    return json.loads(data)


def generate_result_today(json_data: dict) -> tuple[str, str]:
    global Notice
    room = json_data["roomfullname"]
    use = json_data["detaillist"][0]["use"]
    odd = json_data["detaillist"][0]["odd"]
    roomverify = json_data["roomverify"]
    detail = f"寝室号：{room}\n历史使用：{use}\n目前剩余：{odd}\n"
    if float(odd) < int(threshold):
        detail = f"当前剩余电量已不足{threshold}度，请尽快充值！！！\n"*3 + detail
        Notice = True
    return detail, roomverify


def generate_result_week(json_data: dict) -> str:
    result = ""
    for day in json_data["modlist"][0]["weekuselist"]:
        daydate = day["daydate"]
        dayuse = day["dayuse"]
        weekday = day["weekday"]
        result += f"{daydate}————{weekday}，使用电量：{dayuse}\n"
    return result


def build_payload(cmd: str, account: str, timestamp: str, roomverify: str = None):
    payload = {
        'cmd': cmd,
        'account': account,
        'timestamp': timestamp,
        'roomverify': roomverify
    }
    formatted_payload = f"param={quote(json.dumps(payload))}&customercode=973&method={cmd}&command=JBSWaterElecService"
    return formatted_payload


def build_and_send_request(headers: dict, url: str, account: str, cmd: str, timestamp: str, roomverify: str = None):
    payload = build_payload(cmd, account, timestamp, roomverify)
    response = requests.post(url, headers=headers, data=payload).json()
    return response


def main():
    url = "https://xqh5.17wanxiao.com/smartWaterAndElectricityService/SWAEServlet"
    headers = {
        'Host': 'xqh5.17wanxiao.com',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; 2206123SC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.97 Mobile Safari/537.36 Wanxiao/5.7.3',
        'accept': '*/*',
        'origin': 'https://xqh5.17wanxiao.com',
        'x-requested-with': 'com.newcapec.mobile.ncp',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://xqh5.17wanxiao.com/userwaterelecmini/index.html',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'SERVERID=14141aec02e4422f3be40cb7c86d1171|1695880151|1695880137',
        'content-type': 'application/x-www-form-urlencoded'
    }
    # 今日电量通报
    room_response = json.loads(
        build_and_send_request(headers, url, account, "getbindroom", "2023092813491121").get("body", None))
    result = ''
    if "roomlist" in room_response:
        for room in room_response["roomlist"]:
            result_today = generate_result_today(room)

            roomverify = result_today[1]

            week_response = json.loads(
                build_and_send_request(headers, url, account, "h5_getstuindexpage", "2023092813491245",
                                       roomverify).get("body", None))
            result_week = "近一周电量使用情况：\n" + generate_result_week(week_response)

            result += result_today[0] + result_week + "\n\n"
            # print(result)
    else:
        result_today = generate_result_today(room_response)
        roomverify = result_today[1]

        week_response = json.loads(
            build_and_send_request(headers, url, account, "h5_getstuindexpage", "2023092813491245",
                                   roomverify).get("body", None))
        result_week = "近一周电量使用情况：\n" + generate_result_week(week_response)

        result += result_today[0] + result_week
    print(result)
    if Notice:
        pushplus_bot("每日电量播报：", result)
        # send("每日电量播报：", result)
        smtp("每日电量播报：", result)
        # print(result)


if __name__ == '__main__':
    Notice = False
    account = "202010224109"
    # 阈值
    threshold = 20
    main()
