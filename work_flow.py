# -*- encoding: UTF-8 -*-

import data_fetcher
import utils
import strategy.enter as enter
from strategy import turtle_trade, pe
from strategy import backtrace_ma250
from strategy import breakthrough_platform
from strategy import parking_apron
from strategy import low_atr
from strategy import keep_increasing
import baostock as bs
import notice
import logging
import db
import time
import datetime
import urllib
import settings
import pandas as pd


def process(update=False):
    logging.info("************************ process start ***************************************")
    if update:
        try:
            # 登陆系统 ####
            lg = bs.login()
            # 显示登陆返回信息
            print('login respond error_code:' + lg.error_code + ', error_msg:' + lg.error_msg)

            dt = utils.get_recently_trade_date()
            stock_rs = bs.query_all_stock(day=dt)

            # print(stock_rs.data)
            stock_df = stock_rs.get_data()
            data_df = pd.DataFrame()
            for code, status, name in zip(stock_df["code"], stock_df["tradeStatus"], stock_df["code_name"]):
                if "ST" in name:
                    continue
                print("Downloading :" + code + " , name :" + name + " , status :" + status)
                k_rs = bs.query_history_k_data_plus(code, settings.STOCK_FIELDS, start_date=dt, end_date=dt)
                data_df = data_df.append(k_rs.get_data())
                # print(result)
            bs.logout()
            data_df.to_csv(settings.STOCKS_FILE, encoding="utf-8", index=False, header=True)

        except urllib.error.URLError as e:
            print("Update Data Error ")

    stock_trades = pd.read_csv(settings.STOCKS_FILE)
    stock_names = pd.read_csv(settings.STOCK_NAME)
    stock_pd = pd.merge(stock_trades, stock_names, how='left', on=['code', 'code'])
    stock_pd['code'] = stock_pd['code'].astype(str)
    # print(stock_pd.values)
    stocks = [tuple((x[1], x[-1])) for x in stock_pd.values]
    # print(stocks[0])
    #if utils.need_update_data():
    #    utils.prepare()
    #    data_fetcher.run(stocks)
    #     data_fetcher.run(stocks)
    #    check_exit()

    strategies = {
        '海龟交易法则': turtle_trade.check_enter,
        '放量上涨': enter.check_volume,
        '突破平台': breakthrough_platform.check,
        '均线多头': keep_increasing.check,
        '停机坪': parking_apron.check,
        '回踩年线': backtrace_ma250.check,
        # 'pe': pe.check,
    }

    if datetime.datetime.now().weekday() == 0:
        strategies['均线多头'] = keep_increasing.check

    for strategy, strategy_func in strategies.items():
        check(stocks, strategy, strategy_func)
        time.sleep(2)

    logging.info("************************ process   end ***************************************")


def check(stocks, strategy, strategy_func):
    end = None
    m_filter = check_enter(end_date=end, strategy_fun=strategy_func)
    results = list(filter(m_filter, stocks))
    utils.persist(strategy, results)
    logging.info('**************"{0}"**************\n{1}\n**************"{0}"**************\n'.format(strategy, results))
    notice.strategy('**************"{0}"**************\n{1}\n**************"{0}"**************\n'.format(strategy, results))


def check_enter(end_date=None, strategy_fun=enter.check_volume):
    def end_date_filter(code_name):
        data = utils.read_data(code_name)
        if data is None:
            return False
        else:
            return strategy_fun(code_name, data, end_date=end_date)
        # if result:
        #     message = turtle_trade.calculate(code_name, data)
        #     logging.info("{0} {1}".format(code_name, message))
        #     notice.push("{0} {1}".format(code_name, message))

    return end_date_filter


# 统计数据
def statistics(all_data, stocks):
    limitup = len(all_data.loc[(all_data['changepercent'] >= 9.5)])
    limitdown = len(all_data.loc[(all_data['changepercent'] <= -9.5)])

    up5 = len(all_data.loc[(all_data['changepercent'] >= 5)])
    down5 = len(all_data.loc[(all_data['changepercent'] <= -5)])

    def ma250(stock):
        stock_data = utils.read_data(stock)
        return enter.check_ma(stock, stock_data)

    ma250_count = len(list(filter(ma250, stocks)))

    msg = "涨停数：{}   跌停数：{}\n涨幅大于5%数：{}  跌幅大于5%数：{}\n年线以上个股数量：    {}"\
        .format(limitup, limitdown, up5, down5, ma250_count)
    logging.info(msg)
    notice.statistics(msg)


def check_exit():
    t_shelve = db.ShelvePersistence()
    file = t_shelve.open()
    for key in file:
        code_name = file[key]['code_name']
        data = utils.read_data(code_name)
        if turtle_trade.check_exit(code_name, data):
            notice.strategy("{0} 达到退出条件".format(code_name))
            logging.info("{0} 达到退出条件".format(code_name))
            del file[key]
        elif turtle_trade.check_stop(code_name, data, file[key]):
            notice.strategy("{0} 达到止损条件".format(code_name))
            logging.info("{0} 达到止损条件".format(code_name))
            del file[key]

    file.close()

