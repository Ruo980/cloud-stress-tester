import os

import visualize

if __name__ == '__main__':
    # 获取当前工作目录
    current_dir = os.getcwd()

    # 数据预处理：读取原生框架指标和柔性框架指标，处理时间戳并合并结果，导出到各自文件夹
    visualize.preprocessing_script.preprocess()

    # 数据可视化：读取处理后的CPU数据，绘制折线图
    visualize.visualize_cpu_data.visualize_cpu_data(current_dir + "/dataset/merged/cpu_result.csv")

    # 数据可视化：读取处理后的Memory数据，绘制折线图
    visualize.visualize_memory_data.visualize_memory_data(current_dir +"/dataset/merged/memory_result.csv")

    # 数据可视化：读取处理后的Pod数据，绘制折线图
    visualize.visualize_pod_data.visualize_cpu_data(current_dir +"/dataset/merged/pod_result.csv")
