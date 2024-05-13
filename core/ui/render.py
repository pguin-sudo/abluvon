import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from matplotlib.table import Table

from core.data.dataclasses import Price, Item, City


def get_location_marker(item: City) -> str:
    if City.is_portal:
        return '--'
    return '-'


def plot_prices(prices):
