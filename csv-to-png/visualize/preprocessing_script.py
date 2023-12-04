import pandas as pd


def preprocess_dataset(input_file, output_file, time_interval):
    # 读取 CSV 文件
    df = pd.read_csv(input_file, parse_dates=['Time'])

    # 将时间戳转换为秒，并将第一行的时间作为基准
    df['Time'] = (df['Time'] - df['Time'].iloc[0]).dt.total_seconds()

    # 将时间戳转换为以15秒为步长的序列
    df['Time'] = df['Time'].floordiv(time_interval) * time_interval

    # 保存处理后的数据集为新的 CSV 文件
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    """
    处理raw数据:CPU和MEMORY指标监控步长为15s，请求和响应数据监控步长为5s
    """
    file_path_OR = "../dataset/OR/"
    preprocess_dataset(file_path_OR + 'raw/RAW_CPU.csv', file_path_OR + 'processed/RAW_CPU.csv', 15)
    preprocess_dataset(file_path_OR + 'raw/RAW_MEMORY.csv', file_path_OR + 'processed/RAW_MEMORY.csv', 15)
    preprocess_dataset(file_path_OR + 'raw/RAW_REQUEST.csv', file_path_OR + 'processed/RAW_REQUEST.csv', 5)
    preprocess_dataset(file_path_OR + 'raw/RAW_RESPONSE.csv', file_path_OR + 'processed/RAW_RESPONSE.csv', 5)

    """
    处理RE数据:CPU和MEMORY指标监控步长为15s，请求和响应数据监控步长为5s
    """
    file_path_RE = "../dataset/RE/"
    preprocess_dataset(file_path_RE + 'raw/RE_CPU.csv', file_path_RE + 'processed/RE_CPU.csv', 15)
    preprocess_dataset(file_path_RE + 'raw/RE_MEMORY.csv', file_path_RE + 'processed/RE_MEMORY.csv', 15)
    preprocess_dataset(file_path_RE + 'raw/RE_REQUEST.csv', file_path_RE + 'processed/RE_REQUEST.csv', 5)
    preprocess_dataset(file_path_RE + 'raw/RE_RESPONSE.csv', file_path_RE + 'processed/RE_RESPONSE.csv', 5)

    """
    合并已经处理好的OR和RE数据集
    """
    raw_cpu_df = pd.read_csv(file_path_OR + 'processed/RAW_CPU.csv')
    re_cpu_df = pd.read_csv(file_path_RE + 'processed/RE_CPU.csv')
    # 使用 "Time" 列作为关联键进行合并
    merged_cpu_df = pd.merge(raw_cpu_df, re_cpu_df, on='Time', suffixes=('_raw', '_re'))

    raw_memory_df = pd.read_csv(file_path_OR + 'processed/RAW_MEMORY.csv')
    re_memory_df = pd.read_csv(file_path_RE + 'processed/RE_MEMORY.csv')
    # 使用 "Time" 列作为关联键进行合并
    merged_memory_df = pd.merge(raw_memory_df, re_memory_df, on='Time', suffixes=('_raw', '_re'))

    raw_request_df = pd.read_csv(file_path_OR + 'processed/RAW_REQUEST.csv')
    re_request_df = pd.read_csv(file_path_RE + 'processed/RE_REQUEST.csv')
    # 使用 "Time" 列作为关联键进行合并
    merged_request_df = pd.merge(raw_request_df, re_request_df, on='Time', suffixes=('_raw', '_re'))

    raw_response_df = pd.read_csv(file_path_OR + 'processed/RAW_RESPONSE.csv')
    re_response_df = pd.read_csv(file_path_RE + 'processed/RE_RESPONSE.csv')
    # 使用 "Time" 列作为关联键进行合并
    merged_response_df = pd.merge(raw_response_df, re_response_df, on='Time', suffixes=('_raw', '_re'))

    # 将结果保存到新的 CSV 文件
    merged_cpu_df.to_csv('../dataset/merged/cpu_result.csv', index=False)
    merged_memory_df.to_csv('../dataset/merged/memory_result.csv', index=False)
    merged_request_df.to_csv('../dataset/merged/request_result.csv', index=False)
