import yfinance as yf
from globals import *

def data_to_csv(result):
    result.to_csv(CWD + '\Company Data\\tesla.csv')


if __name__ == "__main__":
    tesla = yf.Ticker('CLF')
    data_to_csv(tesla.history(period="max",back_adjust = True))




