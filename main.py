"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: This project has been created for calculating measures of orderbooks and public trades. 
#             It is used python as the programming language to implement theoretical measures that describe
#             the market dynamic. Will be found some methods contained in classes for the orderbook and/or 
#             public trade to be analyzed. Finally, there is a Jupyter notebook where all the measures
              are implemented and a few graphics are displayed.                                          -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: MoyMFO                                                                                      -- #
# -- license: GNU General Public License v3.0                                                            -- #
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
