# 对原始数据集进行预处理：根据时间戳进行数据的发送而不是一次性数据发送
#  1. 原始数据集：azurefunctions-accesses-2020-svc.csv
#  2. 预处理后的数据集：sorted_azurefunctions-accesses-2020-svc.csv和request_per_interval.csv。
# 预处理主要是对原始数据进行排序然后根据时间戳确定每一次的请求量。这样每5秒的发送量不同，从而动态的变化请求速率（request/s）