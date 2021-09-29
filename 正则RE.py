
全局变量：
	字符串
	strings = 'sprint432trekjre0gtrj￥@……%￥%#5434tergr'	
	
1、match跟search的区别：
	pattern = 'print'
	res = re.match(pattern, strings)
	print(res)
	
	pattern = 'tr'
	res = re.search(pattern, strings)
	print(res.group(0))

	match只能匹配跟字符串起始位置跟pattern一致的，当pattern在中间时，匹配出来的为空。
	search能匹配出在字符串任意位置中存在跟pattern相匹配的字符。
	
2、sub跟subn
	subn会返回一个元组，第一个参数为查找替换后的字符串，第二个参数为替换的次数（意思就是有多少个匹配的）。
	sub只返回替换后的字符串。
	
3、匹配出字符串中所有的字母：
	pattern = '[A-Za-z]'
	pattern = re.findall(pattern, strings)
	
4、匹配出字符串所有的数字：
	pattern = '\d+'   -------> --贪婪匹配 ['432', '0', '5434'] 
	pattern = '\d'   ------->  --非贪婪匹配 ['4', '3', '2', '0', '5', '4', '3', '4'] 	
	pattern = re.findall(pattern, strings)
	
5、匹配出所有的普通字符;
	pattern = '\w+'   ------->  --贪婪匹配   ['sprint432trekjre0gtrj', '5434tergr'] 
	pattern = '\w+'	  ------->  --非贪婪匹配 ['s', 'p', 'r', 'i', 'n', 't', '4', '3', '2', 't', 'r', 'e', 'k', 'j', 'r', 'e', '0', 'g', 't', 'r', 'j', '5', '4', '3', '4', 't', 'e', 'r', 'g', 'r'] 
	pattern = re.findall(pattern, strings)


6、邮箱匹配：
	email = 'holddang@sina.com'
	re.match(r'[0-9a-zA-Z_]{0,19}@[sina,163,qq]{1}.[com, net, cn]{1}',text)

