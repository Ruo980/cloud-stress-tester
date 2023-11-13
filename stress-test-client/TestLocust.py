import csv
import os
import random
import string

from locust import HttpUser, TaskSet, task


class TestLocust(TaskSet):
    """
    测试类:两个测试任务
    """

    @task(1)  # 参数表示执行次数，不写默认1次
    def user_query_message(self):
        """
        测试查询消息的任务。
        """
        # 读取 csv 文件数据集内数据进行压力测试
        with open('dataset/azurefunctions-accesses-2020.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过标题行
            for row in reader:
                if len(row) >= 11:  # 确保行中至少有11个值
                    blob_bytes = row[8]
                    read = row[9]
                    # 根据每行的数据来执行不同的请求操作
                    blog_bytes = float(blob_bytes)
                    num = round(blog_bytes / 100)
                    if num <= 0:
                        num = 1

                    if read == "True":
                        # 发起 GET 请求
                        header = {
                            'Content-Type': 'application/json;charset=UTF-8'
                        }
                        url = '/users-re' + '?row=' + str(num)
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
                        header = {
                            'Content-Type': 'application/json;charset=UTF-8'
                        }
                        r = self.client.post('/users-re', headers=header, json=users)
                        # 断言返回结果中的 "succ" 字段值为 "ok"
                        assert r.status_code == 200


class WebsiteUser(HttpUser):
    tasks = [TestLocust]
    min_wait = 500
    max_wait = 5000


# 下面这些可以不用写
if __name__ == '__main__':
    # 使用locust命令行工具运行压力测试
    os.system('locust -f TestLocust.py --host="http://127.0.0.1:8090"')
