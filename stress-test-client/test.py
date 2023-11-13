import csv
import os
import random
import string
from locust import HttpUser, TaskSet, task, constant


# 读取 azurefunctions-accesses-2020.csv 数据集：不是一次性读完，而是调用一次读取一行数据
def read_data_file():
    # 持续从 azurefunctions-accesses-2020.csv 文件中读取数据的生成器
    while True:
        with open('dataset/azurefunctions-accesses-2020.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过标题行
            for row in reader:
                if len(row) >= 11:  # 确保行中至少有11个值
                    yield row


# 读取 request.csv 数据集：利用迭代器实现每隔一定周期读取一行数据
def read_requests_per_interval():
    # 持续从 test.csv 文件中读取每个时间段的请求数的生成器
    while True:
        with open('test.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                yield int(row[0])


class TestLocust(TaskSet):
    """
    测试类:两个测试任务
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_iterator = iter(read_data_file())
        self.requests_iterator = iter(read_requests_per_interval())

    @task(1)  # 参数表示执行次数，不写默认1次
    def user_query_message(self):
        """
        测试查询消息的任务。
        """
        # 读取当前时间点的请求数：用户发起几次周期性请求：比如第二个5秒，还是第三个5秒，使得用户能够在第n个请求周期找到发起请求行数
        current_requests = next(self.requests_iterator, None)

        # 如果数据不为空，则发起相应数量的请求
        if current_requests is not None:
            for _ in range(current_requests):
                # 读取当前时间点的行数：读取azurefunctions-accesses-2020.csv，获取指定周期内的指定行数
                current_row = next(self.data_iterator, None)

                # 如果数据不为空，则根据数据执行相应的请求
                if current_row is not None:
                    blob_bytes = current_row[8]
                    read = current_row[9]
                    blog_bytes = float(blob_bytes)
                    num = round(blog_bytes / 1000)
                    if num <= 0:
                        num = 1
                    header = {'Content-Type': 'application/json;charset=UTF-8'}
                    if read == "True":
                        # 发起 GET 请求
                        url = '/users' + '?row=' + str(num)
                        r = self.client.get(url, headers=header)
                        # 断言返回结果中的 "succ" 字段值为 "ok"
                        assert r.status_code == 200
                    else:
                        # 生成 num 个随机用户数据
                        users = []
                        for _ in range(num):
                            user = {
                                "nickname": ''.join(random.choices(string.ascii_letters, k=5)),
                                "age": random.randint(18, 60)
                            }
                            users.append(user)
                        # 发起 POST 请求
                        r = self.client.post('/users', headers=header, json=users)
                        # 断言返回结果中的 "succ" 字段值为 "ok"
                        assert r.status_code == 200


class WebsiteUser(HttpUser):
    tasks = [TestLocust]


# 下面这些可以不用写
if __name__ == '__main__':
    # 使用locust命令行工具运行压力测试
    os.system('locust -f test.py --host="http://127.0.0.1:8090"')
