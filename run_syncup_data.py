# -*- encoding: UTF-8 -*-
import baostock as bs
import pandas as pd
import json
import utils
import logging
import settings
import schedule
import time

from dao.redis_utils import RedisUtils

logging.basicConfig(format='%(asctime)s %(message)s', filename='sequoia.log')
logging.getLogger().setLevel(logging.INFO)

settings.init()
redisUtils = RedisUtils()


def update_pool2redis():
	# 登陆系统 ####
	lg = bs.login()
	# 显示登陆返回信息
	print('login respond error_code:' + lg.error_code + ', error_msg:' + lg.error_msg)
	dt = utils.get_recently_trade_date()
	dt = '2020-07-20'
	stock_rs = bs.query_all_stock(day=dt)
	stock_df = stock_rs.get_data()
	# print(stock_df)
	stocks = stock_df.set_index('code').T.to_dict(orient='list')
	sJsonStr = json.dumps(stocks, indent=4, ensure_ascii=False).encode('utf-8')
	r = redisUtils.set("Ashare", sJsonStr)
	print("update Ashare to Redis, status:", r)
	bs.logout()


def update_stock_daily(history=False):
	try:
		et = utils.get_recently_trade_date()
		st = et
		if history:
			st = settings.START_DATE
		print(st, et)
		# 登陆系统 ####
		lg = bs.login()
		# 显示登陆返回信息
		print('login respond error_code:' + lg.error_code + ', error_msg:' + lg.error_msg)
		stock = redisUtils.get("Ashare")
		stockJson = json.loads(stock)
		for code in stockJson:
			name = stockJson[code][1]
			if "ST" in name:
				continue
			print("Downloading :" + code + " , name :" + name)
			k_rs = bs.query_history_k_data_plus(code, settings.STOCK_FIELDS, start_date=st, end_date=et)
			print(k_rs.get_data())
			stock_records = k_rs.get_data().to_dict('records')
			for record in stock_records:
				rJsonStr = json.dumps(record, indent=4, ensure_ascii=False).encode('utf-8')
				r = redisUtils.sadd(code, rJsonStr)
				print(r)
			print("{} redis add finish".format(code))
		bs.logout()
	except IOError:
		print("Update Data Error ")


if __name__ == '__main__':
	# update_pool2redis()
	update_stock_daily(history=True)
