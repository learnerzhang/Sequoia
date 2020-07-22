# -*- encoding: UTF-8 -*-
import baostock as bs
import pandas as pd
import datetime
import logging
import settings
import talib as tl

import utils

import concurrent.futures

from pandas.tseries.offsets import *


# def update_data(code_name):
#     stock = code_name[0]
#     old_data = utils.read_data(code_name)
#     if not old_data.empty:
#         start_time = utils.next_weekday(old_data.iloc[-1].date)
#         current_time = datetime.datetime.now()
#         if start_time > current_time:
#             return
#
#         df = ts.get_k_data(stock, autype='qfq')
#         mask = (df['date'] >= start_time.strftime('%Y-%m-%d'))
#         appender = df.loc[mask]
#         if appender.empty:
#             return
#         else:
#             return appender


def init_data(code_name):
    stock = code_name[0]
    name = code_name[1]
    file_name = stock + '_' + name + '.csv'
    # data = ts.pro_bar(ts_code=stock, adj='qfq', api=ts.pro_api(token=settings.TOKEN, timeout=30))
    # data = ts.get_k_data(stock, autype='qfq')
    # 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code + ' , error_msg:' + lg.error_msg)
    # 获取历史K线数据 ####

    # frequency="d"取日k线，adjustflag="3"默认不复权
    rs = bs.query_history_k_data_plus(stock, fields=settings.STOCK_FIELDS, start_date=settings.START_DATE, end_date=settings.END_DATE, frequency="d", adjustflag="3")
    print('query_history_k_data_plus respond error_code:' + rs.error_code + ' , error_msg:' + rs.error_msg +
          ' , code:' + stock + "/" + name)

    # 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    if data_list:
        result = pd.DataFrame(data_list, columns=rs.fields)
        result['p_change'] = tl.ROC(result['close'], 1)
        result.to_csv(settings.DATA_DIR + "/" + file_name, encoding="utf-8", index=False, header=True)
        # print(result.head(3))
    else:
        logging.debug("股票：" + stock + " 没有数据，略过...")

    # 登出系统 ####
    bs.logout()


def run(stocks):
    append_mode = False
    update_fun = init_data

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_stock = {executor.submit(update_fun, stock): stock for stock in stocks}
        for future in concurrent.futures.as_completed(future_to_stock):
            future_to_stock[future]
