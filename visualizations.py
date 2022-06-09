
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

import plotly.graph_objects as go
import pandas as pd
import json
import numpy as np
from plotly.subplots import make_subplots


class OrderbooksAndPublicTradePlots:

    def __init__(self) -> None:
        pass

    
    @staticmethod
    def plot_orderbook() -> go.Figure:
        f = open('files/orderbooks_05jul21.json')
        orderbooks_data = json.load(f)
        data = pd.DataFrame(orderbooks_data['bitfinex'][list(orderbooks_data['bitfinex'].keys())[0]])
        ob_graph = go.Figure(data=[
        go.Bar(name='Ask', x=data['ask'], y=data['ask_size'], marker={'color': 'red'}),
        go.Bar(name='Bid', x=data['bid'], y=data['bid_size'], marker={'color': 'blue'})])
        ob_graph.update_layout(barmode='group')
        
        return ob_graph

    @staticmethod
    def plt_publictrades() -> go.Figure:
        
        pt_data = pd.read_csv('files/btcusdt_binance.csv', header=0)
        pt_data.index = pd.to_datetime(pt_data['timestamp'])
        data_x = np.arange(len(list(pt_data['timestamp'])))[0:59]
        data_y = list(pt_data['price'])[0:59]
        data_y1 = list(pt_data['amount'])[0:59]
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Add traces
        fig.add_trace(
            go.Scatter(x=data_x, y=data_y, name="traded price"),
            secondary_y=False,)

    

        fig.add_trace(
            go.Bar(x=data_x, y=data_y1, name="volume"),
            secondary_y=True,
        )

    

        # Add figure title
        fig.update_layout(
            title_text="Trades publicos"
        )

    

        # Set x-axis title
        fig.update_xaxes(title_text="Timestamp")

    

        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Traded Price</b> <br> BTC/USDT", secondary_y=False)
        fig.update_yaxes(title_text="<b>Volume</b> <br> BTC", secondary_y=True)

    

    #  fig.update_layout(legend_orientation='h', xaxis=dict(ticktext=list(pt_data['timestamp'])[0:499]) )
        return fig.show()