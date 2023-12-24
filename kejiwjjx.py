"""
time：2023.12.12
cron: 12 12 * * *
new Env('科技玩家签到');
"""
import json
import re
import asyncio
from aiohttp import ClientSession

contents = ''


def output(content):
    global contents
    contents += ' \n' + str(content)


class AuthenticatedSession:
    def __init__(self, user, passwd, session):
        self.user_id = None
        self.user_lv = None
        self.user = user
        self.passwd = passwd
        self.authorization = None
        self.session = session
        self.username = None
        self.credit = None
        self.comment_count = None

    async def login(self):
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://www.kejiwanjia.net',
            'Sec-Fetch-Dest': 'empty',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://www.kejiwanjia.net',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        data  = f"nickname=&username={self.user}&password={self.passwd}&code=&img_code=&invitation_code=&token=&smsToken=&luoToken=&confirmPassword=&loginType="


        async with self.session.post('https://www.kejiwanjia.net/wp-json/jwt-auth/v1/token', headers=headers,
                                     data=data) as response:
            try:
                result = json.loads(await response.text())
                self.authorization = "Bearer " + result['token']
                self.session.headers.update({
                    'Authorization': self.authorization
                })
                self.session.cookie_jar.update_cookies({'Authorization': self.authorization})
                self.session = self.session
            except Exception as e:
                print(f"Error occurred: {e}")



    async def info(self):
        async with self.session.post('https://www.kejiwanjia.net/wp-json/b2/v1/getUserInfo',
                                     data={'ref': 'null'}) as response:
            try:
                resp = (await response.text()).replace('\/', '/').encode("utf-8").decode("unicode_escape")
                resp1 = re.sub(r'"icon":"[<]span(.*?)/span>",', '', re.sub(r'"verify_icon"(.+?)/i>",', '', resp))
                result = json.loads(resp1)
                user_data = result['user_data']
                self.username = user_data['name']
                self.comment_count = int(user_data['comment_count'])
                self.credit = int(user_data['credit'])
                self.user_id = user_data['id']
                self.user_lv = user_data['lv']['lv']['name'] + user_data['lv']['lv']['lv']
                user_info = f'【+】用户名：{self.username}，ID：{self.user_id}\n【+】当前等级：{self.user_lv}'
                output(user_info)
            except Exception as e:
                print(f"Error occurred: {e}")

    async def signin(self):
        url = 'https://www.kejiwanjia.net/wp-json/b2/v1/userMission'
        async with self.session.post(url, timeout=20, verify_ssl=False) as resp:
            try:
                result = (await resp.text()).replace('\/', '/').encode('utf-8').decode("unicode_escape")
                if 'credit' in result:
                    result1 = json.loads(result)['credit']
                    self.credit += int(result1)
                    sign_info = '【+】签到成功，获得积分：' + str(result1)
                else:
                    sign_info = '【+】签到失败'
                output(sign_info)
            except Exception as e:
                print(f"Error occurred: {e}")


async def qywx_key():
    qykey = '0e8d3263-029e-4ff4-ae93-58449e040f8a'
    qywx_key_key = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}".format(qykey)
    qywx_key_message = {"msgtype": "text",
                        "text": {
                            "content": contents,
                        }
                        }
    qywx_key_header = {"Content-Type": "application/json", "Charset": "UTF-8"}
    async with ClientSession() as session1:
        async with session1.post(url=qywx_key_key, headers=qywx_key_header, data=json.dumps(qywx_key_message)) as resp:
            if resp.status == 200:
                print('企业微信群机器人消息已推送，请查收  ')


async def handle_user(user, passwd):
    async with ClientSession() as session:
        auth_session = AuthenticatedSession(user, passwd, session)
        await auth_session.login()
        await auth_session.info()
        await auth_session.signin()
    output(f'Total comments: {auth_session.comment_count}, Total credit: {auth_session.credit}')

async def main():
    userpass = dict([('xiaozong_52@qq.com', 123456789),('send_message@qq.com', 123456789)])
    tasks = [handle_user(user, passwd) for user, passwd in userpass.items()]
    await asyncio.gather(*tasks)
    print(contents)
    await qywx_key()


if __name__ == '__main__':
    asyncio.run(main())
