
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: MoyMFO                                                                                      -- #
# -- license: Public                                                                                     -- #
# -- repository: https://github.com/MoyMFO/myst_mfo_lab1                                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import numpy as np
import pandas as pd


class OrderBookMeasures:
    """
    This class contains methods of orderbooks measures. Initialized as required to 
    consult the calculation of different measures.

    Parameteters
    ------------
    data_ob: dict (default: None)
        Orderbook data, it should be a dictionary following next structures:
        'timestamp': timestamp object, e.g. pd.to_datetime()
        'bid_size': bid levels volumes
        'ask_size': ask levels volumes
        'bid': bid levels prices
        'ask': ask levels prices

    Attributes
    ------------
    Both are hidden attributes since data shouldn't be modified.

    __ob_ts: list of orderbooks keys.
    __l_ts: list of timestamps of orderbooks.
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
        """
        This method caculates the median time of orderbook update.

        Parameters
        ----------
        Initialized on instance:
            __l_ts: list of timestamps of orderbooks.

        Returns
        ------
        Medain time orderbook: float
        """
        ob_m1 = np.median([self.__l_ts[n_ts + 1] - self.__l_ts[n_ts] for n_ts in range(0, len(self.__l_ts)-1)]).total_seconds() * 1000
        return ob_m1

    # -- Spread -- #
    def spread(self) -> list:
        """
        This method caculates the spread of top of the book.

        Parameters
        ----------
        Initialized on instance:
            data_ob: orderbook data.
            __ob_ts: list of timestamps of orderbooks.

        Returns
        ------
        Spread: list
        """
        ob_m2 = [self.data_ob[self.__ob_ts[0]]['ask'][0] 
                 - self.data_ob[self.__ob_ts[0]]['bid'][0] 
                for i in range(0, len(self.__ob_ts))]
        return ob_m2

    # -- Midprice -- #
    def mid_price(self) -> pd.DataFrame:
        """
        This method caculates the mid price of top of the orderbook.

        Parameters
        ----------
        Initialized on instance:
            data_ob: orderbook data.
            __ob_ts: list of timestamps of orderbooks.

        Returns
        ------
        Mid price: DataFrame
        """
        ob_m3 = [(self.data_ob[self.__ob_ts[i_ts]]['ask'][0] 
                + self.data_ob[self.__ob_ts[i_ts]]['bid'][0])*0.5 
                for i_ts in range(0, len(self.__ob_ts))]
        return ob_m3

    # -- No. Price Levels -- #
    def price_levels(self) -> list:
        """
        This method caculates the price leves of the orderbook.

        Parameters
        ----------
        Initialized on instance:
            data_ob: orderbook data.
            __ob_ts: list of timestamps of orderbooks.

        Returns
        Price leves: list
        """
        ob_m4 = [self.data_ob[i_ts].shape[0] for i_ts in self.__ob_ts]
        return ob_m4

     # -- Bid_Volume -- #
    def bid_volume(self) -> list:
        """
        This method caculates the bid volume of the orderbook.

        Parameters
        ----------
        Initialized on instance:
            data_ob: orderbook data.
            __ob_ts: list of timestamps of orderbooks.

        Returns
        ------
        Bid volume: list
        """
        ob_m5 = [np.round(self.data_ob[i_ts]['bid_size'].sum(), 6) 
                 for i_ts in self.__ob_ts]
        return ob_m5

     # -- Ask_Volume -- #
    def ask_volume(self) -> list:
        """
        This method caculates the ask volume of the orderbook.

        Parameters
        ----------
        Initialized on instance:
            data_ob: orderbook data.
            __ob_ts: list of timestamps of orderbooks.

        Returns
        ------
        Ask volume: list
        """
        ob_m6 = [np.round(self.data_ob[i_ts]['ask_size'].sum(), 6) 
                for i_ts in self.__ob_ts]
        return ob_m6

     # -- Total_Volume -- #
    def total_volume(self) -> list:
        """
        This method caculates the total volume of the orderbook.

        Parameters 
        ----------
        Initialized on instance:
            data_ob: orderbook data.
            __ob_ts: list of timestamps of orderbooks.

        Returns
        ------
        Total volume: list
        """
        ob_m7 = [np.round(self.data_ob[i_ts]['bid_size'].sum() 
                 + self.data_ob[i_ts]['ask_size'].sum(), 6) for i_ts in self.__ob_ts]
        return ob_m7

    # -- OrderBook Imbalance (v: volume, d: depth) -- #
    def ob_imbalance(self, depth: str or int='full') -> pd.DataFrame:
        """
        This method caculates the Orderbook imbalance.

        Parameters 
        ----------
        Initialized on instance:
            data_ob: orderbook data.
            __ob_ts: list of timestamps of orderbooks.

        Required on calling:
            Depth: str or int. 'full' for the complete orderbook depth or int opcional depth.
        Returns
        ------
        Ob imbalance: DataFrame
        """
        def __obimb(v, d): return np.sum(v.iloc[:d,0])/np.sum([v.iloc[:d,0], v.iloc[:d,1]]) 
        if depth == 'full':
            ob_m8 = [__obimb(self.data_ob[i_ts][['bid_size','ask_size']],
                    len(self.data_ob[i_ts])) for i_ts in self.__ob_ts]
        else:
            ob_m8 = [__obimb(self.data_ob[i_ts][['bid_size','ask_size']], 
            depth) for i_ts in self.__ob_ts]
        return pd.DataFrame(ob_m8)

    # -- wighted-Midprice (p: price, v: volume) -- #
    def w_midprice(self) -> list:
        """
        This method caculates the weighted midprice of the orderbook.

        Parameters 
        ----------
        Initialized on instance:
            data_ob: orderbook data.

        Returns
        ------
        Weighted Midprice: list
        """
        def __w_midprice(p, v): return ((v.iloc[0,1]/np.sum([v.iloc[0,0], v.iloc[0,1]]))*p.iloc[0,0] 
                                       + (v.iloc[0,0]/np.sum([v.iloc[0,0], v.iloc[0,1]]))*p.iloc[0,1])
        ob_m9  = [__w_midprice(self.data_ob[i_ts][['bid','ask']], self.data_ob[i_ts][['bid_size', 'ask_size']]) for i_ts in self.__ob_ts]
        return ob_m9

    # -- VWAP (Volume-Weighted Average Price) (p: price, v: volume, d:depth) -- #
    def vwap(self, depth: str or int='full') -> list:
        """
        This method caculates the Volume-Weighted Average Price of the orderbook.

        Parameters 
        ----------
        Initialized on instance:
            data_ob: orderbook data.
            __ob_ts: list of timestamps of orderbooks.

        Required on calling:
            Depth: str or int. 'full' for the complete orderbook depth or int opcional depth.
        Returns
        ------
        VWAP: list
        """

        def __vwap_calculation(p, v, d): return (np.sum(p.iloc[:d, 0] * v.iloc[:d,0] + p.iloc[:d,1] * v.iloc[:d,1]) 
                                                / np.sum(v.iloc[:d,0] + v.iloc[:d,1]))
        if depth == 'full':
            ob_m10 = [__vwap_calculation(self.data_ob[i_ts][['bid', 'ask']], self.data_ob[i_ts][['bid_size', 'ask_size']], 
                 len(self.data_ob[i_ts])) for i_ts in self.__ob_ts]
        else:
            ob_m10 = [__vwap_calculation(self.data_ob[i_ts][['bid', 'ask']], self.data_ob[i_ts][['bid_size', 'ask_size']], 
                     depth) for i_ts in self.__ob_ts]
        return ob_m10

    def ohclvv(self, by: str) -> pd.DataFrame:
        """
        This method caculates the OHCLVV of the midpire orderbook.

        Parameters 
        ----------
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.
        Returns
        ------
        OHCLVV: DataFrame
        """
        df_mid_price = pd.DataFrame({'mid price':self.mid_price()}, index=self.__l_ts)
        ohclvv = pd.DataFrame({'Open price': df_mid_price['mid price'].resample(by, closed='left').first(), 
                               'High price': df_mid_price['mid price'].resample(by, closed='left').max(), 
                               'Low price': df_mid_price['mid price'].resample(by, closed='left').min(),
                               'Close price': df_mid_price['mid price'].resample(by, closed='left').last(),
                               'Asset Volume': df_mid_price['mid price'].resample(by, closed='left').sum(), 
                               'Transaction Volume': df_mid_price['mid price'].resample(by, closed='left').count()})
        return ohclvv

    def ob_imbalance_stats(self, statistic_measure: str, depth: str='full') -> float:
        """
        This method caculates oderderbook imbalance stats: Mean, Variance, Skew, and Kurtosis.

        Parameters 
        ----------
        Required on calling:
            static_measure: str. Mean, Variance, Skew, Kurtosis.
            Depth: str or int. 'full' for the complete orderbook depth or int opcional depth.
        Returns
        ------
        ob desired stat: float 
        """
        ob_imbalance = self.ob_imbalance(depth=depth)
        stats = {
            'Mean': ob_imbalance.mean()[0], 'Variance': ob_imbalance.var()[0],
            'Skew': ob_imbalance.skew()[0], 'Kurtosis': ob_imbalance.kurtosis()[0]
        }
        return stats[statistic_measure]


class PublicTradesMeasures:
    """
    This class contains methods of public trades measures. Initialized as required to 
    consult the calculation of different measures.

    Parameters
    ------------
    pt_data: pd.DataFrame (default: None)
        Public trades data, it should be a pandas DataFrame following next structures:
        'timestamp': timestamp object, e.g. pd.to_datetime()
        'price': price
        'amount': traded volume
        'side': sell or buy

    Attributes
    ------------
    This is data obtained at initialization

    pt_data: public trades data
    """

    def __init__(self, pt_data: pd.DataFrame) -> pd.DataFrame:
        self.pt_data = pt_data

    # -- Measures by transaction count -- #
    def buy_trade_count(self, by: str) -> pd.Series:
        """
        This method caculates the buy trade count of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: lpublic trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        buy trade count: Series
        """
        buy_trade_count = self.pt_data[self.pt_data['side'] == 'buy']['side'].resample(by, closed='left').count() 
        return buy_trade_count

    def sell_trade_count(self, by: str) -> pd.Series:
        """
        This method caculates the sell trade count of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        sell trade count: Series
        """
        sell_trade_count = self.pt_data[self.pt_data['side'] == 'sell']['side'].resample(by, closed='left').count()
        return sell_trade_count      

    def total_trade_count(self, by: str) -> pd.Series:
        """
        This method caculates the total trade count of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        total trade count: Series
        """
        n_pt_data = self.pt_data['side'].resample(by, closed='left').count()
        return n_pt_data

    def difference_trade_count(self, by: str) -> pd.DataFrame:
        """
        This method caculates the difference buy-sell trade count of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        difference buy-sell trade count: DataFrame
        """
        trade_flow_imbalance = pd.DataFrame(self.buy_trade_count(by) - self.sell_trade_count(by))
        return trade_flow_imbalance
    
    # -- Measures by asset volume & price -- #s
    def buy_volume(self, by: str) -> pd.Series:
        """
        This method caculates the buy asset volume of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        buy asset volume: Series
        """
        buy_volume = self.pt_data[self.pt_data['side'] == 'buy']['amount'].resample(by, closed='left').sum() 
        return buy_volume

    def sell_volume(self, by: str) -> pd.Series:
        """
        This method caculates the sell asset volume of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        sell asset volume: Series
        """
        sell_volume = self.pt_data[self.pt_data['side'] == 'sell']['amount'].resample(by, closed='left').sum() 
        return sell_volume    

    def total_volume(self, by: str) -> pd.Series:
        """
        This method caculates the total asset volume of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        total asset volume: Series
        """
        v_pt_data = self.pt_data['amount'].resample(by, closed='left').sum()
        return v_pt_data

    def high_price(self, by: str) -> pd.Series:
        """
        This method caculates the high price by resampling of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        high price: Series
        """
        h_pt_data = self.pt_data['price'].resample(by, closed='left').max()
        return h_pt_data
    
    def low_price(self, by: str) -> pd.Series:
        """
        This method caculates the low price by resampling of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        low price: Series
        """
        l_pt_data = self.pt_data['price'].resample(by, closed='left').min()
        return l_pt_data

    def open_price(self, by: str) -> pd.Series:
        """
        This method caculates the open price by resampling of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        open price: Series
        """
        o_pt_data = self.pt_data['price'].resample(by, closed='left').first()
        return o_pt_data

    def close_price(self, by: str) -> pd.Series:
        """
        This method caculates the close price by resampling of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        close price: Series
        """
        c_pt_data = self.pt_data['price'].resample(by, closed='left').last()
        return c_pt_data
    
    def trade_flow_imbalance(self, by: str) -> pd.DataFrame:
        """
        This method caculates the trade flow imbalance (difference buy-sell) by resampling of public trades.

        Parameters
        ----------
        Initialized on instance:
            pt_data: public trades data.
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.

        Returns
        ------
        trade flow imbalance: Series
        """
        trade_flow_imbalance = pd.DataFrame(self.buy_volume(by) - self.sell_volume(by))
        return trade_flow_imbalance
    
    def ohclvv(self, by: str) -> pd.DataFrame:
        """
        This method caculates the OHCLVV of the trade price.

        Parameters 
        ----------
        Required on calling:
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.
        Returns
        ------
        OHCLVV: DataFrame
        """
        ohclvv = pd.DataFrame({'Open price': self.open_price(by), 'High price': self.high_price(by), 
                               'Low price': self.low_price(by),'Close price': self.close_price(by),
                               'Asset Volume': self.total_volume(by), 'Transaction Volume': self.total_trade_count(by)})
        return ohclvv

    def public_trades_stats(self, statistic_measure: str, by: str) -> float:
        """
        This method caculates public trade price stats: Mean, Variance, Skew, and Kurtosis.

        Parameters 
        ----------
        Required on calling:
            static_measure: str. Mean, Variance, Skew, Kurtosis.
            by: str. Groupying time desired. e.g. 'H' or '60T' to resample by hour.
        Returns
        ------
        public trades desired stat: float 
        """
        trade_flow_imbalance = self.trade_flow_imbalance(by)
        stats = {
            'Mean': trade_flow_imbalance.mean()[0], 'Variance': trade_flow_imbalance.var()[0],
            'Skew': trade_flow_imbalance.skew()[0], 'Kurtosis': trade_flow_imbalance.kurtosis()[0]
        }
        return stats[statistic_measure]


class DataTransformationToPlot:

    @staticmethod
    def data_for_public_trades(data) -> pd.DataFrame:
        pt_data = data.groupby('price').resample('1T')['amount'].sum()
        return pt_data