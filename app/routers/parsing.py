"""Эндпоинты для управления парсингом.
"""
from fastapi import APIRouter,Body
from fastapi.responses import RedirectResponse

from app.core.enums import Tag
from app.schemas import ParsingArgsSchema
from app.core.settings import APP_KEY, HEADERS, WEB_SCRAPY_URL, POEMS_STORE
from app.core.requests import SendRequest
from app.core.validators import validate_author

router = APIRouter(tags=[Tag.PARSING])


@router.post(
    path='/choose_parsing/',
    summary='Принимает параметры для парсинга.'
)
async def choose_parsing_view(
    parsing_data: ParsingArgsSchema = Body(
        ..., examples=ParsingArgsSchema.Config.schema_extra['examples']
    )
):
    await validate_author(parsing_data.author)

    request = SendRequest(url=WEB_SCRAPY_URL, data=parsing_data.json(), headers=HEADERS)
    response = await request.POST
    return await response.json()

    # err = response.get('error')
    # if err:
    #     raise HTTPException(400, err)
    # return RedirectResponse(
    #     '/parsing/wait_parsing?author=' + author,
    #     status_code=302
    # )


# @router.get('/choose_poems/')
# async def choose_poems_view():
#     """Выбрать стихи из списка.

#     Returns:
#         _type_: _description_
#     """
#     return {"message": "choose_poems"}


# @router.get('/choose_download/')
# async def choose_download_view():
#     """Выбрать тип загружаемого файла.

#     Returns:
#         _type_: _description_
#     """
#     return {"message": "choose_download"}


# @router.get('/download/<doc_type>')
# async def download_view(doc_type: str):
#     """Загрузить файл.

#     Args:
#         doc_type (str): _description_

#     Returns:
#         _type_: _description_
#     """
#     return {"message": "fule"}

# @router.get('/wait_parsing')
# async def wait_parsing(
#         author: str = Query(
#         title='Автор произведений'
#     )
# ):
#     out_file = Path(POEMS_STORE % author)
#     while not out_file.exists():
#         await sleep(1)
#     print(555555555555)
#     return {'file': out_file}


# @router.get('/choose_parsing/{spider_name}')
# async def choose_parsing_view(
#     spider_name: SpiderNames,
#     author: str = Query(
#         title='Автор произведений',
#         description='URL-ссылка на страницу автора.'
#     )
# ):
#     """Выбрать тип парсинга.

#     ### Args:
#     - **spider (SpiderNames)**: Тип парсинга.
#     - **author (optional)**: Автор произведений.

#     Returns:
#         _type_: _description_
#     """
#     out_file = Path(POEMS_STORE % author)
#     if out_file.exists():
#         out_file.unlink()

#     params={'spider':spider_name, 'author':author}
#     headers = {'AUTH_KEY': AUTH_KEY}

#     response = requests.get(url=SCRAPY_URL, params=params, headers=headers).json()
#     err = response.get('error')
#     if err:
#         raise HTTPException(400, err)
#     return RedirectResponse(
#         '/parsing/wait_parsing?author=' + author,
#         status_code=302
#     )


# # @router.get('/choose_poems/')
# # async def choose_poems_view():
# #     """Выбрать стихи из списка.

# #     Returns:
# #         _type_: _description_
# #     """
# #     return {"message": "choose_poems"}


# # @router.get('/choose_download/')
# # async def choose_download_view():
# #     """Выбрать тип загружаемого файла.

# #     Returns:
# #         _type_: _description_
# #     """
# #     return {"message": "choose_download"}


# # @router.get('/download/<doc_type>')
# # async def download_view(doc_type: str):
# #     """Загрузить файл.

# #     Args:
# #         doc_type (str): _description_

# #     Returns:
# #         _type_: _description_
# #     """
# #     return {"message": "fule"}
