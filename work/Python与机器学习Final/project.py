import numpy as np
import pandas as pd
import matplotlib.pyplot as plot

'==================================== 读取数据 ================================================================================='
csv_path  = 'F:\work_projects\python_script\work\Python与机器学习Final\Pokemon\pokemon.csv'
pokemon_data = pd.read_csv(csv_path)
total_size = pokemon_data.size

percent_missing = pokemon_data.isnull().sum() * 100 / len(pokemon_data)
missing_value_df = pd.DataFrame({
    'column_name': pokemon_data.columns,
    'percent_missing': percent_missing
})

print('数据缺失前10排名：')
miss_10 = missing_value_df.sort_values(by='percent_missing', ascending=False).head(10)
print(miss_10)


'======================================= 整体平均性别占比 =============================================================================='
# 计算pokemon的性别占比
# 获取所有pokemon性别
pokemon_sex_scale = pokemon_data["percentage_male"]
# 获取所有
sex_count = pokemon_sex_scale.count()
sex_total_sum = pokemon_sex_scale.sum()
sex_scale = sex_total_sum / sex_count
print(f'整体平均性别占比为： {sex_scale}')


'======================================= 宝可梦体型（身高，体重）分布 =============================================================================='
# 身高
# 统计升高  axis = 0 删除包含NaN的任何行  axis = 1 表示列
pokemon_height = pokemon_data['height_m'].dropna(axis=0)
print(len(pokemon_height))
pokemon_mean_height = pokemon_height.mean()
pokemon_media_height = pokemon_height.median()
pokemon_height_max = pokemon_height.max()
pokemon_height_min = pokemon_height.min()

print(f'所有宝可梦的平均升高为: {pokemon_mean_height}'
      f'中位身高为：{pokemon_media_height},'
      f'最高的为：{pokemon_height_max}'
      f'最低的为：{pokemon_height_min}')


# 体重
pokemon_weight = pokemon_data['weight_kg'].dropna(axis=0)
pokemon_mean_weight = pokemon_weight.mean()
pokemon_media_weight = pokemon_weight.median()
pokemon_weight_max = pokemon_weight.max()
pokemon_weight_min = pokemon_weight.min()
print(f'所有宝可梦的平均体重为: {pokemon_mean_weight}'
      f'中位体重为：{pokemon_media_weight},'
      f'最重的为：{pokemon_weight_max}'
      f'最轻的为：{pokemon_weight_min}')

'======================================= 不同世代的宝可梦数量分布 =============================================================================='

# 获取pokemon的所有世代，并统计每个世代有多少数量
pokemon_generation = pokemon_data['generation'].value_counts()
# 利用matplot画出图形进行分析

pokemon_generation.sort_values(ascending=False).plot(kind="bar",alpha=1, width=0.8, color="#99ccff", edgecolor="white", label="所有世代宝可梦的数量", lw=3)
generation_max = pokemon_generation.max()
generation_min = pokemon_generation.min()
plot.show()
print(f"从途中不难看出，第五代的宝可梦数据是最多的为: {generation_max}  而第六代的数量是最少的为{generation_min}")

'======================================= 比较不同世代的宝可梦水平（基础攻击，基础防御，特殊攻击，特殊防御，速度等） =============================================================================='

#建立数据透视表

def draw_excel(action, color="#66CCCC", description=None):
    try:
        # values='attack' 需要计算的值
        # index='generation' 分组的依据
        # aggfunc='sum' 选择聚合函数
        pokemonAttr = pokemon_data[['generation', action]]
        pokemon_info = pokemonAttr.pivot_table(values=action, index='generation', aggfunc='sum')
        pokemon_info.sort_values(by=action).plot(kind='bar', alpha=1, width=0.8, color=color, edgecolor="white", label= description, lw=3)
        pokemon_action_max = pokemon_info[action].max()
        pokemon_action_min = pokemon_info[action].min()
        pokemon_dic = pokemon_info.to_dict()
        
        index_max = None
        index_min = None
        for key, val in pokemon_dic[action].items():
            if val == pokemon_action_max:
                index_max = key
            if val == pokemon_height_min:
                index_min = key
        print(f"宝可梦的 {action} 属性对比结果, "
              f"最大的为第 {index_max} 代宝可梦,{action}为：{pokemon_action_max},"
              f"最小的为第 {index_min} 代宝可梦,{action}为：{pokemon_action_min} ")
        plot.show()
    except Exception as e:
        print('输入参数有有误')
        raise

info_dic = {
    "attack": "所有世代宝可梦的攻击属性对比",
    "defense": "所有世代宝可梦的防御对比",
    "sp_attack": "所有世代宝可梦的特殊攻击对比",
    "sp_defense": "所有世代宝可梦的特殊防御对比",
    "speed": "所有世代宝可梦的攻击速度对比"}
for key, value in info_dic.items():
    draw_excel(key, description=value)



'======================================= 宝可梦的类型（type1，type2）分布如何？ =============================================================================='
# type1
type_1_pokemon = pokemon_data['type1'].value_counts()
type_1_pokemon.sort_values(ascending=True).plot(kind="barh", alpha=1, width=0.8, color="#9966ff", edgecolor="white", label="type1宝可梦分布", lw=3)
type_1_max = type_1_pokemon.max()
type_1_min = type_1_pokemon.min()
plot.show()
print(f'type1的宝可梦中water宝可梦是最多为：{type_1_max}只，flying宝可梦数量是最少的为：{type_1_min}只')


# type2
type_2_pokemon = pokemon_data['type2'].value_counts()
type_2_pokemon.sort_values(ascending=True).plot(kind="barh",alpha=1, width=0.8, color="#9966ff", edgecolor="white", label="type2宝可梦分布", lw=3)
type_2_max = type_2_pokemon.max()
type_2_min = type_2_pokemon.min()
plot.show()
print(f'type2的宝可梦中water宝可梦是最多为：{type_2_max}只，flying宝可梦数量是最少的为：{type_2_min}只')

'======================================= 传奇宝可梦的数量是多少？ =============================================================================='
legend_pokemon_count = pokemon_data['is_legendary'].value_counts()
print(f'传奇宝可梦的数量为：{legend_pokemon_count[1]}')
