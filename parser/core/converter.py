"""Конвертеры текстовых файлов.
"""
import json
from parser.core.enums import DocType, StoreFields
from parser.settings import DOCX_TEMPLATES, POEMS_SEPARATOR
from pathlib import Path

from docxtpl import DocxTemplate, RichText
from pydantic import BaseModel

# Номера пробельных символов
SPACE_CHARS = {160, 32}


class JsonConvereter(BaseModel):
    """Конвертирует `.json` в форматы `.md`, `.docx`.

    #### Attrs
    - json_file (Path): Файл с исходными данными в формаье `json`.
    - doc_type (Enum): Желаемый формат выходного файла.
    - end_text (str): Разделитель текстов.
    - data (list[dict[str, str]] | None): Данные прочитанные из `json_file`.
    """
    json_file: Path
    doc_type: DocType
    end_text: str | None = POEMS_SEPARATOR
    data: list[dict] | None = None

    def __call__(self) -> Path:
        match self.doc_type:
            case DocType.JSON.value:
                return self._to_json()
            case DocType.MD.value:
                return self._to_md()
            case DocType.DOCX.value:
                return self._to_docx()

    def get_data_from_file(self) -> list[dict[str, str]]:
        """Получает данные из связанного JSON-файла.

        #### Returns:
        - list[dict[str, str]]: Прочитанные данные.
        """
        with open(self.json_file) as json_file:
            return json.loads(json_file.read())

    def set_file_extension(self, file: Path, doc_type: str) -> Path:
        """Устанавливает расширение файла.

        #### Args:
        - file (Path): Проверяемое название файла.
        - doc_type (str): Необходимое расширение.

        #### Returns:
        - str: Название файла с расширением.
        """
        if not doc_type.startswith('.'):
            doc_type = '.' + doc_type
        return file.with_suffix('').with_suffix(doc_type)

    def _to_json(self) -> Path:
        """Возвращает файл `.json`.

        #### Returns:
        - Path: Месторасположение выходного файла в формате `.json`.
        """
        return self.set_file_extension(self.json_file, DocType.JSON.value)

    def _to_md(self) -> Path:
        """Конвертирует из `.json` в `.md`.

        #### Returns:
        - Path: Месторасположение выходного файла в формате `.md`.
        """
        out_file = self.set_file_extension(self.json_file, DocType.MD.value)
        res = []

        for poem in self.get_data_from_file():
            title = poem.get(StoreFields.TITLE.value)
            link = poem.get(StoreFields.LINK.value)
            author = poem.get(StoreFields.AUTHOR.value)
            poem_text = poem.get(StoreFields.TEXT.value)
            # TODO: Decrease complexity with switch-case
            if title:
                if link:
                    text = f'### [{title}]({link})\n\n'
                else:
                    text = f'### {title}\n\n'
            if author:
                text += f'*{author}*\n'

            if poem_text:
                md_text = poem_text.split('\n')
                indent = True
                for index, line in enumerate(md_text):
                    space = 0
                    for char in line:
                        if ord(char) not in SPACE_CHARS:
                            break
                        space += 1
                    if space:
                        md_text[index] = '> ' * (space // 2) + line[space:]
                    elif not space and indent:
                        md_text[index] = '\n' + line
                    indent = space
                text += '  \n'.join(md_text) + self.end_text

            res.append(text)

        with open(out_file, 'w') as writer:
            writer.write(''.join(res))

        return out_file

    def __title_link_to_docx(self, file: Path) -> Path:
        """Конвертирует из `.json` в `.docx`.
        В исходном файле должны быть поля `title` и `link`.

        #### Args:
        - file (Path): Название выходного файла.

        #### Returns:
        - Path: Месторасположение выходного файла в формате `.docx`.
        """
        doc = DocxTemplate(DOCX_TEMPLATES / 'title_link.docx')
        title_links = RichText()

        for title_link in self.data:
            title_links.add(
                text=title_link[StoreFields.TITLE.value] + '\n',
                underline=True,
                url_id=doc.build_url_id(title_link[StoreFields.LINK.value])
            )

        doc.render(context={'title_links': title_links})
        doc.save(file)
        return file

    def __poems_to_docx(self, file: Path) -> Path:
        """Конвертирует из `.json` в `.docx`.
        В исходном файле должны быть поля `title`, `author` и `text`.

        #### Args:
        - file (Path): Название выходного файла.

        #### Returns:
        - Path: Месторасположение выходного файла в формате `.docx`.
        """
        doc = DocxTemplate(DOCX_TEMPLATES / 'poems.docx')
        poems = RichText()

        for poem in self.data:
            poems.add(poem[StoreFields.TITLE.value] + '\n\n')
            poems.add(poem[StoreFields.AUTHOR.value] + '\n', color='#FF00FF')
            if isinstance(poem[StoreFields.TEXT.value], str):
                poems.add(poem[StoreFields.TEXT.value] + self.end_text, italic=True)
            else:
                poems.add(''.join(poem[StoreFields.TEXT.value]) + self.end_text, italic=True)

        doc.render(context={'poems': poems})
        doc.save(file)
        return file

    def _to_docx(self) -> Path:
        """Вызывает нужную функцию для конвертации из `.json` в `.docx`.

        #### Returns:
        - Path: Месторасположение выходного файла в формате `.docx`.

        #### Raises:
        - ValueError: Для переданного файла нет подходящего шаблона `docx`.
        """
        file = self.set_file_extension(self.json_file, DocType.DOCX.value)
        self.data = self.get_data_from_file()
        if len(self.data) == 0:
            return self.__title_link_to_docx(file)

        keys_set = set(self.data[0].keys())

        if {StoreFields.TITLE.value, StoreFields.LINK.value} == keys_set:
            return self.__title_link_to_docx(file)

        if {
            StoreFields.TITLE.value, StoreFields.AUTHOR.value, StoreFields.TEXT.value
        } == keys_set:
            return self.__poems_to_docx(file)

        raise ValueError(
            'Для переданного файла нет подходящего шаблона `docx`'
        )
