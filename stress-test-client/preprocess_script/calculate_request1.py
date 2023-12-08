# 绘制 request-1.csv 数据集的请求量

import pandas as pd
import matplotlib.pyplot as plt

# 读取request-1.csv数据集
request_file_path = "../dataset/requests-1.csv"
df = pd.read_csv(request_file_path)
# 绘制count列的变化折线图
df.plot(y='count', figsize=(20, 10), title='Requests per hour')
plt.show()
