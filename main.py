
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: MoyMFO                                                                                      -- #
# -- license: Public                                                                                     -- #
# -- repository: https://github.com/MoyMFO/myst_mfo_lab1                                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
from functions import PublicTradesMeasures, OrderBookMeasures, DataTransformationToPlot
from data import DataPreparation


# Instances: Data preparation (repo rename: commit test)
data = DataPreparation()

public_trades_data = data.public_trades_csv_transformation('btcusdt_binance.csv')

order_books_data = data.order_books_json_transformation('orderbooks_05jul21.json')

# Instances: Measures
public_trades_measures = PublicTradesMeasures(public_trades_data)
order_books_measures = OrderBookMeasures(order_books_data)
data_to_plot = DataTransformationToPlot()
#print(order_books_data)

#print(public_trades_measures.public_trades_stats(statistic_measure = 'Kurtosis', by='H'))
#print(public_trades_measures.sell_trade_count(by='H'))
#print(public_trades_measures.total_trade_count(by='H'))
#print(order_books_measures.ob_imbalance_stats(statistic_measure='Mean', depth='full'))
#print(order_books_measures.ohclvv('20T'))
#print(public_trades_measures.difference_trade_count(by='H'))
print(data_to_plot.data_for_public_trades(public_trades_data))
