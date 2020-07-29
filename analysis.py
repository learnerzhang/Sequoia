import warnings
import pandas_datareader.data as web
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
# ⽤来正常显示中⽂标签
plt.rcParams['axes.unicode_minus'] = False
# ⽤来正常显示负号 #有中⽂出现的情况，需要u'内容'
warnings.filterwarnings('ignore')


def get_stock(start, end, code, update=False):
	# 获取股票数据
	if update:
		stock_data = web.DataReader(code, 'yahoo', start, end)
		stock_data.to_csv("ipynb_data/{}.csv".format(code))
	df = pd.read_csv("ipynb_data/{}.csv".format(code))
	# df.info()
	# df.tail(10)
	return df


def stock_tendency(df):
	# 计算跌涨幅
	df['Range'] = df['Close'] - df['Close'].shift(1)
	# 调整数据索引
	df.index = df.Date
	df = df[['High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close', 'Range']]
	# 简单查看股票价格走势图
	df['Close'].plot(figsize=(20, 4), color='r', alpha=0.8, grid=True, rot=0, title='{} tendency'.format(code))
	plt.show()


def get_ma(df):
	df['Close'].plot(figsize=(20, 4), c='b')
	df['Close'].rolling(window=10).mean().plot(c='b')
	df['Close'].rolling(window=10).mean().plot(c='r')
	df['Close'].rolling(window=30).mean().plot(c='y')
	df['Close'].rolling(window=60).mean().plot(c='g')
	plt.legend(['Close', '30ave', '60ave'], loc='best')
	plt.show()


def get_min_max(df):
	"""
		Min-Max 标准化是最常用的规范化手段
	"""
	df_min_max = (df - df.min()) / (df.max() - df.min())
	df_min_max.plot(figsize=(16, 9))
	plt.show()


if __name__ == '__main__':
	start = datetime.datetime(2018, 1, 1)  # 指定开始时间
	end = datetime.datetime.now()  # 指定结束时间
	code = '002605.SZ'
	code = '600178.SS'
	df = get_stock(start, end, code)
	print(df.isnull().values.sum())
	stock_tendency(df)
	get_ma(df)
	get_min_max(df)
