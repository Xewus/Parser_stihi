"""Работа с внешними ресурсами.
"""
from aiohttp import ClientResponse, ClientSession
from aiohttp.client_exceptions import ClientError
from pydantic import BaseModel, HttpUrl


class SendRequest(BaseModel):
    """Посылает запросы к сторонним сервисам.
    """
    url: HttpUrl
    data: dict | None
    headers: dict[str, str] | None

    async def __request_get(self) -> ClientResponse | None:
        try:
            async with ClientSession(
                headers=self.headers, conn_timeout=1.3
            ) as session:
                response = await session.get(url=self.url)
                return response
        except ClientError:
            return

    async def __request_post(self) -> ClientResponse | None:
        try:
            async with ClientSession(
                headers=self.headers, conn_timeout=1.3
            ) as session:
                return await session.post(url=self.url, data=self.data)

        except ClientError:
            return

    @property
    async def GET(self) -> ClientResponse | None:
        response = await self.__request_get()
        if response is not None:
            # WTF: Без этого действия контекст теряет
            # тело ответа при выходе из функции!!!
            await response.text()
        return response

    @property
    async def POST(self) -> ClientResponse | None:
        return await self.__request_post()
