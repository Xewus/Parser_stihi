"""Эндпоинты для управления парсингом.
"""
from pathlib import Path
from parser.core.enums import Tag, SpiderNames, DocType
from parser.core.validators import validate_author
from parser.poems.commands import start_spider
from parser.web.schemas import ChooseParsingSchema, RespUriSchema
from parser.core.utils import extract_poem_links

from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse, FileResponse
from parser.core.converter import JsonConvereter


router = APIRouter(tags=[Tag.PARSING])


@router.post(
    path='/choose_parsing/',
    summary='Принимает параметры для запуска парсера',
    response_description='Перенаправляет на ресурс дальнейшего выбора действий',
)
async def choose_parsing_view(
    args: ChooseParsingSchema= Body(
        ..., examples=ChooseParsingSchema.Config.schema_extra['examples']
    )
):
    args.author = await validate_author(args.author)
    if args.spider == SpiderNames.CHOOSE_POEMS.value:
        result_file = await start_spider(
            spider=SpiderNames.LIST_POEMS, author=args.author
        )
        poem_links = await extract_poem_links(result_file)


    uri = await start_spider(**args.dict())
    return await download_file(uri, DocType.JSON)


@router.post('/choose_poems/')
async def choose_poems_view():
    """Выбрать стихи из списка.

    Returns:
        _type_: _description_
    """
    return {"message": "choose_poems"}


@router.get('/download_file/{doc_type}')
async def download_file(
    json_file: str | Path,
    doc_type = DocType
):
    converter = JsonConvereter(json_file, doc_type)
    out_file = str(converter())
    return FileResponse(
        path=out_file,
        media_type='application/octet-stream',
        filename=out_file.split('/')[-1]
    )


