## Description
*This project has been created for calculating measures of orderbooks and public trades. It is used python as the 
programming language to implement theoretical measures that describe the market dynamic. Will be found some methods contained
in classes for the orderbook and/or public trade to be analyzed. Finally, there is a Jupyter notebook where all the measures
are implemented and a few graphics are displayed.*

## Install dependencies

Install all the dependencies stated in the requirements.txt file, just run the following command in terminal:

        pip install -r requirements.txt
        
Or you can manually install one by one using the name and version in the file.

## Funcionalities

This project is about the calculation of plenty orderbook and public trades measures.

### For orderbooks measures: 

When a JSON files with orderbooks is provided we can get measures:

### Instances: Data preparation
data = DataPreparation()
order_books_data = data.order_books_json_transformation('orderbooks_05jul21.json')
### Instances: Measures
order_books_measures = OrderBookMeasures(order_books_data)
### Call measures
order_books_measures.ohclvv('20T')

### For public trades measures: 

When a CSV file with public trades is provided we can get measures:

### Instances: Data preparation
data = DataPreparation()
public_trades_data = data.public_trades_csv_transformation('btcusdt_binance.csv')
### Instances: Measures
public_trades_measures = PublicTradesMeasures(public_trades_data)
### Call measures
public_trades_measures.sell_trade_count(by='H')

### IMPORTANT:
main.py only shows some measures as a testing/proof of working. Find all measures in the Jupyter notebook.

## Author
Moises Flores Ortiz. Student of financial engineering about to graduate.

## License
**GNU General Public License v3.0** 

*Permissions of this strong copyleft license are conditioned on making available 
complete source code of licensed works and modifications, which include larger 
works using a licensed work, under the same license. Copyright and license notices 
must be preserved. Contributors provide an express grant of patent rights.*

## Contact
*For more information in reggards of this repo, please contact if722183@iteso.mx*
