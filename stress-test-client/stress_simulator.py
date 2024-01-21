import csv
import time

import pandas as pd
from locust import HttpUser, task, TaskSet
# 请求脚本的编写宗旨就是：保证请求数量和数据大小。对于数据生成和读取能简化则简化，不要影响客户端发起请求的速率和性能。
# 通过固定数据量能够实现请求负载只和RPS有关而不是和数据大小有关。
# 多线程是并发的而不是并行的。设置多线程的目的是：一个用户发起请求后往往会等待响应才会发起第二个请求，但是如果请求过多可能就会堵塞在请求序列中，从而影响下一个请求的发起。
# 我们的思路是，先设置尽可能多的用户数量并发请求，来避免请求堵塞，从而验证本地客户端真正能够发起的总请求量（随着用户数量增多1秒内可能各用户请求数变小，但整体的请求量一定上去了（节省了请求序列等待时间））
# 这样我们实际就会测出一个主机的最大请求量，然后我们再规定用户数量100，确定每秒发起请求量的范围，再对请求量数据集进行归一化处理，使得每秒发起请求量在这个范围内。
# 这样我们本机能做到1秒内发起的请求量总数随着请求量数据集而发生变化。

# 定义post请求user-re接口的数据生成：50个用户
users_re = [
    {'nickname': 'ABCDE', 'age': 28},
    {'nickname': 'xyzXY', 'age': 42},
    {'nickname': 'LMNOP', 'age': 20},
    {'nickname': 'qrstU', 'age': 55},
    {'nickname': 'vwxyz', 'age': 36},
    {'nickname': 'FGHIJ', 'age': 48},
    {'nickname': 'klmno', 'age': 30},
    {'nickname': 'pqrst', 'age': 22},
    {'nickname': 'WXYZA', 'age': 40},
    {'nickname': 'ijklm', 'age': 33},
    {'nickname': 'UVWXY', 'age': 25},
    {'nickname': 'nopqr', 'age': 50},
    {'nickname': 'IJKLM', 'age': 18},
    {'nickname': 'DEFGH', 'age': 38},
    {'nickname': 'BCDEF', 'age': 45},
    {'nickname': 'uvwxY', 'age': 29},
    {'nickname': 'QRSTU', 'age': 32},
    {'nickname': 'ghijk', 'age': 52},
    {'nickname': 'opqrs', 'age': 21},
    {'nickname': 'lmnop', 'age': 44},
    {'nickname': 'WXYZA', 'age': 31},
    {'nickname': 'ijklm', 'age': 46},
    {'nickname': 'UVWXY', 'age': 27},
    {'nickname': 'nopqr', 'age': 35},
    {'nickname': 'IJKLM', 'age': 23},
    {'nickname': 'DEFGH', 'age': 39},
    {'nickname': 'BCDEF', 'age': 41},
    {'nickname': 'uvwxY', 'age': 53},
    {'nickname': 'QRSTU', 'age': 37},
    {'nickname': 'ghijk', 'age': 26},
    {'nickname': 'opqrs', 'age': 49},
    {'nickname': 'lmnop', 'age': 19},
    {'nickname': 'ABCDE', 'age': 47},
    {'nickname': 'xyzXY', 'age': 34},
    {'nickname': 'LMNOP', 'age': 24},
    {'nickname': 'qrstU', 'age': 51},
    {'nickname': 'vwxyz', 'age': 43},
    {'nickname': 'FGHIJ', 'age': 28},
    {'nickname': 'klmno', 'age': 37},
    {'nickname': 'pqrst', 'age': 22},
    {'nickname': 'WXYZA', 'age': 40},
    {'nickname': 'ijklm', 'age': 33},
    {'nickname': 'UVWXY', 'age': 55},
    {'nickname': 'nopqr', 'age': 50},
    {'nickname': 'IJKLM', 'age': 18},
    {'nickname': 'DEFGH', 'age': 38},
    {'nickname': 'BCDEF', 'age': 45},
    {'nickname': 'uvwxY', 'age': 29},
    {'nickname': 'QRSTU', 'age': 32},
    {'nickname': 'ghijk', 'age': 52},
    {'nickname': 'opqrs', 'age': 21},
    {'nickname': 'lmnop', 'age': 44}
]

