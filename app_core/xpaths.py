""" Строки в формате `xpath` для парсера.
"""

body_page = '//*[@class="maintext"]'
title_page = '*/h1/text()'
amount_poems = '//p[contains(., "Произведений")]/b/text()'
poem_link = '//*[@class="poemlink"]'

author_on_poem_page = '//*[@class="titleauthor"]/*/a/text()'
poem_text = '//*[@class="text"]/text()'
