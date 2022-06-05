
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import numpy as np
import pandas as pd


class OrderBookMeasures:

    """
    Parameteters
    ------------
    data_ob: dict (default: None)
        Datos de entrada del libro de ordenes, es un diccionario con la siguiente estructura:
        'timestamp': objeto tipo timestamp reconocible por maquina, e.g. pd.to_datetime()
        'bid_size': volume de niveles bid
        'bid': precio de niveles bid
        'ask': precio de niveles ask
    """

    def __init__(self, data_ob: dict) -> dict:
        self.data_ob = data_ob

    # Hidden Attributes
    @property
    def __ob_ts(self) -> list:
        return list(self.data_ob.keys())

    @property
    def __l_ts(self) -> list:
        return [pd.to_datetime(i_ts) for i_ts in self.__ob_ts]

    # -- Median Time of OrderBook update -- #
    def meadian_time_ob(self) -> float:
        ob_m1 = np.median([self.__l_ts[n_ts + 1] - self.__l_ts[n_ts] for n_ts in range(0, len(self.__l_ts)-1)]).total_seconds() * 1000
        return ob_m1

    # -- Spread -- #
    def spread(self) -> list:
        ob_m2 = [self.data_ob[self.__ob_ts[0]]['ask'][0] 
                 - self.data_ob[self.__ob_ts[0]]['bid'][0] 
                for i in range(0, len(self.__ob_ts))]
        return ob_m2

    # -- Midprice -- #
    def mid_price(self) -> list:
        ob_m3 = [(self.data_ob[self.__ob_ts[0]]['ask'][0] 
                + self.data_ob[self.__ob_ts[0]]['bid'][0])*0.5 
                for i in range(0, len(self.__ob_ts))]
        return ob_m3

    # -- No. Price Levels -- #
    def price_levels(self) -> list:
        ob_m4 = [self.data_ob[i_ts].shape[0] for i_ts in self.__ob_ts]
        return ob_m4

     # -- Bid_Volume -- #
    def bid_volume(self) -> list:
        ob_m5 = [np.round(self.data_ob[i_ts]['bid_size'].sum(), 6) 
                 for i_ts in self.__ob_ts]
        return ob_m5

     # -- Ask_Volume -- #
    def ask_volume(self) -> list:
        ob_m6 = [np.round(self.data_ob[i_ts]['ask_size'].sum(), 6) 
                for i_ts in self.__ob_ts]
        return ob_m6

     # -- Total_Volume -- #
    def total_volume(self) -> list:
        ob_m7 = [np.round(self.data_ob[i_ts]['bid_size'].sum() 
                 + self.data_ob[i_ts]['ask_size'].sum(), 6) for i_ts in self.__ob_ts]
        return ob_m7

    # -- OrderBook Imbalance (v: volume, d: depth) -- #
    def ob_imbalance(self) -> list:
        # v[0] Bid volume, v[1] Ask volume 
        def __obimb(v, d): return np.sum(v.iloc[:d,0])/np.sum([v.iloc[:d,0], v.iloc[:d,1]])
        ob_m8 = [__obimb(self.data_ob[i_ts][['bid_size','ask_size']],
                 len(self.data_ob[i_ts])) for i_ts in self.__ob_ts]
        return ob_m8

    # -- wighted-Midprice (p: price, v: volume) -- #
    def w_midprice(self) -> list:
        # w_midprice = lambda p, v: (v.iloc[:,1]/np.sum([v.iloc[:,0], v.iloc[:,1]]))*p.iloc[:,0] + (v.iloc[:,0]/np.sum([v.iloc[:,0], v.iloc[:,1]]))*p.iloc[:,1]
        # ob_m9  = [w_midprice(data_ob[i_ts][['bid','ask']], data_ob[i_ts][['bid_size', 'ask_size']]) for i_ts in ob_ts]
        ob_m8 = self.ob_imbalance()
        ob_m3 = self.mid_price()
        ob_m9 = [ob_m8[i_ts] * ob_m3[i_ts] for i_ts in range(0, len(self.__ob_ts))]
        return ob_m9

    # -- VWAP (Volume-Weighted Average Price) (p: price, v: volume, d:depth) -- #
    def vwap(self) -> list:
        # p[0]:Bid price, p[1]:Ask price, v[0]: Bid volume, v[1]: Ask volume
        def __vwap_calculation(p, v, d): return np.sum(p.iloc[:d, 0] * v.iloc[:d,0] + p.iloc[:d,1] * v.iloc[:d,1]) / np.sum(v.iloc[:d,0] + v.iloc[:d,1])
        ob_m10 = [__vwap_calculation(self.data_ob[i_ts][['bid', 'ask']], self.data_ob[i_ts][['bid_size', 'ask_size']], 
                 len(self.data_ob[i_ts])) for i_ts in self.__ob_ts]
        return ob_m10


class PublicTradesMeasures:

    def __init__(self, pt_data: pd.DataFrame) -> pd.DataFrame:
        self.pt_data = pt_data

    def transaction_volume(self, by: str) -> pd.Series:
        n_pt_data = self.pt_data['side'].resample(by).count()
        return n_pt_data
    
    def asset_volume(self, by: str) -> pd.Series:
        v_pt_data = self.pt_data['amount'].resample(by).sum()
        return v_pt_data

    def high_price(self, by: str) -> pd.Series:
        h_pt_data = self.pt_data['price'].resample(by).max()
        return h_pt_data
    
    def low_price(self, by: str) -> pd.Series:
        l_pt_data = self.pt_data['price'].resample(by).min()
        return l_pt_data

    def open_price(self, by: str) -> pd.Series:
        o_pt_data = self.pt_data['price'].resample(by).first()
        return o_pt_data

    def close_price(self, by: str) -> pd.Series:
        c_pt_data = self.pt_data['price'].resample(by).last()
        return c_pt_data
    
    def ohclvv(self, by: str) -> pd.DataFrame:
        ohclvv = pd.DataFrame({'Open price': self.open_price(by), 'High price': self.high_price(by), 
                       'Low price': self.low_price(by),'Close price': self.close_price(by),
                       'Asset Volume': self.asset_volume(by), 'Transaction Volume': self.transaction_volume(by)})
        return ohclvv

    def trade_flow_imbalance(self, by: str) -> pd.DataFrame:
        trade_flow_imbalance = pd.DataFrame(self.pt_data[self.pt_data['side'] == "buy"]['amount'].resample(by).sum() 
                               - self.pt_data[self.pt_data['side'] == "sell"]['amount'].resample(by).sum())
        return trade_flow_imbalance
