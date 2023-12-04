import pandas as pd

# 读取CSV文件
file_path = "../dataset/sorted_azurefunctions-accesses-2020-svc.csv"
output_file = '../dataset/request_per_interval2.csv'
df = pd.read_csv(file_path)

# 将Timestamp列转换为pandas的时间格式
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

# 获取第一行的时间戳
first_timestamp = df['Timestamp'].iloc[0]

# 计算每行数据与第一行数据的时间差（以毫秒为单位）
df['TimeDifference'] = (df['Timestamp'] - first_timestamp).dt.total_seconds() * 1000

# 将第一行时间戳设定为0，其他行的时间戳值为原时间戳与第一行时间戳的差值
df['AdjustedTimestamp'] = df['TimeDifference'].astype(int)

# 保存整理后的数据到新的CSV文件
df.to_csv(output_file, index=False)

# 打印整理后的数据框
print(df[['Timestamp', 'AdjustedTimestamp']])
