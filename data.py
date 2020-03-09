import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import os


# Function to import the data-set of the stock
def import_df(stock_name):
    start = dt.datetime(1990, 1, 1)
    end = dt.datetime.today() - dt.timedelta(days=1)
    df = web.DataReader(stock_name, 'yahoo', start, end)
    new_name = stock_name.lower() + '.csv'
    df.to_csv(new_name)
    df = pd.read_csv(new_name, parse_dates=True, index_col=0)
    if os.path.exists(new_name):
        os.remove(new_name)
        print('File ', stock_name, ' removed successfully')
    else:
        print("The file does not exist")
    return df