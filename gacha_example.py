from GGanalysis import FiniteDist
import numpy as np

# 使用 FiniteDist 类进行快速卷积
a = FiniteDist([0, 0.25, 0.5, 0.25])  # 从列表初始化分布律
b = FiniteDist(np.array([0, 0.5, 0.5]))  # 从numpy数组初始化分布律
c = a * b ** 5  # c的分布为a的分布卷积5次b的分布
# print('a的期望、方差、分布为', a.exp, a.var, a)
# print('b的期望、方差、分布为', b.exp, b.var, b)
# print('c的期望、方差、分布为', c.exp, c.var, c)
#
# print('分布在类中以numpy数组形式保存', c.dist)

# 计算抽卡所需抽数分布律 以原神为例
import GGanalysis.games.genshin_impact as GI


def gacha_divination(
        target_character_num: int,
        exist_character_pull_count: int,
        exist_character_big_guarantee: bool,
        target_weapon_num: int,
        exist_weapon_pull_count: int,
        exist_weapon_big_guarantee: bool,
        exist_weapon_fate_point: int
):
    """
    预测抽卡期望
    :param target_character_num: 要抽的角色数
    :param exist_character_pull_count: 角色池已经垫了的数量
    :param exist_character_big_guarantee: 角色池下一个保底是否为大保底
    :param target_weapon_num: 要抽的武器数量
    :param exist_weapon_pull_count: 武器池已经垫了的数量
    :param exist_weapon_big_guarantee: 武器池下一个保底是否为大保底
    :param exist_weapon_fate_point: 武器池定轨命定值
    """
    # 原神角色池的计算
    # print('角色池在垫了20抽，有大保底的情况下抽3个UP五星抽数的分布')
    print(f'初始化角色池环境\n要抽的角色数量：{target_character_num}\n已垫抽数：{exist_character_pull_count}\n'
          f'下一个保底是否为大保底：{exist_character_big_guarantee}')
    dist_c = GI.up_5star_character(
        item_num=target_character_num,
        pull_state=exist_character_pull_count,
        up_guarantee=1 if exist_character_big_guarantee else 0
    )
    # print('期望为', dist_c.exp, '方差为', dist_c.var, '分布为', dist_c.dist)
    print(f'\033[31m期望为：{dist_c.exp}\033[0m\n\033[31m方差为：{dist_c.var}\033[0m')
    print()

    # 原神武器池的计算
    print(f'初始化武器池环境\n要抽的武器数量：{target_weapon_num}\n已垫抽数：{exist_weapon_pull_count}\n'
          f'下一个保底是否为大保底：{exist_weapon_big_guarantee}\n定轨命定值：{exist_weapon_fate_point}')
    dist_w = GI.up_5star_ep_weapon(
        item_num=target_weapon_num,
        pull_state=exist_weapon_pull_count,
        up_guarantee=1 if exist_weapon_big_guarantee else 0,
        fate_point=exist_weapon_fate_point
    )
    # print('期望为', dist_w.exp, '方差为', dist_w.var, '分布为', dist_w.dist)
    # print('期望为', dist_w.exp, '方差为', dist_w.var)
    print(f'\033[31m期望为：{dist_w.exp}\033[0m\n\033[31m方差为：{dist_w.var}\033[0m')
    print()

    # 联合角色池和武器池
    print(f'在前述条件下抽{target_character_num}个角色和{target_weapon_num}个武器所需抽数分布')
    dist_c_w = dist_c * dist_w
    # print('期望为', dist_c_w.exp, '方差为', dist_c_w.var, '分布为', dist_c_w.dist)
    print(f'\033[31m期望为：{dist_c_w.exp}\033[0m\n\033[31m方差为：{dist_c_w.var}\033[0m')
    print()

    # 需要画图则打开注释
    from GGanalysis.gacha_plot import DrawDistribution
    fig = DrawDistribution(
        dist_c_w,
        title=f'角色池已垫抽数：{exist_character_pull_count}，下个保底是否为大保底：{exist_character_big_guarantee}\n'
              f'武器池已垫抽数：{exist_weapon_pull_count}，下个保底是否为大保底：{exist_weapon_big_guarantee}，定轨命定值：{exist_weapon_fate_point}\n'
              f'获取{target_character_num}个角色及{target_weapon_num}个武器所需抽数',
        dpi=72
    )
    fig.draw_two_graph()


gacha_divination(
    target_character_num=2,
    exist_character_pull_count=69,
    exist_character_big_guarantee=False,
    target_weapon_num=1,
    exist_weapon_pull_count=33,
    exist_weapon_big_guarantee=False,
    exist_weapon_fate_point=0
)

# 对比玩家运气
# dist_c = GI.up_5star_character(item_num=10)
# dist_w = GI.up_5star_ep_weapon(item_num=3)
# print('在同样抽了10个UP五星角色，3个特定UP五星武器的玩家中，仅花费1000抽的玩家排名前',
#       str(round(100 * sum((dist_c * dist_w)[:1001]), 2)) + '%')
