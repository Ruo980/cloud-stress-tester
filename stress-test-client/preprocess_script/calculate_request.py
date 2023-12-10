# 重新计算数据集的请求量变化

import pandas as pd
import matplotlib.pyplot as plt

file_path = "../dataset/azurefunctions-accesses-2020.csv"
df = pd.read_csv(file_path)

# 将Timestamp列转换为pandas的时间格式
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

# 将时间戳转为日期格式
df['Date'] = df['Timestamp'].dt.date
# 将时间戳转为小时格式
df['Hour'] = df['Timestamp'].dt.hour

# 生成新的csv数据集：按照日期统计每天的行数
df.groupby('Date').size().to_csv('../dataset/request_per_day.csv', header=['count'])
# 生成新的csv数据集：按照小时统计每小时的行数
df.groupby(['Hour']).size().to_csv('../dataset/request_per_hour.csv', header=['count'])
# 生成新的csv数据集：按照日期小时统计每天每小时的行数
df.groupby(['Date', 'Hour']).size().to_csv('../dataset/request_per_day_hour.csv', header=['count'])

# 数据可视化：将该数据集绘制成折线图，显示每天的请求数量
request_file_path = "../dataset/request_per_day.csv"
df = pd.read_csv(request_file_path)
df['Date'] = pd.to_datetime(df['Date'])
df.plot(x='Date', y='count', figsize=(20, 10), title='Requests per day')
plt.show()

# 数据可视化：将该数据集绘制成折线图，显示每天每小时的请求数量
request_file_path = "../dataset/request_per_hour.csv"
df = pd.read_csv(request_file_path)
df['Hour'] = pd.to_datetime(df['Hour'])
df.plot(x='Hour', y='count', figsize=(20, 10), title='Requests per hour')
plt.show()

# 数据可视化：将该数据集绘制成折线图，显示每天每小时的请求数量
request_file_path = "../dataset/request_per_day_hour.csv"
df = pd.read_csv(request_file_path)
df.plot(y='count', figsize=(20, 10), title='Requests per day per hour')
plt.show()


# 归一化处理：将count数据映射到[0,250]的区间
df['count'] = (df['count'] - df['count'].min()) / (df['count'].max() - df['count'].min()) * 250
df.plot(y='count', figsize=(20, 10), title='Requests per hour')
plt.show()
# 将归一化数据保存到新的数据集中
df.to_csv('../dataset/request/requests-normalized.csv', index=False)