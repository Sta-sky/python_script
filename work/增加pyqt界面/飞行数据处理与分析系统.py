import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

def plot_col(df, cols):
    # h = np.array(df['时']).astype(np.string_)
    # m = np.array(df['分']).astype(np.string_)
    # s = np.array(df['秒']).astype(np.string_)
    # sym = np.array(['-']*len(h))
    # time = h+sym+m+sym+s
    # print(time)
    time = df['时'].apply(str) + '-' + df['分'].apply(str) + '-' + df['秒'].apply(str)
    time = time.loc[time != '0-0-0']
    Xtick = []
    for i in time:
        Xtick.append(i)
        Xtick.append(' ')
        Xtick.append(' ')
        Xtick.append(' ')

    for c in cols:
        print(c)
        if isinstance(c, list):
            title = '_'.join(c)
            y = df[c[0]]
            for i in range(1, len(c)):
                y += df[c[i]]
            x = range(len(df))
            z = np.polyfit(x, y, 7)
            p = np.poly1d(z)
            plt.figure(figsize=(50, 30))
            plt.tick_params(axis='x', labelsize=8)
            plt.plot(x, y, label=str(p))
            plt.xticks(x, Xtick, rotation=270)
            plt.xlabel('time')
            plt.ylabel(title)
            plt.title(title)
            plt.legend()
            title = title.replace('/', '_')
            plt.savefig('{}.jpg'.format(title))

        else:
            x = range(len(df))
            y = df[c]
            z = np.polyfit(x, y, 7)
            p = np.poly1d(z)
            plt.figure(figsize=(50, 30))
            plt.plot(x, y, label=str(p))
            plt.xticks(x, Xtick, rotation=270)
            plt.tick_params(axis='x', labelsize=8)
            plt.xlabel('time')
            plt.ylabel(c)
            plt.title(c)
            plt.legend()
            c = c.replace('/', '_')
            plt.savefig('{}.jpg'.format(c))



if __name__ == '__main__':
    data = pd.read_csv('convert.csv', encoding='gbk')
    cols = ['俯仰/度', '滚转/度', '航向/度', ['无线电高度高位/FT', '无线电高度低位/FT'], '计算空速/KT', '垂直速度/KT',
            '马赫数', '推力扭矩']
    plot_col(data, cols)

