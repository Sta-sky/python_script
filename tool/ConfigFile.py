import configparser


class MyConfigFile:
	
	def __init__(self, config_path):
		self.config_path = config_path
		self.cp = configparser.ConfigParser()
	
	def get_sections(self) -> list:
		"""	返回 配置 大项 """
		try:
			return self.cp.sections()
		except  Exception as e:
			return []
		
	def get_keys(self, item: str) -> list:
		""" 获取单项 的所有键 """
		try:
			return self.cp.options(item)
		except Exception as e:
			return []
		
	def get_items(self, item: str) -> list:
		""" 获取 单项的所有 键值对"""
		try:
			return self.cp.items(item)
		except Exception as e:
			return []
		
	def get_val(self, item: str, key: str) -> str:
		try:
			return self.cp.get(item, key)
		except Exception as e:
			return ''
	
	def add_section(self, item: str) -> bool:
		try:
			self.cp.add_section(item)
			return True
		except Exception as e:
			return False
	
	def add_key_val(self, item: str, key: str, val: str) -> bool:
		try:
			self.cp.set(item, key, val)
		except Exception as e:
			return False
	
	def write_config_file(self) -> bool:
		""" 写入 文件 """
		try:
			with open(self.config_path, 'w+') as f:
				self.cp.write(f)
			return True
		except Exception as e:
			return False

