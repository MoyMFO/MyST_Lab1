
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: MoyMFO                                                                                      -- #
# -- license: Public                                                                                     -- #
# -- repository: https://github.com/MoyMFO/MyST_Lab1                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
from functions import PublicTradesMeasures, OrderBookMeasures
from data import DataPreparation


# Instances: Data preparation
public_trades_data = DataPreparation('btcusdt_binance.csv')
public_trades_data = public_trades_data.public_trades_csv_transformation()

order_books_data = DataPreparation('orderbooks_05jul21.json')
order_books_data = order_books_data.order_books_json_transformation()

# Instances: Measures
public_trades_measures = PublicTradesMeasures(public_trades_data)
order_books_measures = OrderBookMeasures(order_books_data)


#print(public_trades_measures.trade_flow_imbalance(by='H'))
#print(public_trades_measures.ohclvv(by='H'))
print(order_books_measures.spread())

