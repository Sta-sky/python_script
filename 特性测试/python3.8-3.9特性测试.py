
"""
python 3.9， 3.8 新特性

"""

# 字典合并更新
dict_1 = {1: "1", 2: "2"}
dict_2 = {3: "3", 2: "2"}

# 1
print({**dict_2, **dict_1})

# 2
dict_2.update(dict_1)

print(dict_2)
print(dict_1)
# 3
print(dict_1 | dict_2)


# 赋值表达式
a = [1,2,3]
if (n := len(a)) < 10:
    print(f"List is too long ({n} elements, expected <= 10)")


# 仅限位置形参

# def param(a, b, /, c, d):
#
#     print(a, b, c, d)
#
#
# param(3, 4, test=3, test1=5)

def parse(family):
    test = family.split()
    print(test)
    firstname, secoend, *members, lastname = family.split()
    return firstname.upper(),secoend.upper(), *members, lastname.upper()


print(parse('simpsons homer marge bart lisa maggie'))
# ('SIMPSONS', 'homer', 'marge', 'bart', 'lisa', 'maggie')


# 字典推导式输入值
# cast_1 = {input('role? ') : input('actor? ')}
# cast = {input(f'请输入第{i}个key： '): input(f'请输入第{i}个value： ') for i in range(2)}
# print(cast)

# 数组推导式输入值
# test_list = [int(input(f"请输入第{item}个元素")) for item in range(3)]
#
# print(test_list)


from itertools import accumulate

print(accumulate([10, 5, 30, 15], initial=1000))

from pprint import pprint, pp
d = dict(d=1, c=3, a=2)

print("=="*50)
pp(d)                  # 根据字典的key倒叙

pprint(d)              # 根据字典的key正序

b = 100
match b:
    case 300:
        print("test")
    case _:
        print("success")



