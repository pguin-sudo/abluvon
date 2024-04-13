import json
import random
import time
from datetime import datetime

import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from normalize import correct_data


locations_colors = {
    'Black Market': '#444444',
    'Brecilien': '#000000',
    'Caerleon': '#FF0000',
    'Thetford': '#FF00FF',
    'Fort Sterling': '#00FFFF',
    'Lymhurst': '#00FF00',
    'Bridgewatch': '#FF2222',
    'Martlock': '#0000FF'
}


def get_location_color(location_name: str) -> str:
    for location in locations_colors:
        if location in location_name:
            return locations_colors[location]
    return '#DDDDDD'


def get_location_marker(location_name: str) -> str:
    if 'Portal' in location_name:
        return '--'
    return '-'


def get_current_prices(item_name, qualities=0, filter=''):
    data = requests.get(f'https://west.albion-online-data.com/api/v2/stats/prices/{item_name}?qualities={qualities}')
    data = data.json()
    with open(f'data/current_prices/{item_name}-{time.time()}-{qualities}.json', 'w+') as file:
        json.dump(data, file)

    result = {}
    for d in data:
        location = d['city']
        result[location] = (
        d['quality'], d['sell_price_min'], d['sell_price_max'], d['buy_price_min'], d['buy_price_max'])
    return result


def get_avg_prices(item_name, qualities=0, filter='', interval=1) -> dict:
    data = requests.get(
        f'https://west.albion-online-data.com/api/v2/stats/history/{item_name}?time-scale={interval}&qualities={qualities}')
    data = data.json()
    with open(f'data/avg_prices/{item_name}-{time.time()}-{qualities}.json', 'w+') as file:
        json.dump(data, file)

    items = {}
    for item in data:
        timestamps = []
        avg_prices = []
        location = item['location']

        if filter != '' and filter not in location:
            continue

        for record in item['data']:
            timestamps.append(datetime.strptime(record['timestamp'], "%Y-%m-%dT%H:%M:%S"))
            avg_prices.append(record['avg_price'])

        items[location] = pd.DataFrame({
            'Timestamp': timestamps,
            'Avg Price': avg_prices
        })
    return items


def generate_plt(current_item_name, qualities):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # ax1
    current_prices = get_current_prices(current_item_name, qualities)

    columns = ['Location', 'Quality', 'Sell Price Min', 'Sell Price Max', 'Buy Price Min', 'Buy Price Max']
    cell_text = []
    cell_colors = []

    price_min = min(
        [min(values) for values in zip(*[values for key, values in current_prices.items() if key != 'Quality'])])
    price_max = max(
        [max(values) for values in zip(*[values for key, values in current_prices.items() if key != 'Quality'])])

    for location, values in current_prices.items():
        location_color = get_location_color(location)
        mr_value = [location, values[0]]
        color_row = []

        for value in values[1:]:
            mr_value.append(value)
            normalized_price = (value - price_min) / (price_max - price_min)
            color = cm.RdYlGn(normalized_price)
            color_row.append(location_color)  # Add the first color value from location_color list
            color_row.append(color)  # Add the color calculated based on normalized price

        # Append additional colors or empty strings to ensure that color_row has 5 elements
        while len(color_row) < 5:
            color_row.append('')

        cell_text.append(mr_value)
        cell_colors.append(color_row)

    cell_colors = [['white' if color == '' else color for color in row] for row in cell_colors]

    data_df = pd.DataFrame(cell_text, columns=columns)
    mask = data_df['Location'] != 'Quality'
    data_df.loc[mask, 'Sell Price Min'] = data_df.loc[mask, 'Sell Price Min'].astype(float)
    data_df.loc[mask, 'Sell Price Max'] = data_df.loc[mask, 'Sell Price Max'].astype(float)
    data_df.loc[mask, 'Buy Price Min'] = data_df.loc[mask, 'Buy Price Min'].astype(float)
    data_df.loc[mask, 'Buy Price Max'] = data_df.loc[mask, 'Buy Price Max'].astype(float)
    data_df = data_df.set_index('Location')

    ax1.axis('off')
    ax1.table(cellText=data_df.values, cellColours=cell_colors, colLabels=data_df.columns, loc='center')

    # ax2
    avg_prices = get_avg_prices(current_item_name, qualities)
    for item in avg_prices:
        if item in current_prices:
            for value in current_prices[item]:
                ax2.plot(datetime.now(), value, 'o', color=get_location_color(item))

        ax2.plot(avg_prices[item]['Timestamp'], avg_prices[item]['Avg Price'],
                 get_location_marker(item), color=get_location_color(item))

    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=get_location_color(location),
                                 label=location)
                      for location in
                      current_prices.keys()]

    ax2.legend(handles=legend_handles)

    # global
    ax2.set_xlabel('Timestamp')
    ax2.set_ylabel('Average Price')
    ax2.set_title(f'Price {current_item_name} for every hour')
    plt.xticks(rotation=45)
    ax2.grid(True)

    plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    while True:
        print('\n<-----| New item |----->')
        item = input('Item: ')
        if not item:
            item = 'T4_BAG'

        qualities = input('Qualities: ')
        if not qualities:
            qualities = 0

        generate_plt(item, qualities)
