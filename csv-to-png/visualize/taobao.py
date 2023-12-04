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


def visualize_cpu_data(RL_path, SL_path):
    # 读取CSV文件
    df1 = pd.read_csv(RL_path)
    df2 = pd.read_csv(SL_path)

    # 设置美化参数
    beautify_plot()

    # 绘制折线图
    plt.figure(figsize=(14, 9))
    plt.plot(df1['Epoch'], df1['CTR'], marker=None, linestyle='-', color='#2ecc71', linewidth=2, label="RL")
    plt.plot(df2['Epoch'], df2['CTR'], marker=None, linestyle='-', color='#e74c3c', linewidth=2, label="SL")
    # 添加标签和标题
    plt.title('CTR OVER Epoch')
    plt.xlabel('Epoch')
    plt.ylabel('CTR')

    # 显示图例和网格
    plt.legend()
    plt.grid(True)

    # 显示图形
    plt.show()


# 在函数外调用，确保不会在导入时显示图形
if __name__ == "__main__":
    RL_path = "../dataset/taobao/RL_output.csv"
    SL_path = "../dataset/taobao/SL_output.csv"
    visualize_cpu_data(RL_path, SL_path)
