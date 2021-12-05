

def printColor(msg, color=None, style=0):
	colorDci = {
		'orange': 31,
		'green': 32,
		'red': 33,
		'white': 34,
		'fense': 35,
		'blue': 36,
		'gray': 37,
	}
	if color:
		color = colorDci.get(color)
		if not color:
			color = 30
	print(f'\033[{style};{color}m {msg} \033[m')

