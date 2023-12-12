# 绘制 request-2.csv 数据集的请求量

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取request-1.csv数据集
request_file_path = "../dataset/requests-3.csv"
df = pd.read_csv(request_file_path)
# 绘制count列的变化折线图
df.plot(y='count', figsize=(20, 10), title='Requests per hour')
plt.show()

# 归一化处理：将count数据映射到[0,15]的区间
df['count'] = (df['count'] - df['count'].min()) / (df['count'].max() - df['count'].min()) * 15
df.plot(y='count', figsize=(20, 10), title='Requests per hour')
plt.show()
# 将归一化数据保存到新的数据集中
df.to_csv('../dataset/request/requests-3-normalized.csv', index=False)

# 重复每行5次
extended_df = pd.DataFrame(np.repeat(df.values, 5, axis=0), columns=df.columns)

# 绘制曲线
plt.figure(figsize=(20, 10))

# 绘制 count 的折线图
extended_df.plot(y='count', label='count', title='Requests per hour')
plt.show()
