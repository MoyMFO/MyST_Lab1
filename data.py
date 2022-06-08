
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: MoyMFO                                                                                      -- #
# -- license: Public                                                                                     -- #
# -- repository: https://github.com/MoyMFO/myst_mfo_lab1                                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import json

class DataPreparation:
    """
    This class contains methods to prepare orderbook data coming from JSON file 
    and public trades data comming from CSV file.

    Parameters
    ------------
    No required at initialization

    Attributes
    ------------
    None
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def public_trades_csv_transformation(filepath) -> pd.DataFrame:
        """
        This method prepare public trades data from a CSV file.

        Parameters 
        ----------
        Required on calling:
             filepath: CSV file path (default: None)
                Public trades data, it should be a CSV following next structures:
                'datetime': datetime to be typed as timestamp.
                'price': price
                'amount': traded volume
                'side': sell or buy
        Returns
        ------
        public trades data: DataFrame
        """
        pt_data = pd.read_csv(filepath, header=0)
        pt_data.index = pd.to_datetime(pt_data['timestamp'])
        return pt_data

    @staticmethod
    def order_books_json_transformation(filepath) -> dict:
        """
        This method prepare public trades data from a CSV file.

        Parameters 
        ----------
        Required on calling:
             data_ob: JSON file path (default: None)
                Orderbook data, it should be a JSON following next structures:
                'datetime': datetime to be typed as timestamp.
                'bid_size': bid levels volumes
                'ask_size': ask levels volumes
                'bid': bid levels prices
                'ask': ask levels prices
        Returns
        ------
        orderbooks data: dict
        """
        f = open(filepath)
        orderbooks_data = json.load(f)
        ob_data = orderbooks_data['bitfinex']
        #Drop None Keys
        ob_data = {i_key: i_value for i_key, i_value in ob_data.items() if i_value is not None}
        #Convert to DataFrame and rearange columns
        ob_data = {i_ob: pd.DataFrame(ob_data[i_ob])[['bid_size','bid','ask','ask_size']]
                if  ob_data[i_ob] is not None else None for i_ob in list(ob_data.keys())}
        return ob_data
