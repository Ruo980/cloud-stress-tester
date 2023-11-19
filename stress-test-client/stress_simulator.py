import csv
import os
import random
import string
from locust import HttpUser, TaskSet, task, constant, between


def generate_random_users(num):
    users = []
    for _ in range(num):
        user = {
            "nickname": ''.join(random.choices(string.ascii_letters, k=5)),
            "age": random.randint(18, 60)
        }
        users.append(user)
    return users


# 由于数据集非常巨大，一次性读取并操作是不可行的，因此考虑使用游标的方式来逐行读取数据，边读变发送请求
def read_requests_per_interval():
    """
    构建请求量生成器函数：返回每个周期的请求量用于发起请求行数的读取
    :return:
    """
    with open('dataset/request_per_interval.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for row in reader:
            yield int(row[0])  # 将该函数转换为生成器函数，逐行读取而不是一次性加载。每次调用生成器的next()函数就会到达下一行并暂停


def read_data_file(num_rows):
    """
    构建请求生成器函数：借助游标，每次读取文件的一行数据然后暂停
    :param num_rows:
    :return:
    """
    with open('dataset/sorted_azurefunctions-accesses-2020-svc.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for _ in range(num_rows):
            for row in reader:
                yield row


def read_data_rows(iterator, num_rows):
    """
    从请求生成器函数中读取指定数量的行
    :param iterator: 行迭代器
    :param num_rows: 需要读取的行数
    :return: 读取到的数据列表
    """
    data = []
    for _ in range(num_rows):
        row = next(iterator, None)
        if row is not None:
            data.append(row)
    return data


class TestLocust(TaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 生成一个迭代器：利用生成器函数来逐行读取CSV文件中的请求数
        self.requests_iterator = iter(read_requests_per_interval())
        # 每次使用next()函数来从迭代器中获取下一行的数据
        self.current_requests = next(self.requests_iterator, None)

        # 生成一个迭代器：利用生成器函数来逐行读取CSV文件中的请求数据
        self.data_iterator = iter(read_data_file(10000))
        self.current_data = next(self.data_iterator, None)

    def on_start(self):
        # 每次用户开始测试时，设置request_per_interval.csv迭代器的起始位置
        self.requests_iterator = iter(read_requests_per_interval())
        # 每次用户开始测试时，设置sorted_azurefunctions-accesses-2020-svc.csv迭代器的起始位置
        self.current_requests = next(self.requests_iterator, None)

    def perform_request_redis(self, read, num):
        """
        执行请求操作：只对Redis发起读写请求
        :param read:
        :param num:
        :return:
        """
        header = {'Content-Type': 'application/json;charset=UTF-8'}
        # 该类型操作 Redis 数据库
        if read == "True":
            # 发起 GET 请求
            url = '/users-re' + '?row=' + str(num)
            r = self.client.get(url, headers=header)
            # 断言返回结果中的 "succ" 字段值为 "ok"
            assert r.status_code == 200
        else:
            # 发起 POST 请求
            r = self.client.post('/users-re', headers=header, json=generate_random_users(num))
        header = {'Content-Type': 'application/json;charset=UTF-8'}

    def perform_request_mysql(self, read, num):
        """
        执行请求操作：只对MySQL发起读写请求
        :param read:
        :param num:
        :return:
        """
        header = {'Content-Type': 'application/json;charset=UTF-8'}
        # 该类型操作 MySQL 数据库
        if read == "True":
            # 发起 GET 请求
            url = '/users' + '?row=' + str(num)
            r = self.client.get(url, headers=header)
            # 断言返回结果中的 "succ" 字段值为 "ok"
            assert r.status_code == 200
        else:
            # 发起 POST 请求
            r = self.client.post('/users', headers=header, json=generate_random_users(num))
        header = {'Content-Type': 'application/json;charset=UTF-8'}

    @task(1)
    def user_query_message(self):
        """
        用户执行测试任务：一个测试任务包含多个周期性请求，即每秒应该有不同的请求速率。
        总请求率/一个周期时间(等待时间)就是一个请求速率的值。
        一个周期内的请求个数由数据集request_per_interval.csv决定，而具体每行的请求方式和数据则由sorted_azurefunctions-accesses-2020-svc.csv决定
        某个周期应该发送request_per_interval.csv某行决定的请求数，在这个周期内发送指定行数的sorted_azurefunctions-accesses-2020-svc.csv中的请求
        :return:
        """
        print("一次测试执行：")
        if self.current_requests is not None:
            # 当前周期内的请求数
            num_rows = self.current_requests
            # 读取num_rows行的请求方式和数据
            data = read_data_file(num_rows)
            for current_row in data:
                blob_type = current_row[6]
                blob_bytes = current_row[8]
                read = current_row[9]
                blog_bytes = float(blob_bytes)
                # 获取数据量
                num = round(blog_bytes / 1000)
                if num <= 0:
                    num = 1
                # 发送请求，进行压力测试：根据请求的数据类型、读写方法和数据量来发送请求，我们可以选择对Redis或MySQL进行操作请求
                self.perform_request_mysql(read, num)
            # 等待2秒:用户发起一次请求之后的等待时间
            self.wait()
            self.current_requests = next(self.requests_iterator, None)  # 从迭代器中获取下一行的数据，确定下一个周期的请求发送数量


class WebsiteUser(HttpUser):
    """
    用户线程类：
    指定一个用户的测试任务和每个周期内的等待时间
    """
    tasks = [TestLocust]
    wait_time = between(6, 10)  # 设置用户执行任务之间的等待时间范围


# 下面这些可以不用写
if __name__ == '__main__':
    # 使用locust命令行工具运行压力测试
    os.system('locust -f stress_simulator.py --host="http://127.0.0.1:8090"')
