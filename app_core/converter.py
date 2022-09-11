"""Конвертеры текстовых файлов.
"""
import json
import shutil
from pathlib import Path

from docxtpl import DocxTemplate, RichText

from app_core import settings

TEXT = settings.TEXT
AUTHOR = settings.AUTHOR
TITLE = settings.TITLE
LINK = settings.LINK
POEMS_STORE = settings.POEMS_STORE
POEMS_SEPARATOR = settings.POEMS_SEPARATOR
SPACE_CHARS = {160, 32}


class JsonConvereter:
    """Конвертирует `.json` в форматы `.md`, `.docx`.

    #### Attrs
    - doc_type (str): Желаемый формат выходного файла.
    - json_file (str): Файл с исходными данными в формаье `json`.
    - end_text (str): Разделитель текстов.
    """
    def __init__(
        self,
        doc_type: str,
        json_file: str | Path | None = None,
        end_text: str | None = None
    ) -> None:
        if doc_type == 'json':
            self.converter = self._to_json
        elif doc_type == 'md':
            self.converter = self._to_md
        elif doc_type == 'docx':
            self.converter = self._to_docx
        else:
            raise ValueError (f'Неправильный формат `{doc_type}`')

        self.json_file = json_file or POEMS_STORE
        self.end_text = end_text or POEMS_SEPARATOR

    @property
    def __get_data_from_file(self) -> list[dict[str, str]]:
        """Получает данные из связанного JSON-файла.

        Returns:
            list[dict[str, str]]: Прочитанные данные
        """
        with open(self.json_file) as json_file:
            data = json.loads(json_file.read())
        return data

    def checked_filename(self, filename: str, doc_type: str) -> str:
        """Проверяет расширение файла.

        Args:
            filename (str): Проверяемое название файла.
            doc_type (str): Необходимое расширение.

        Returns:
            str: Название файла с расширением.
        """
        if not filename.endswith(doc_type):
            return f'{filename}.{doc_type}'
        return filename

    def _to_json(self, out_file: str) -> str:
        """Копирует входной файл в выходной.

        #### Args:
            out_file (str): Название выходного файла.

        #### Returns:
            str: Название выходного файла.
        """
        out_file = self.checked_filename(out_file, 'json')
        shutil.copy(self.json_file, out_file)
        return out_file

    def _to_md(self, out_file: str) -> str:
        """Конвертирует из `.json` в `.md` .

        #### Args:
            out_file (str): Название выходного файла.

        #### Returns:
            str: Название выходного файла.
        """
        out_file = self.checked_filename(out_file, 'md')
        res = []
        for poem in self.__get_data_from_file:
            if TITLE in poem:
                if LINK in poem:
                    text = f'### [{poem[TITLE]}]({poem[LINK]})\n\n'
                else:
                    text = f'### {poem[TITLE]}\n\n'
            if AUTHOR in poem:
                text += f'*{poem[AUTHOR]}*\n\n'

            if TEXT in poem:
                md_text = poem[TEXT].split('\n')
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

    def __title_link_to_docx(self, out_file: str) -> str:
        """Конвертирует из `.json` в `.docx` .
        В исходном файле должны быть поля `title` и `link`.

        #### Args:
            out_file (str): Название выходного файла.

        #### Returns:
            str: Название выходного файла.
        """
        doc = DocxTemplate(settings.DOCX_TEMPLATES / 'title_link.docx')
        title_links = RichText()

        for title_link in self.data:
            title_links.add(
                text=title_link[TITLE] + '\n',
                underline=True,
                url_id=doc.build_url_id(title_link[LINK])
            )

        doc.render(context={'title_links': title_links})
        doc.save(out_file)
        return out_file

    def __poems_to_docx(self, out_file: str) -> str:
        """Конвертирует из `.json` в `.docx` .
        В исходном файле должны быть поля `title`, `author` и `text`.

        #### Args:
            out_file (str): Название выходного файла.

        #### Returns:
            str: Название выходного файла.
        """
        doc = DocxTemplate(settings.DOCX_TEMPLATES / 'poems.docx')
        poems = RichText()

        for poem in self.data:
            poems.add(f'{poem[TITLE]}\n\n')
            poems.add(f'{poem[AUTHOR]}\n', color='#FF00FF')
            if isinstance(poem[TEXT], str):
                poems.add(poem[TEXT] + self.end_text, italic=True)
            else:
                poems.add(''.join(poem[TEXT]) + self.end_text, italic=True)

        doc.render(context={'poems': poems})
        doc.save(out_file)
        return out_file

    def _to_docx(self, out_file: str) -> str:
        """Вызывает нужную функцию для конвертации из `.json` в `.docx` .

        #### Args:
            out_file (str): Название выходного файла.

        #### Returns:
            str: Название выходного файла.
        #### Raises:
            ValueError: Для переданного файла нет подходящего шаблона `docx`.
        """
        out_file = self.checked_filename(out_file, 'docx')
        self.data = self.__get_data_from_file
        if len(self.data) == 0:
            return self.__title_link_to_docx(out_file)

        keys_set = set(self.data[0].keys())
        if {TITLE, LINK} == keys_set:
            return self.__title_link_to_docx(out_file)
        if {TITLE, AUTHOR, TEXT} == keys_set:
            return self.__poems_to_docx(out_file)
        raise ValueError(
            'Для переданного файла нет подходящего шаблона `docx`'
        )
