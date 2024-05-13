import datetime

from dataclasses import dataclass
from core.data.database import Model


@dataclass
class Item(Model):
    id: str

    name: str = 'Unknown'
    description: str = 'No description'
    price: float = 0.0
    image_url: str = 'https://orientacorp.ru'
    link: str = 'https://orientacorp.ru/'


@dataclass
class City(Model):
    id: str

    name: str = 'Unknown'
    description: str = 'No description'
    color: str = '#DDDDDD'
    is_portal: bool = False


@dataclass
class Price(Model):
    item: Item
    city: City

    quantity: int
    sell_price_min: int
    sell_price_min_date: datetime.datetime
    sell_price_max: int
    sell_price_max_date: datetime.datetime
    buy_price_min: int
    buy_price_min_date: datetime.datetime
    buy_price_max: int
    buy_price_max_date: datetime.datetime
