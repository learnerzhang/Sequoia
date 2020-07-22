# -*- coding: UTF-8 -*-
import datetime
from pandas.tseries.offsets import *
import baostock as bs
import xlrd
import pandas as pd
import os
import settings

ONE_HOUR_SECONDS = 60 * 60


# 获取股票代码列表
def get_stocks(config=None):
	if config:
		data = xlrd.open_workbook(config)
		table = data.sheets()[0]
		rows_count = table.nrows
		codes = table.col_values(0)[1:rows_count - 1]
		names = table.col_values(1)[1:rows_count - 1]
		return list(zip(codes, names))
	else:
		data_files = os.listdir(settings.DATA_DIR)
		stocks = []
		for file in data_files:
			code_name = file.split(".")[0]
			code = code_name.split("-")[0]
			name = code_name.split("-")[1]
			appender = (code, name)
			stocks.append(appender)
		return stocks


def clean_files():
	for the_file in os.listdir(settings.DATA_DIR):
		file_path = os.path.join(settings.DATA_DIR, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)


# 读取本地数据文件
def read_data(code_name):
	stock = code_name[0]
	name = code_name[1]
	file_name = stock + '_' + name + '.csv'
	# print(file_name)
	if os.path.exists(settings.DATA_DIR + "/" + file_name):
		return pd.read_csv(settings.DATA_DIR + "/" + file_name)
	else:
		return None


# 是否需要更新数据
def need_update_data():
	try:
		code_name = ('sz.000001', '平安银行')
		data = read_data(code_name)
		if data is None:
			return True
		else:
			start_time = next_weekday(data.iloc[-1].date)
			current_time = datetime.datetime.now()
			if start_time > current_time:
				return False
			return True
	except IOError:
		return True


# 是否是工作日
def is_weekday():
	return datetime.datetime.today().weekday() < 5


def next_weekday(date):
	return pd.to_datetime(date) + BDay()


def persist(strategy, results):
	with open(settings.OUTPUT + "/" + strategy + ".txt", 'w') as wf:
		for e in results:
			wf.write(e[0] + "-" + e[1] + '\n')


def prepare():
	dirs = [settings.DATA_DIR, settings.DB_DIR]
	for dir in dirs:
		if os.path.exists(dir):
			clean_files()
			return
		else:
			os.makedirs(dir)


def init_trade_date():
	settings.init()

	# 登陆系统 ####
	lg = bs.login()
	# 显示登陆返回信息
	print('login respond error_code:' + lg.error_code)
	print('login respond  error_msg:' + lg.error_msg)

	# 获取交易日信息 ####
	rs = bs.query_trade_dates(start_date=settings.START_DATE, end_date=settings.END_DATE)
	print('query_trade_dates respond error_code:' + rs.error_code)
	print('query_trade_dates respond  error_msg:' + rs.error_msg)

	# 打印结果集 ####
	data_list = []
	while (rs.error_code == '0') & rs.next():
		# 获取一条记录，将记录合并在一起
		data_list.append(rs.get_row_data())
	result = pd.DataFrame(data_list, columns=rs.fields)

	# 结果集输出到csv文件 ####
	result.to_csv(settings.STOCKS_DATE, encoding="utf-8", index=False, header=True)
	# print(result)
	# 登出系统 ####
	bs.logout()


def get_recently_trade_date():
	settings.init()
	dt = datetime.date.today()
	if os.path.exists(settings.STOCKS_DATE):
		trade_dates = pd.read_csv(settings.STOCKS_DATE, header=0)
		trade_date_dict = trade_dates.set_index("calendar_date")['is_trading_day'].to_dict()
		tmp_dt = str(dt)
		if tmp_dt in trade_date_dict:
			if trade_date_dict[tmp_dt] == 1:
				return tmp_dt
			else:
				dt_num = 1
				dt_pass = str(dt - datetime.timedelta(days=dt_num))
				while dt_pass in trade_date_dict and trade_date_dict[dt_pass] == 0:
					dt_num += 1
					dt_pass = str(dt - datetime.timedelta(days=dt_num))
				if dt_pass in trade_date_dict:
					return dt_pass
			print("Date Is Not Exist !!!, Reload Trade Dates. ")
	else:
		print("Date Is Not Exist, Reloading Trade Dates. ")
		init_trade_date()
		print("Date Loading Finish. ")
	return None


if __name__ == '__main__':
	# init_trade_date()
	dt = get_recently_trade_date()
	print(dt)
