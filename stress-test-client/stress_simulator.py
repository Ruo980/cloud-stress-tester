import csv
import os
import random
import string
from locust import HttpUser, TaskSet, task, constant, between


class TestLocust(TaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requests_iterator = iter(self.read_requests_per_interval())
        self.current_requests = next(self.requests_iterator, None)

    def read_requests_per_interval(self):
        """
        读取下一个周期应该发起的请求数
        :return:
        """
        with open('./dataset/request_per_interval.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                yield int(row[0])

    def read_data_file(self, num_rows):
        """
        读取num_rows行数的请求方式和数据
        :param num_rows:
        :return:
        """
        data = []
        with open('./dataset/sorted_azurefunctions-accesses-2020-svc.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for _ in range(num_rows):
                row = next(reader, None)
                if row is not None:
                    data.append(row)
        return data

    @task(1)
    def user_query_message(self):
        """
        用户执行测试任务：周期性的发起不同个数的请求。一个周期内的请求个数由数据集request_per_interval.csv决定，而具体每行的请求方式和数据则由sorted_azurefunctions-accesses-2020-svc.csv决定
        :return:
        """
        if self.current_requests is not None:
            num_rows = self.current_requests
            data = self.read_data_file(num_rows)

            for current_row in data:
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

            # 等待2秒:用户发起一次请求之后的等待时间
            self.wait()

    def on_start(self):
        # 在开始时，设置迭代器的起始位置
        self.requests_iterator = iter(self.read_requests_per_interval())

    def on_stop(self):
        # 当停止时，做一些清理工作
        pass


class WebsiteUser(HttpUser):
    """
    用户线程类：
    指定一个用户的测试任务和每个周期内的等待时间
    """
    tasks = [TestLocust]
    wait_time = between(1, 3)  # 设置用户执行任务之间的等待时间范围


# 下面这些可以不用写
if __name__ == '__main__':
    # 使用locust命令行工具运行压力测试
    os.system('locust -f stress_simulator.py --host="http://127.0.0.1:8090"')
