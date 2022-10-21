"""Вспомогательные функции.
"""

import shutil
from datetime import datetime, timedelta
from pathlib import Path

from aiohttp import ClientSession, ClientResponse
from aiohttp.client_exceptions import ClientError

from core.settings import DATE_FORMAT, RESULT_DIR


def clean_poem_text(text: list[str]) -> str:
    """Отрезает текст стиха от нижележащих примечаний.

    #### Args:
    - text (list[str]): Текст стиха.

    #### Returns:
    - text (str): Текст стиха.
    """
    counter = 0
    for index, line in enumerate(text):
        counter = counter + 1 if line == '\n' else 0
        if counter == 3:
            text = text[:index]
    return ''.join(text)


def dir_manager() -> Path:
    """Создаёт папку для сохранения результатов парсинга и удалет устаревшую.
    """
    today = datetime.today()
    two_days_ago = today - timedelta(days=2)
    today = today.strftime(DATE_FORMAT)
    two_days_ago = two_days_ago.strftime(DATE_FORMAT)

    today_dir = Path(RESULT_DIR % today)
    two_days_ago_dir = Path(RESULT_DIR % two_days_ago)

    if two_days_ago_dir.exists():
        shutil.rmtree(two_days_ago_dir)
    if not today_dir.exists():
        today_dir.mkdir()
    return today_dir


class SendRequest:
    def __init__(
        self,
        url: str,
        data: dict | None = None,
        headers: dict | None = None
    ) -> None:
        self.url = url
        self.data = data
        self.headers = headers

    async def __request_get(self, session: ClientSession) -> ClientResponse:
        async with session.get(url=self.url, allow_redirects=False) as response:
            await response.text()
            return response

    async def __request_post(self, session: ClientSession) -> ClientResponse:
        async with session.post(url=self.url, data=self.data) as response:
            return response

    async def _send_request(self, request_method) -> ClientResponse | None:
        try:
            async with ClientSession(headers=self.headers, conn_timeout=1.3) as session:
                response = await request_method(session=session)
                return response
        except ClientError:
            return

    @property
    async def GET(self) -> ClientResponse | None:
        return await self._send_request(self.__request_get)
    
    @property
    async def POST(self) -> ClientResponse | None:
        return await self._send_request(self.__request_post)
