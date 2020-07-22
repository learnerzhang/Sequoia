# -*- encoding: UTF-8 -*-
import unittest
import baostock as bs
import talib
from talib import ATR
import pandas as pd
import settings
import utils
import notice
import strategy.enter as enter
import strategy.low_atr as low_atr
import strategy.enter as enter
import strategy.backtrace_ma250 as backtrace_ma250
import strategy.parking_apron as parking_apron
import strategy.breakthrough_platform as breakthrough_platform
import logging


class TestShare(unittest.TestCase):

	def setUp(self) -> None:
		settings.init()

	def test_pro_api(self):
		lg = bs.login()
		# 显示登陆返回信息
		print('login respond error_code:' + lg.error_code + ', error_msg:' + lg.error_msg)
		dt = utils.get_recently_trade_date()
		rs = bs.query_all_stock(day=dt)
		# 打印结果集 ####
		data_list = []
		while (rs.error_code == '0') & rs.next():
			# 获取一条记录，将记录合并在一起
			data_list.append(rs.get_row_data())
		result = pd.DataFrame(data_list, columns=rs.fields)

		# 结果集输出到csv文件 ####
		result.to_csv(settings.STOCK_NAME, encoding="utf-8", index=False, header=True)
		print(result.head())

		# 登出系统 ####
		bs.logout()

	def test_talib_ATR(self):
		#
		# code_name = ('300623', '捷捷微电')
		# code_name = ('600145', '*ST新亿')
		# code_name = ('601700', '风范股份')
		# code_name = ('000725', '京东方Ａ')
		# code_name = ('002157', '正邦科技')
		code_name = ('300663', '科蓝软件')
		end = '2020-12-30'

		data = utils.read_data(code_name)
		print(data.head())
		result = enter.check_volume(code_name, data, end_date=end)
		print("\nlow atr check {0}'s result: {1}".format(code_name, result))

		rolling_window = 21
		moving_average = 20

		average_true_range = ATR(
			data.high.values[-rolling_window:],
			data.low.values[-rolling_window:],
			data.close.values[-rolling_window:],
			timeperiod=moving_average
		)
		print("*" * 50)
		print(data['high'].values)
		print("*" * 50)
		print(average_true_range)
		print("*" * 10)

	def tearDown(self) -> None:
		print("Test End!")


if __name__ == '__main__':
	unittest.main()
