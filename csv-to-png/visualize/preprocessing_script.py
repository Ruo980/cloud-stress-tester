import os

import pandas as pd


def preprocess_dataset(input_file, output_file, time_interval):
    """
    预处理数据集
    :param input_file:
    :param output_file:
    :param time_interval:
    :return:
    """
    # 读取 CSV 文件
    df = pd.read_csv(input_file, parse_dates=['Time'])

    # 将时间戳转换为秒，并将第一行的时间作为基准
    df['Time'] = (df['Time'] - df['Time'].iloc[0]).dt.total_seconds()

    # 将时间戳转换为以15秒为步长的序列
    df['Time'] = df['Time'].floordiv(time_interval) * time_interval

    # 保存处理后的数据集为新的 CSV 文件
    df.to_csv(output_file, index=False)


def preprocess():
    """
    预处理过程：将收集到的原生数据集进行预处理，得到可供后续分析的数据集
    """
    # 获取当前工作目录
    current_dir = os.getcwd()

    """
    处理raw数据:CPU和MEMORY指标监控步长为15s，请求和响应数据监控步长为5s
    """
    file_path_OR = current_dir + "/dataset/OR/"
    preprocess_dataset(file_path_OR + 'raw/RAW_CPU.csv', file_path_OR + 'processed/RAW_CPU.csv', 15)
    preprocess_dataset(file_path_OR + 'raw/RAW_MEMORY.csv', file_path_OR + 'processed/RAW_MEMORY.csv', 15)
    preprocess_dataset(file_path_OR + 'raw/RAW_POD.csv', file_path_OR + 'processed/RAW_POD.csv', 15)

    """
    处理RE数据:CPU和MEMORY指标监控步长为15s，请求和响应数据监控步长为5s
    """
    file_path_RE = current_dir + "/dataset/RE/"
    preprocess_dataset(file_path_RE + 'raw/RE_CPU.csv', file_path_RE + 'processed/RE_CPU.csv', 15)
    preprocess_dataset(file_path_RE + 'raw/RE_MEMORY.csv', file_path_RE + 'processed/RE_MEMORY.csv', 15)
    preprocess_dataset(file_path_RE + 'raw/RE_POD.csv', file_path_RE + 'processed/RE_POD.csv', 15)

    """
    合并已经处理好的OR和RE数据集
    """
    raw_cpu_df = pd.read_csv(file_path_OR + 'processed/RAW_CPU.csv')
    re_cpu_df = pd.read_csv(file_path_RE + 'processed/RE_CPU.csv')
    # 使用 "Time" 列作为关联键进行合并
    merged_cpu_df = pd.merge(raw_cpu_df, re_cpu_df, on='Time', suffixes=('_OR', '_RE'))

    raw_memory_df = pd.read_csv(file_path_OR + 'processed/RAW_MEMORY.csv')
    re_memory_df = pd.read_csv(file_path_RE + 'processed/RE_MEMORY.csv')
    # 使用 "Time" 列作为关联键进行合并
    merged_memory_df = pd.merge(raw_memory_df, re_memory_df, on='Time', suffixes=('_OR', '_RE'))

    raw_pod_df = pd.read_csv(file_path_OR + 'processed/RAW_POD.csv')
    re_pod_df = pd.read_csv(file_path_RE + 'processed/RE_POD.csv')
    # 使用 "Time" 列作为关联键进行合并
    merged_pod_df = pd.merge(raw_pod_df, re_pod_df, on='Time', suffixes=('_OR', '_RE'))

    # 将结果保存到新的 CSV 文件
    merged_cpu_df.to_csv(current_dir+'/dataset/merged/cpu_result.csv', index=False)
    merged_memory_df.to_csv(current_dir+'/dataset/merged/memory_result.csv', index=False)
    merged_pod_df.to_csv(current_dir+'/dataset/merged/pod_result.csv', index=False)
