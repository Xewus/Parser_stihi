from .author import AllPoemsSpider, ChooseSpider, BasePoemsSpider, ListPoemsSpider

SPIDERS = (
    AllPoemsSpider, ListPoemsSpider, ChooseSpider
)

def get_spider_by_name(name: str) -> BasePoemsSpider | None:
    """Получает паука по имени.

    Args:
        name (str): Имя нужного паука.

    Returns:
        BasePoemsSpider | None: Найденный паук.
    """
    for spider in SPIDERS:
        if spider.name == name:
            return spider
