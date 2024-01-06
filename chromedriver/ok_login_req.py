import aiohttp
import asyncio
import os

from dotenv import load_dotenv

from bs4 import BeautifulSoup

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
login = os.getenv("LOGIN_PHONE")
password = os.getenv("PASSWORD")

data = {
    'st.redirect': '',
    'st.asr': '',
    'st.posted': 'set',
    'st.fJS': 'on',
    'st.st.screenSize': '1600 x 900',
    'st.st.browserSize': '739',
    'st.st.flashVer': '0.0.0',
    'st.email': login,
    'st.password': password,
}

url = "https://ok.ru/dk?cmd=AnonymLogin&st.cmd=anonymMain"


class Decor:
    def __init__(self, arg):
        self._arg = arg

    def __call__(self):
        def wrapper(func):
            resp = func()
            if resp.cookies.get("AUTHCODE") is not None:
                return resp
            else:
                print("Not logged")


class ConnectToOk:

    async def login_to_ok(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data) as response:
                #return response.text()
                return response


class OkParser(ConnectToOk):

    def __int__(self, *args, **kwargs):
        self.url = "https://ok.ru/dk?cmd=AnonymLogin&st.cmd=anonymMain"
        self.data = {
            'st.redirect': '',
            'st.asr': '',
            'st.posted': 'set',
            'st.fJS': 'on',
            'st.st.screenSize': '1600 x 900',
            'st.st.browserSize': '739',
            'st.st.flashVer': '0.0.0',
            'st.email': login,
            'st.password': password,
        }


    async def check_messages(self) -> str:
        resp_data = await self.login_to_ok()
        resp_data = await resp_data.text()
        soup = BeautifulSoup(resp_data, "html.parser")
        answer = soup.find(id='counter_ToolbarMessages').text
        print(f"Новых сообщений: {answer}")
        # return answer

    async def check_notifications(self) -> str:
        soup = BeautifulSoup(await self.login_to_ok(self.url, self.data), "html.parser")
        answer = soup.find(id='counter_Notifications').text
        print(f"Новых оповещений: {answer}")
        # return answer


runner = OkParser()
asyncio.run(runner.check_messages())

@Decor
async def hobby_to_ok():
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://ok.ru/hobby') as response:
            print(response.cookies.get("AUTHCODE"))
            return await response.text()

#
# asyncio.run(hobby_to_ok())