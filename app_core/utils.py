import docx


def extract_author(dirty_string: str) -> str:
    """Вытаскивает имя автора их строки.

    Args:
        dirty_string (str): _description_

    Raises:
        Exception: _description_

    Returns:
        str: _description_
    """
    dirty_list = dirty_string.split('/')
    if len(dirty_list) == 1:
        return dirty_list[0]
    for i, v in enumerate(dirty_list):
        print(v)
        if v == 'avtor' and i < len(dirty_list) - 1:
            return (dirty_list[i + 1])
    raise Exception(f'no author in {dirty_list}')


def clean_poem_text(text: list) -> list:
    """Отрезает текст стиха от нижележащих примечаний.

    #### Args:
        text (list): Текст стиха.

    #### Returns:
        text (list): Обрезанный текст стиха.
    """
    n = 0
    for index, line in enumerate(text):
        n = n + 1 if line == '\n' else 0
        if n == 2:
            text = text[:index]
    return text


def add_hyperlink(paragraph, url, text):
    """
    A function that places a hyperlink within a paragraph object.

    :param paragraph: The paragraph we are adding the hyperlink to.
    :param url: A string containing the required url
    :param text: The text displayed for the url
    :return: The hyperlink object
    """

    # This gets access to the document.xml.rels file and
    # gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(
        url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True
    )

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
    hyperlink.set(docx.oxml.shared.qn('r:id'), r_id, )

    # Create a w:r element
    new_run = docx.oxml.shared.OxmlElement('w:r')

    # Create a new w:rPr element
    rPr = docx.oxml.shared.OxmlElement('w:rPr')

    # Join all the xml elements together add
    # the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    paragraph._p.append(hyperlink)

    return hyperlink
