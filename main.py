from core.parsers.prices import get_current_prices
from core.ui.render import plot_prices

if __name__ == '__main__':
    while True:
        print('\n<-----| New item |----->')
        item = input('Item: ')
        if not item:
            item = 'BAG'

        qualities = input('Qualities: ')
        if not qualities:
            qualities = 0

        tier = input('Tier: ')
        if not qualities:
            tier = '4'

        plot_prices(get_current_prices(item, tier,  qualities))
