import pandas as pd
import matplotlib.pyplot as plt


def merge_response_data(p50_file, p90_file, p95_file, p99_file, output_file):
    """
    预处理数据集: 将四个数据集合并为一个数据集
    :param p50_file:
    :param p90_file:
    :param p95_file:
    :param p99_file:
    :param output_file:
    :return:
    """
    # 读取四个数据集
    df_p50 = pd.read_csv(p50_file, parse_dates=['Time'])
    df_p90 = pd.read_csv(p90_file, parse_dates=['Time'])
    df_p95 = pd.read_csv(p95_file, parse_dates=['Time'])
    df_p99 = pd.read_csv(p99_file, parse_dates=['Time'])

    # 合并数据集
    df_merged = pd.merge(df_p50, df_p90, on="Time", how="outer")
    df_merged = pd.merge(df_merged, df_p95, on="Time", how="outer")
    df_merged = pd.merge(df_merged, df_p99, on="Time", how="outer")

    # 重新排序列的顺序
    df_merged = df_merged[['Time', 'P50', 'P90', 'P95', 'P99']]

    # 使用fillna填充NaN值，例如可以填充为0
    df_merged = df_merged.fillna(0)

    # 保存合并后的数据集为新的 CSV 文件
    df_merged.to_csv(output_file, index=False)


def visualize_merged_data(merged_file):
    """
    可视化数据集：将合并的四个数据集进行可视化
    :type merged_file: object
    :param merged_file:
    :return:
    """
    # 读取合并后的数据集
    df_merged = pd.read_csv(merged_file, parse_dates=['Time'])

    # 设置美化参数
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['figure.titlesize'] = 18

    # 绘制折线图
    plt.figure(figsize=(18, 12))
    plt.plot(df_merged['Time'], df_merged['P50'], marker=None, linestyle='-', color='#3498db', linewidth=2, label='P50')
    plt.plot(df_merged['Time'], df_merged['P90'], marker=None, linestyle='-', color='#2ecc71', linewidth=2, label='P90')
    plt.plot(df_merged['Time'], df_merged['P95'], marker=None, linestyle='-', color='#e74c3c', linewidth=2, label='P95')
    plt.plot(df_merged['Time'], df_merged['P99'], marker=None, linestyle='-', color='#f39c12', linewidth=2, label='P99')

    # 添加标签和标题
    plt.title('Response Time Percentiles Over Time')
    plt.xlabel('Time')
    plt.ylabel('Response Time (ms)')

    # 显示图例和网格
    plt.legend()
    plt.grid(True)

    # 自动调整日期格式
    plt.gcf().autofmt_xdate()

    # 显示图形
    plt.show()

    # 计算百分位数的平均响应时间
    p50_avg = df_merged['P50'].mean()
    p90_avg = df_merged['P90'].mean()
    p95_avg = df_merged['P95'].mean()
    p99_avg = df_merged['P99'].mean()

    # 填充数据，这里是假设的数据，你需要根据实际情况修改
    data = {
        '框架类型': ['默认框架', '柔性框架'],
        '50分位': [p50_avg, p50_avg],  # 这里填充实际的百分位数值
        '90分位': [p90_avg, p90_avg],
        '95分位': [p95_avg, p95_avg],
        '99分位': [p99_avg, p99_avg],
    }

    # 创建 DataFrame
    df = pd.DataFrame(data)
    print(df)


if __name__ == "__main__":
    # 输入四个数据集的文件路径和输出文件的路径
    p50_file = "../dataset/RESPONSE_RATE/ResponseP50.csv"
    p90_file = "../dataset/RESPONSE_RATE/ResponseP90.csv"
    p95_file = "../dataset/RESPONSE_RATE/ResponseP95.csv"
    p99_file = "../dataset/RESPONSE_RATE/ResponseP99.csv"
    output_file = "../dataset/RESPONSE_RATE/MergedResponseData.csv"

    # 调用合并函数
    merge_response_data(p50_file, p90_file, p95_file, p99_file, output_file)

    # 调用可视化函数
    visualize_merged_data(output_file)
