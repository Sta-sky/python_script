from rich import print as rprint

from rich.console import Console

console = Console(color_system='256', style=None)


data = {
	1: "我是一只小小鸟",
	2: "我是一只小小鸟",
	3: "我是一只小小鸟",
	4: "我是一只小小鸟"
}

li = ['1', 'bgfd', '545', 654]

console.print(data)
console.print("[blue underline]Looks like a link")
console.print(locals())
console.print("FOO", style="white on blue")


