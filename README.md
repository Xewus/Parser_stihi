## Парсер сайта www.stihi.ru \**

#### Возможности
- Скачать все стихи указанного автора.
- Скачать выбранные стихи.
- Скачать список стихов в виде списка [Названий](ссылка).

Скачивание доступно в форматах ***.json***, ***.md***, ***.docx*** .

#### Использовано
- [Python](https://www.python.org/downloads/release/python-3107/)
- [Scrapy](https://scrapy.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tortoise ORM](https://tortoise.github.io/)
- [SQLite](https://www.sqlite.org/index.html)

#### Примечания
- \** ***Прежде всего, вам, конечно, следует руководствоваться законодательством в интелектуальной сфере.***
- Но портале зарегистрировано порядка миллиона писателей с различным уровнем образования и более 50 миллионов произведений. Парсер ${\color{yellow}не\ обрабатывает\ их\ грамматические\ и\ синтаксические\ ошибки}$, такие как - лишние пробелы, отсутствующие запятые и т.п. Текст произведения скачивается ${\color{yellow}как\ есть}$. 
Отступы также сохранены, так как могут быть авторскими, яркий пример - Владимир Маяковский.
Кроме того, среди этих миллионов вполне может встретиться текст, который парсер обработает некорректно, что потребует некоторой доработки, но пока такого случая не было.

- Предполагается, что сервисом будут пользоваться всего несколько человек, потому, для упрощения обслуживания, управление доступом к сервису осуществлется с использованием СУБД SQLite.

- Защиту ${\color{green}stihi.ru}$ осуществляет сервис ${\color{red}Qrator}$. На момент релиза настройки парсера позволяют обходить ограничения. Но ${\color{yellow}не\ гарантируется}$, что в будущем не понадобится изменить настройки.