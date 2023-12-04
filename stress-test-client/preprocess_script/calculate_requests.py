import pandas as pd
from tqdm import tqdm

# 逐块读取CSV文件
chunk_size = 10000  # 适当的块大小，可以根据需要调整
input_file = '../dataset/azurefunctions-accesses-2020.csv'
output_file = '../dataset/request_per_interval.csv'

# 获取总行数，以便在tqdm中显示进度
total_rows = sum(1 for _ in pd.read_csv(input_file, chunksize=chunk_size))

# 打开文件以便追加写入
with open(output_file, 'w') as f:
    f.write('count\n')

    # 使用tqdm显示读取的进度
    for chunk in tqdm(pd.read_csv(input_file, chunksize=chunk_size), total=total_rows // chunk_size + 1):
        # 将'Timestamp'列转换为日期时间格式
        chunk['Timestamp'] = pd.to_datetime(chunk['Timestamp'], unit='ms')

        # 初始化变量
        interval_start = chunk['Timestamp'].iloc[0]
        count = 0

        # 遍历块并计算每个间隔的行数
        for index, row in chunk.iterrows():
            if row['Timestamp'] - interval_start > pd.to_timedelta(16000000, unit='ms'):
                f.write(f'{count}\n')
                count = 0
                interval_start = row['Timestamp']
            count += 1

        # 处理最后一个间隔
        f.write(f'{count}\n')
