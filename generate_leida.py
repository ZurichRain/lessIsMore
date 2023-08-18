import numpy as np
import matplotlib.pyplot as plt

import random

char_num = [chr(i) for i in range(ord('A'), ord('Z')+1)]
month = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
cat_lis = ['Category1', 'Category2', 'Category3', 'Category4', 'Category5']
ins_lis = [ 'Interest1', 'Interest2', 'Interest3', 'Interest4', 'Interest5']
scor_lis = [ 'Score1', 'Score2', 'Score3', 'Score4', 'Score5']

all_lis = [
    month,
    cat_lis,
    ins_lis,
    scor_lis
]

all_color_lis =  plt.rcParams['axes.prop_cycle'].by_key()['color']

def get_chart_img(img_idx):
    n = random.randint(3,10)
    # 设置图中的标签
    if n>5:
        st_idx = random.randint(0,len(char_num)-n)
        labels = np.array(char_num[st_idx:st_idx+n])
    else:
        labels = np.array(random.choice(all_lis)[:n])
    print(labels)
    data_n = random.randint(1,5)
    bar_lis = [
        [0,1],
        [1,10],
        [1,100],
        [1,1000],
        [100,200],
        [500,1000]
    ]
    curbar = random.choice(bar_lis)
    # each_data_n = random.randint(curbar[0],curbar[1])
    type_of_data = ['int','float']
    ctype = random.choice(type_of_data)
    data_lis = []
    for _ in range(data_n):
        if ctype == 'int':
            data_lis.append(np.array([random.randint(curbar[0],curbar[1]) for _ in range(n)]))
        else:
            data_lis.append(np.array([random.uniform(curbar[0],curbar[1]) for _ in range(n)]))
    
    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    # 闭合数据
    data_aft = []
    for d in data_lis:
        data_aft.append(np.concatenate((d, [d[0]])))

    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    color_lis = random.sample(all_color_lis,data_n)
    for idx, c in enumerate(color_lis):
        ax.fill(angles, data_aft[idx], color=c, alpha=0.25)
    
    # ax.fill(angles, data, color='red', alpha=0.25)
    # ax.fill(angles, data1, color='blue', alpha=0.25)

    # 设置图中的标签
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # plt.show()
    plt.savefig('./images/{}.jpg'.format(str(img_idx)))
    
    gpt4_prompt='''
我们现在有如下数据表格,
表格标题是: {}
数据是:{}
现在我们将它画成一个雷达图,其中xxx是xxx颜色
关于这个数据你可以提出哪些问题?并给出相应的答案.
'''.format()
    print(gpt4_prompt)


get_chart_img(0)
# # 设置图中的标签
# labels = np.array(['A', 'B', 'C', 'D', 'E'])
# # 数据长度
# data = np.array([2, 3.5, 4, 4.5, 5])
# data1 = np.array([3.5, 3.5, 4, 5, 6])

# # 计算角度
# angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
# # 闭合数据
# data = np.concatenate((data, [data[0]]))
# data1 = np.concatenate((data1, [data1[0]]))
# angles += angles[:1]

# fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# ax.fill(angles, data, color='red', alpha=0.25)
# ax.fill(angles, data1, color='blue', alpha=0.25)

# # 设置图中的标签
# ax.set_yticklabels([])
# ax.set_xticks(angles[:-1])
# ax.set_xticklabels(labels)

# # plt.show()
# plt.savefig('1.jpg')

# # 有如下雷达图,关键信息如下:

