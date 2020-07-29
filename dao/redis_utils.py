import redis


class RedisUtils:
	def __init__(self):
		pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
		self.r = redis.Redis(connection_pool=pool)

	def set(self, key, value):
		return self.r.set(key, value)

	def get(self, key):
		return self.r.get(key)

	def rpush(self, key, values):
		return self.r.rpush(key, values)

	def lpush(self, key, values):
		return self.r.lpush(key, values)

	def sadd(self, key, values):
		"""
		向键为key的集合中添加元素
		"""
		return self.r.sadd(key, values)

	def srem(self, key, values):
		"""
		从键为key的集合中删除元素
		"""
		return self.r.srem(key, values)

	def scard(self, key):
		"""
			返回键为key的集合的元素个数
		"""
		return self.r.scard(key)

	def smembers(self, key):
		"""
		返回键为key的集合的所有元素
		"""
		return self.r.smembers(key)

	def getAllKeys(self, pattern):
		return self.r.keys(pattern=pattern)