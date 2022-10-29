"""Эндпоинты для управления парсингом.
"""
from parser.core.converter import JsonConvereter
from parser.core.enums import DocType, SpiderNames, Tag
from parser.core.utils import extract_poem_links, get_result_file
from parser.core.validators import valdate_file, validate_author
from parser.poems.commands import start_spider
from parser.web.schemas import (AuthorDocTypeSchema, AuthorSchema,
                                ChoosedPoemsSchema, RespChoosePoemsSchema)
from pathlib import Path

from fastapi import APIRouter, Body, Query
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from pydantic import HttpUrl

router = APIRouter(tags=[Tag.PARSING])


@router.post(
    path='/all-poems',
    summary='Скачать все стихи автора',
    description='Парсит все тексты стихов указанного автора, '
    'затем предлагает скачать файл в выбранном формате.',
    response_class=FileResponse
)
async def all_poems_view(
    args: AuthorDocTypeSchema = Body(
        examples=AuthorDocTypeSchema.Config.schema_extra['examples']
    )
):
    file = await start_spider(
        spider=SpiderNames.ALL_POEMS.value,
        author=await validate_author(args.author)
    )
    return await download_file(file, args.doc_type)


@router.post(
    path='/list-poems',
    summary='Скачать список всех стихов',
    description='Парсит все название стихов указанного автора и '
    'ссылки на эти стихи, затем предлагает скачать файл в выбранном формате.',
    response_class=FileResponse
)
async def list_poems_view(
    args: AuthorDocTypeSchema = Body(
        examples=AuthorDocTypeSchema.Config.schema_extra['examples']
    )
):
    file = await start_spider(
        spider=SpiderNames.LIST_POEMS.value,
        author=await validate_author(args.author)
    )
    return await download_file(file, args.doc_type)


@router.get(
    path='/choose_poems',
    summary='Выбрать стихи для парсинга',
    description='Выдаёт список названий стихов указанного '
    'автора с ссылками на эти стихи.',
    response_model=RespChoosePoemsSchema
)
async def get_poems_view(
    author: str | HttpUrl = Query(
        examples=AuthorSchema.Config.schema_extra['examples']
    )
):
    author = await validate_author(author)
    file = await get_result_file(author, SpiderNames.LIST_POEMS.value)
    if not file.exists():
        file = await start_spider(
        spider=SpiderNames.LIST_POEMS.value,
        author=author
    )
    return RespChoosePoemsSchema(author=author, poems = await extract_poem_links(file))


@router.post(
    path='/choose_poems',
    summary='Скачать выбранные стихи',
    description='Парсит все тексты стихов по указанным ссылкам, '
    'затем предлагает скачать файл в выбранном формате.',
    response_class=FileResponse
)
async def choosed_poems_view(
    args: ChoosedPoemsSchema = Body(
        example=ChoosedPoemsSchema.Config.schema_extra['example']
    )
):
    file = await start_spider(
        spider=SpiderNames.CHOOSE_POEMS.value,
        author=await validate_author(args.author),
        urls=args.urls
    )
    return await download_file(file, args.doc_type)


async def download_file(file: Path, doc_type: DocType):
    await valdate_file(file)
    converter = JsonConvereter(json_file=file, doc_type=doc_type)
    file = converter()
    return FileResponse(
        path=file,
        media_type='application/octet-stream',
        filename=str(file).split('/')[-1]
    )
