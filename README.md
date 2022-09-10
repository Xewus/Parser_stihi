## Парсер сайта www.stihi.ru

#### Возможности
- Скачать все стихи указанного автора.
- Скачать выбранные стихи.
- Скачать список стихов в виде [Название](ссылка).

Скачивание доступно в форматах ***.json***, ***.md***, ***.docx*** .

#### Использовано
- [Python 3.10.7](https://www.python.org/downloads/release/python-3107/)
- [Scrapy 2.6.2](https://scrapy.org/)
- [Flask 2.2.2](https://flask.palletsprojects.com/en/latest/)

#### Примечания
- Но портале зарегистрировано порядка миллиона писателей с различным уровнем образования с сотнями и тысячами произведений. Парсер **не обрабатывает их грамматические и синтаксические ошибки**, такие как - лишние пробелы и отступы, отсутствующие запятые и т.п. Текст произведения скачивается **как есть**.
- Предполагается, что сервисом будут пользоваться несколько человек и он не сохраняет никакие данные, взламывать и красть нечего. Потому, для упрощения обслуживания, никакие СУБД и СБ не подключены, данные для обеспечения доступа пользователям упрощены и пишутся в обычный файл.