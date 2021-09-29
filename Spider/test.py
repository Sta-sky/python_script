# info = {'1' : 12}

class Test:
	def __init__(self):
		self.default = 'test'
		self.name = '党远洋'
	
	def test_assert(self):
		info = [12]
	
		if info:
			assert isinstance(info, dict), "你的断言出错了"

	def __repr__(self):
		return f'{self.__dict__.keys()}, {self.default}'
	
	def __str__(self):
		return f'名字是, {self.default}'

test = Test()
print(test)
print(test.__repr__())
print(test.__str__())

lists = [1, 2]
s = '332432'
print(dir(s))
print(getattr(s, '__repr__'))

list_ = {'b':2, 'a': 1}
def test(**args):
	print(args)
	
test(**list_)
