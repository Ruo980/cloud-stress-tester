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

    # 绘制折线图
    plt.figure(figsize=(14, 9))
    plt.plot(df['Time'], df['CPU_OR'], marker=None, linestyle='-', color='#2ecc71', linewidth=2,label="OR_CPU")
    plt.plot(df['Time'], df['CPU_RE'], marker=None, linestyle='-', color='#e74c3c', linewidth=2,label="RE_CPU")

    # 添加标签和标题
    plt.title('CPU USAGE OVER TIME')
    plt.xlabel('Time (s)')
    plt.ylabel('CPU Used Rate (%)')

    # 显示图例和网格
    plt.legend()
    plt.grid(True)

    # 显示图形
    plt.show()


# 在函数外调用，确保不会在导入时显示图形
if __name__ == "__main__":
    file_path = "../dataset/merged/cpu_result.csv"
    visualize_cpu_data(file_path)
