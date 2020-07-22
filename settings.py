# -*- encoding: UTF-8 -*-


def init():
    global DB_DIR, DATA_DIR, NOTIFY, CONFIG, STOCKS_FILE, \
        STOCKS_DATE, START_DATE, END_DATE, INDEX_FIELDS, STOCK_FIELDS, \
        STOCK_NAME, OUTPUT
    DATA_DIR = 'data'
    DB_DIR = 'storage'
    NOTIFY = True
    OUTPUT = './out'
    STOCKS_FILE = './storage/stocks.csv'
    STOCKS_DATE = './storage/trade_dates.csv'
    STOCK_NAME = './storage/stock_names.csv'
    START_DATE = '2001-01-01'
    END_DATE = '2020-12-30'
    STOCK_FIELDS = 'date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,pbMRQ,peTTM,psTTM,pcfNcfTTM,isST'
    INDEX_FIELDS = 'date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST'
    # CONFIG = 'config/主板200亿-创业板100亿.xlsx'
    # CONFIG = 'config/沪深A股.xlsx'
