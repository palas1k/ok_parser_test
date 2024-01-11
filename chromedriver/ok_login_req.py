import aiohttp
import asyncio
import os

from dotenv import load_dotenv

from bs4 import BeautifulSoup

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
login = os.getenv("LOGIN_PHONE")
password = os.getenv("PASSWORD")


def logged_check(func):
    async def wrapped(*args):
        resp = await func(*args)
        if resp is not None:
            return resp
        else:
            print("Non logged")
            return None

    return wrapped


class Auth:
    session = None
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

    # @logged_check
    def start_session(self):
        print(self.session)
        self.session = aiohttp.ClientSession()
        return self.session

    @logged_check
    def get_data(self):
        conn = self.start_session()
        r = conn.post(url=self.url, data=self.data)
        return r

    async def session_close(self):
        if self.session is not None:
            print(self.session)
            await self.session.close()
            self.session = None
            print("Session close")
            print(self.session)


class OkParser:

    def __init__(self):
        self.auth_session = Auth()

    async def get_data(self):
        print('Перед получением данных')
        obj = await self.auth_session.get_data()
        print("Получение данных")
        await self.auth_session.session_close()
        return await obj.text()

    async def check_messages(self) -> str:
        resp_data = await self.get_data()
        soup = BeautifulSoup(resp_data, "html.parser")
        answer = soup.find(id='counter_ToolbarMessages').text
        print(f"Новых сообщений: {answer}")

    async def check_notifications(self) -> str:
        resp_data = await self.get_data()
        soup = BeautifulSoup(resp_data, "html.parser")
        answer = soup.find(id='counter_Notifications').text
        if answer != '':
            print(f"Новых оповещений: {answer}")
        else:
            print("Новых оповещений нет")
        await self.auth_session.session_close()


runner = OkParser()
asyncio.run(runner.check_messages())
