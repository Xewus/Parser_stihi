from aiohttp import ClientResponse, ClientSession
from aiohttp.client_exceptions import ClientError


class SendRequest:
    """Посылает запросы к сторонним серверам.
    """
    def __init__(
        self,
        url: str,
        data: dict | None = None,
        headers: dict | None = None
    ) -> None:
        self.url = url
        self.data = data
        self.headers = headers

    async def __request_get(self) -> ClientResponse:
        try:
            async with ClientSession(headers=self.headers, conn_timeout=1.3) as session:
                response = await session.get(url=self.url, allow_redirects=False)
                print('_S_R', id(response), response.host)
                return response
        except ClientError:
            return

    async def __request_post(self) -> ClientResponse:
        try:
            async with ClientSession(headers=self.headers, conn_timeout=1.3) as session:
                return await session.post(url=self.url, data=self.data)

        except ClientError:
            return

    @property
    async def GET(self) -> ClientResponse | None:
        response =  await self.__request_get()
        await response.text()
        return response
    
    @property
    async def POST(self) -> ClientResponse | None:
        return await self.__request_post()
