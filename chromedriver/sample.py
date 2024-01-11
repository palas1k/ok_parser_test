import aiohttp


class SessionManager:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    def get_session(self):
        return self.session


def auth_required(func):
    async def wrapper(self, *args, **kwargs):
        if not self.is_authenticated:
            raise Exception("Authentication required")
        return await func(self, *args, **kwargs)

    return wrapper


class AuthenticatedChecker:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.is_authenticated = False  # Изначально пользователь не аутентифицирован

    async def authenticate(self, username, password):
        # Здесь вы можете использовать aiohttp и переданную сессию для выполнения проверки аутентификации пользователя.
        # Например, отправка запроса к API или проверка в базе данных.
        session = self.session_manager.get_session()
        # Пример асинхронного запроса к какому-либо URL с использованием aiohttp
        async with session.get('https://example.com/api/auth',
                               params={'username': username, 'password': password}) as response:
            if response.status == 200:
                self.is_authenticated = True
                return True
            else:
                self.is_authenticated = False
                return False

    @auth_required
    async def get_data(self, url):
        # Этот метод требует аутентификации пользователя
        session = self.session_manager.get_session()
        async with session.get(url) as response:
            data = await response.text()
            return data

    @auth_required
    async def post_data(self, url, data):
        # Этот метод требует аутентификации пользователя
        session = self.session_manager.get_session()
        async with session.post(url, data=data) as response:
            result = await response.text()
            return result


# Пример использования:

async def main():
    session_manager = SessionManager()
    auth_checker = AuthenticatedChecker(session_manager)

    username = "example_user"
    password = "example_password"

    is_authenticated = await auth_checker.authenticate(username, password)

    if is_authenticated:
        print(f"User {username} is authenticated.")

        # Пример использования методов get_data и post_data
        data = await auth_checker.get_data('https://example.com/api/data')
        print("Data:", data)

        result = await auth_checker.post_data('https://example.com/api/post', {'key': 'value'})
        print("Result:", result)
    else:
        print(f"User {username} is not authenticated.")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    