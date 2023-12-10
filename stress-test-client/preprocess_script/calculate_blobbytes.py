# 分别可视化原数据集和排序后数据集的blob_bytes字段的数据分布
"""

import pandas as pd
import matplotlib.pyplot as plt

# 可视化原数据集的blob_bytes字段的数据分布

df = pd.read_csv('../dataset/azurefunctions-accesses-2020.csv')
df.plot(y='BlobBytes', figsize=(20, 10), title='Blob bytes distribution')
plt.show()

# 按照时间戳重新排序azurefunctions-accesses-2020.csv
# 将Timestamp列转换为pandas的时间格式并进行重新排序并生成csv文件
pd.read_csv('../dataset/azurefunctions-accesses-2020.csv').sort_values(by='Timestamp').to_csv("../dataset/sorted_azurefunctions-accesses-2020.csv", index=False)
# 可视化新数据集blob_bytes字段的数据分布
df = pd.read_csv('../dataset/sorted_azurefunctions-accesses-2020.csv')
df.plot(y='BlobBytes', figsize=(20, 10), title='Sorted Blob bytes distribution')
plt.show()
"""
