import time
from datetime import datetime

import pandas as pd
import requests

import core.settings as settings
from core.data.dataclasses import Price, City, Item


def get_current_prices(item_core, tier=4, qualities=0) -> list[Price]:
    item_id = f'T{tier}_{item_core}'

    data = requests.get(f'{settings.SERVER_URL}/stats/prices/{item_id}?qualities={qualities}')
    data = data.json()

    result = []

    item = Item.find(id=item_id)
    if Item.find(item_id) is None:
        item = Item(item_id)
        item.save()

    for entry in data:
        city_id = entry['city']

        city = City.find(id=city_id)
        if city is None:
            city = City(city_id)
            city.save()

        result.append(Price(
            item,
            city,
            0,
            entry['sell_price_min'],
            datetime.fromisoformat(entry['sell_price_min_date']),
            entry['sell_price_max'],
            datetime.fromisoformat(entry['sell_price_max_date']),
            entry['buy_price_min'],
            datetime.fromisoformat(entry['buy_price_min_date']),
            entry['buy_price_max'],
            datetime.fromisoformat(entry['buy_price_max_date'])
        ))

    return result
