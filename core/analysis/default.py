from statistics import mean
from core.data.dataclasses import Price


def get_avg_prices(prices: list[Price]) -> Price:
    item = prices[0].item
    city = prices[0].city
    quantity = len(prices)
    sell_price_min = int(mean([price.sell_price_min for price in prices]))
    sell_price_max = int(mean([price.sell_price_max for price in prices]))
    buy_price_min = int(mean([price.buy_price_min for price in prices]))
    buy_price_max = int(mean([price.buy_price_max for price in prices]))

    # For dates, you may need to decide how to handle them. Here, I'm simply taking the earliest and latest dates.
    sell_price_min_date = min(price.sell_price_min_date for price in prices)
    sell_price_max_date = max(price.sell_price_max_date for price in prices)
    buy_price_min_date = min(price.buy_price_min_date for price in prices)
    buy_price_max_date = max(price.buy_price_max_date for price in prices)

    return Price(item=item,
                 city=city,
                 quantity=quantity,
                 sell_price_min=sell_price_min,
                 sell_price_min_date=sell_price_min_date,
                 sell_price_max=sell_price_max,
                 sell_price_max_date=sell_price_max_date,
                 buy_price_min=buy_price_min,
                 buy_price_min_date=buy_price_min_date,
                 buy_price_max=buy_price_max,
                 buy_price_max_date=buy_price_max_date)