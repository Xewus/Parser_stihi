from pathlib import Path
from app_core import settings
import json
import pypandoc
from docxtpl import DocxTemplate, RichText

TEXT = settings.TEXT
AUTHOR = settings.AUTHOR
TITLE = settings.TITLE
LINK = settings.LINK
POEMS_STORE = settings.POEMS_STORE


class JsonConvereter:
    def __init__(self, doc_type: str, json_file: str | Path | None = None) -> None:
        if doc_type == 'json':
            self.converter = self._to_json
        elif doc_type == 'md':
            self.converter = self._to_md
        elif doc_type == 'docx':
            self.converter = self._to_docx
        else: raise

        if json_file is None:
            json_file = POEMS_STORE
        self.json_file = json_file

        with open(self.json_file) as file:
            self.data = json.loads(file.read())
        self.end_text = '\n' + '-' * 30 + '\n\n'

    def _to_json(self, out_file: str) -> str:
        if not out_file.endswith('json'):
            out_file = f'{out_file}.json'
        Path(self.json_file).rename(out_file)
        return out_file

    def _to_md(self, out_file: str) -> str:
        """Записывает из .json в .md

        Args:
            out_file (_type_): _description_
        """
        if not out_file.endswith('md'):
            out_file = f'{out_file}.md'
        res = []
        for poem in self.data:
            if TITLE in poem:
                if LINK in poem:
                    text = f'### [{poem[TITLE]}]({poem[LINK]})\n\n'
                else:
                    text = f'### {poem[TITLE]}\n\n'
            if AUTHOR in poem:
                text += f'*{poem[AUTHOR]}*\n\n'
            if TEXT in poem:
                if isinstance(poem[TEXT], str):
                    text += poem[TEXT] + self.end_text
                else:
                    text += ''.join(poem[TEXT]) + self.end_text
            res.append(text)
        with open(out_file, 'w') as writer:
            writer.write(''.join(res))
        return out_file

    def _title_link_to_docx(self, out_file: str) -> str:
        doc = DocxTemplate(settings.DOCX_TEMPLATES / 'title_link.docx')
        title_links = RichText()
        for title_link in self.data:
            title_links.add(title_link)
        
        context = {'title_links': title_links}
        doc.render(context)
        doc.save(out_file)
        return out_file

    def _poems_to_docx(self, out_file: str) -> str:
        doc = DocxTemplate(settings.DOCX_TEMPLATES / 'poems.docx')
        poems = RichText()
        for poem in self.data:
            poems.add(f'{poem[TITLE]}\n\n', size=16)
            poems.add(f'{poem[AUTHOR]}\n', size=12, color='#F0F')
            if isinstance(poem[TEXT], str):
                poems.add(poem[TEXT] + self.end_text, italic=True)
            else:
                poems.add(''.join(poem[TEXT]) + self.end_text, italic=True)
        
        context = {'poems': poems}
        doc.render(context)
        doc.save(out_file)
        return out_file

    def _to_docx(self, out_file: str) -> str:
        if not out_file.endswith('docx'):
            out_file = f'{out_file}.docx'
        keys_set = set(self.data[0].keys())
        if len(self.data) == 0 or {TITLE, LINK} == keys_set:
            return self._title_link_to_docx(out_file)
        if {TITLE, AUTHOR, TEXT} == keys_set:
            return self._poems_to_docx(out_file)
        raise
