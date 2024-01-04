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


async def login():
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=data) as response:
            return await response.text()


class OkParser:

    async def check_messages(self):
        resp = await login()
        soup = BeautifulSoup(resp, "html.parser")
        answer = soup.find(id='counter_ToolbarMessages').text
        print(f'Новых сообщений: {answer}')


    async def check_notifications(self):
        resp = await login()
        soup = BeautifulSoup(resp, "html.parser")
        answer = soup.find(id='counter_Notifications').text
        print(f'Новых оповещений: {answer}')


asyncio.run(OkParser().check_login())
