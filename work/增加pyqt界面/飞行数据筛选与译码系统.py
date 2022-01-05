# -*- coding:utf-8 -*-

# import pandas as pd
from pandas import DataFrame

dic1 = {}
dic2 = {}
with open("QAR数据（飞行航班1） - 副本.txt","r",encoding="utf-8")as f2:
    li2 = f2.readlines()

with open("查找.txt","r",encoding="utf-8")as f:
    li = f.readlines()
for i in li[0].strip().split("/"):
    dic1[i] = []

for i2 in li[1].strip().split("/"):
    dic2[i2] = []

print(dic1)
print(dic2)

for x in li[0].strip().split("/"):
    if len(x) == 2:
        for n in li2:
            if n.startswith(f"#10{x}") or n.startswith(f"#20{x}") or n.startswith(f"#30{x}") or n.startswith(f"#40{x}"):
                dic1[x].append("\t"+n[5:9])
    if len(x) == 3:
        for n in li2:
            if n.startswith(f"#1{x}") or n.startswith(f"#2{x}") or n.startswith(f"#3{x}") or n.startswith(f"#4{x}"):
                dic1[x].append("\t"+n[5:9])

print("=====")

for y in li[1].strip().split("/"):
    if len(y) == 3:
        for m in li2:
            if m.startswith(f"#1{y}"):
                dic2[y].append("\t"+m[5:9])

print(dic1)
print(dic2)



dic1.update(dic2)

num = 0
for k,v in dic1.items():
    if len(v) > num:
        num = len(v)

for k,v in dic1.items():
    if len(v) != num:
        for i in range(num-len(v)):
            v.append("")

#字典中的key值即为csv中列名
dataframe = DataFrame(dic1)
dataframe.to_csv('result.csv',index=False,sep=',')
import pandas as pd
import numpy as np
import re
df = pd.DataFrame(pd.read_excel("译码对应数据.xls"))
data = pd.read_csv('result.csv')
# 这个是转化数据的函数
def convert(x, idxs, coef):
    if type(x) == str:
        # 将16进制的数据转化为10进制，在转化为2进制
        bin_str = bin(int(x, 16))[2:]
        # 固定二进制的长度为16
        if len(bin_str)<16:
            bin_str = '0'*(16-len(bin_str)) + bin_str
        if len(idxs)>1:
            # 从低位开始算的
            bin_str = bin_str[-idxs[1]:-idxs[0]]
        else:
            bin_str = bin_str[-idxs[0]]
        return int(bin_str, 2) * coef
    # 如果16进制是0，则被pandas读取成0，也就是float数据，直接返回0即可
    else:
        return 0

convert_df = pd.DataFrame()
for column in df.columns:
    # 获取特定位数
    if type(df[column][0]) == str:
        idxs = re.findall(r'\d+',df[column][0])
        idxs = list(map(int, idxs))
    else:
        idxs = [int(df[column][0])]
    # 获取系数
    if pd.isnull(df[column][10]):
        coef = 1
    else:
        coef = df[column][10]
    # 需要整合的数据列
    number_columns = []
    for i in range(1, 9):
        # 如果是空值则跳出循环
        if pd.isnull(df[column][i]):
            break
        # 如果不在result.csv文件则跳过，数据问题
        if str(df[column][i]) not in data.columns:
            continue
        number_columns.append(str(int(df[column][i])))
    # 找不到对应的数据，则跳过这个数据
    if len(number_columns) == 0:
        continue
    # 删除掉空值
    new_data = data[number_columns].copy().dropna(axis=0, how='any')
    # 整合多列的数据
    new_data = np.reshape(new_data.values, [-1])
    convert_df[column] = pd.Series(new_data)
    convert_df[column] = convert_df[column].apply(convert, args=[idxs, coef])

convert_df.to_csv('convert.csv', encoding='utf_8_sig', index=False)