# 定义post请求user接口的数据生成：30个用户
users = [
    {'nickname': 'ABCDE', 'age': 28},
    {'nickname': 'xyzXY', 'age': 42},
    {'nickname': 'LMNOP', 'age': 20},
    {'nickname': 'qrstU', 'age': 55},
    {'nickname': 'vwxyz', 'age': 36},
    {'nickname': 'FGHIJ', 'age': 48},
    {'nickname': 'klmno', 'age': 30},
    {'nickname': 'pqrst', 'age': 22},
    {'nickname': 'WXYZA', 'age': 40},
    {'nickname': 'ijklm', 'age': 33},
    {'nickname': 'UVWXY', 'age': 25},
    {'nickname': 'nopqr', 'age': 50},
    {'nickname': 'IJKLM', 'age': 18},
    {'nickname': 'DEFGH', 'age': 38},
    {'nickname': 'BCDEF', 'age': 45},
    {'nickname': 'uvwxY', 'age': 29},
    {'nickname': 'QRSTU', 'age': 32},
    {'nickname': 'ghijk', 'age': 52},
    {'nickname': 'opqrs', 'age': 21},
    {'nickname': 'lmnop', 'age': 44},
    {'nickname': 'WXYZA', 'age': 31},
    {'nickname': 'ijklm', 'age': 46},
    {'nickname': 'UVWXY', 'age': 27},
    {'nickname': 'nopqr', 'age': 35},
    {'nickname': 'IJKLM', 'age': 23},
    {'nickname': 'DEFGH', 'age': 39},
    {'nickname': 'BCDEF', 'age': 41},
    {'nickname': 'uvwxY', 'age': 53},
    {'nickname': 'QRSTU', 'age': 37},
    {'nickname': 'ghijk', 'age': 26}
]


# 任务类：定义一个用户的压测任务
class TaskLogic(TaskSet):

    def on_start(self):
        # 初始化一个标志，用于在 perform_request 方法中切换接口
        self.switch_interface = False

        # 初始化一个标志，用于在 perform_request 方法中交替执行 GET 和 POST
        self.perform_get = True

    @task
    def my_task(self):
        """
        定义一个用户的压测任务
        """
        # 读取请求量数据集，获取每5分钟的每秒请求量
        df=pd.read_csv("./dataset/request/requests-3-normalized.csv")
        count_values = df['count'].astype(int).tolist()
        for request_count in count_values:
            print(request_count)
            # 每秒发起request_count个请求，持续5分钟，也就是300次循环
            for _ in range(300):
                # 每秒发起request_count个请求，没有超过1秒则等待剩余时间；超过1秒则退出循环
                start_time = time.time()  # 记录循环开始时间
                print(start_time)
                i=0
                for _ in range(request_count):
                    i=i+1
                    # 根据每行各列的内容进行相应的请求
                    self.perform_request()
                    elapsed_time = time.time() - start_time
                    print(elapsed_time)
                    if elapsed_time > 1:
                        print("It has been 1 second and not all requests have been sent.")
                        print(i)
                        print()
                        print("Sent approx:", i, "requests in 1 second")
                        break
                print("Completed in one cycle")
                # 如果内部循环结束时还没超过1秒钟，等待剩余时间
                remaining_time = 1 - (time.time() - start_time)
                if remaining_time > 0:
                    print("The send request was completed within one second")
                    time.sleep(remaining_time)
            print("five minutes passed")

    # 发起 HTTP 请求，进行压力测试：根据请求的数据类型、读写方法和数据量来发送请求
    def perform_request(self):
        header = {'Content-Type': 'application/json;charset=UTF-8'}
        # 根据switch_interface的值请求不同的接口
        if self.switch_interface:
            if self.perform_get:
                # 发起 GET 请求到 users-re 接口
                url = '/users-re' + '?row=' + str(500)
                r = self.client.get(url, headers=header)
            else:
                # 发起 POST 请求到 users-re 接口
                r = self.client.post('/users-re', headers=header, json=users_re)
        else:
            if self.perform_get:
                # 发起 GET 请求到 users 接口
                url = '/users' + '?row=' + str(300)
                r = self.client.get(url, headers=header)
            else:
                # 发起 POST 请求到 users 接口
                r = self.client.post('/users', headers=header, json=users)
        if not self.switch_interface:
            self.perform_get = not self.perform_get
        self.switch_interface = not self.switch_interface


# 用户线程类：定义一个压测用户行为和任务
class MyUser(HttpUser):
    # wait between 3.0 and 10.5 seconds after each task
    # 我们这里用户只执行一次任务，因此不需要进行设置
    # wait_time = between(3.0, 10.5)

    tasks = [TaskLogic]  # 用户执行任务列表，这里只执行一个任务，执行完之后结束

    def on_stop(self):
        # 在用户执行完所有任务后输出信息
        print("OK")

# 下面代码注释，我们使用命令行工具运行脚本进行压力测试
# locust -f stress_simulator.py --host="http://127.0.0.1:8090"
# if __name__ == '__main__':
# 使用locust命令行工具运行压力测试
# os.system('locust -f stress_simulator.py --host="http://127.0.0.1:8090"')


# 发起的请求目标为：http://172.31.234.111:30341