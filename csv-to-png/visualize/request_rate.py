import pandas as pd
import matplotlib.pyplot as plt


def beautify_plot():
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['figure.titlesize'] = 18


def visualize_cpu_data(file_path):
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 设置美化参数
    beautify_plot()

    # 提取数量和时间列
    data = df['count']
    time = [i * 5 for i in range(1, len(data) + 1)]
    # 将数据除以5
    modified_data = data / 5

    # 绘制折线图
    plt.figure(figsize=(18, 12))
    plt.plot(time, modified_data, marker=None, linestyle='-', color='#2ecc71', linewidth=2,label="Raw_request")

    # 添加标签和标题
    plt.title('REQUEST RATE OVER TIME')
    plt.xlabel('Time (s)')
    plt.ylabel('Request Rate (ops/s)')

    # 显示图例和网格
    plt.legend()
    plt.grid(True)

    # 显示图形
    plt.show()


# 在函数外调用，确保不会在导入时显示图形
if __name__ == "__main__":
    file_path = "../dataset/REQUEST_RATE/request_per_interval2.csv"
    visualize_cpu_data(file_path)
