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


def logged_check(func):
    async def wrapped(*args):
        resp = await func(*args)
        if ConnectToOk().session is not None:
            return resp
        else:
            return None

    return wrapped


class ConnectToOk:
    session = None

    def start_session(self):
        return aiohttp.ClientSession()

    async def stop_session(self):
        return self.session.close()

    # post
    async def get_data(self):
        self.session = await self.start_session().post(url=url, data=data)
        return self.session


class OkParser:

    obj = ConnectToOk()

    async def get_data(self):
        obj = await self.obj.get_data()
        return await obj.text()

    async def stop_session(self):
        await self.obj.stop_session()



    @logged_check
    async def check_messages(self) -> str:
        resp_data = await self.get_data()
        soup = BeautifulSoup(resp_data, "html.parser")
        answer = soup.find(id='counter_ToolbarMessages').text
        print(f"Новых сообщений: {answer}")
        await self.stop_session()
        # return answer

    @logged_check
    async def check_notifications(self) -> str:
        resp_data = await self.get_data()
        soup = BeautifulSoup(resp_data, "html.parser")
        answer = soup.find(id='counter_Notifications').text
        if answer != '':
            print(f"Новых оповещений: {answer}")
        else:
            print("Новых оповещений нет")
        await self.stop_session()
        # return answer


runner = OkParser()
asyncio.run(runner.check_messages())

# runner = ConnectToOk()
# asyncio.run(runner.auth_to_ok())


@logged_check
async def hobby_to_ok():
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://ok.ru/hobby') as response:
            print(response.cookies.get("AUTHCODE"))
            return await response.text()


# asyncio.run(hobby_to_ok())
