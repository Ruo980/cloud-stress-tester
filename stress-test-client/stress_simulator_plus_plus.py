import csv
import os
import random
import string
import time

from locust import HttpUser, task, TaskSet


# 读取请求量数据集
def read_request_counts():
    with open('./dataset/request_per_day_hour.csv', 'r') as request_csvfile:
        csvreader = csv.reader(request_csvfile)
        # 跳过表头
        header = next(csvreader, None)
        for request_row in csvreader:
            count = int(request_row[2])  # 读取第三列：count 值
            # 指定生成器的生成内容：每次调用父函数时返回一个 count 请求量
            yield count


# 读取请求内容数据集
def read_azure_data(count):
    with open('dataset/sorted_azurefunctions-accesses-2020.csv', 'r') as azure_csvfile:
        csvreader = csv.reader(azure_csvfile)
        # 跳过表头
        header = next(csvreader, None)
        for _ in range(count):
            # 按照文件指针，接着上一次读取的位置继续读取
            azure_data_row = next(csvreader, None)
            if azure_data_row:
                yield azure_data_row


# 生成post请求的数据:用户类作为数据体
def generate_random_users(num):
    users = []
    for _ in range(num):
        user = {
            "nickname": ''.join(random.choices(string.ascii_letters, k=5)),
            "age": random.randint(18, 60)
        }
        users.append(user)
    return users


# 任务类：定义一个用户的压测任务
class TaskLogic(TaskSet):

    @task
    def my_task(self):
        """
        定义一个用户的压测任务:
            用户同时操作request_per_day_hour.csv和sorted_azurefunctions-accesses-2020.csv两个数据集,前者规定了一次发起的请求量，后者规定了请求的内容和形式。
            用户任务类一边读取request_per_day_hour.csv确定每次发起的请求量，然后再读取sorted_azurefunctions-accesses-2020.csv的指定行数。之后根据每行的内容发起不同的http请求。
        :return:
        """
        # 生成一个生成器：读取 request_per_day_hour.csv 中的请求量
        request_counts = read_request_counts()

        # 迭代生成器：读取相应数量的 sorted_azurefunctions-accesses-2020.csv 行数并发起请求
        for request_count in request_counts:
            print(request_count)
            start_time = time.time()  # 记录循环开始时间
            for azure_data_row in read_azure_data(request_count):
                # 根据每行各列的内容进行相应的请求
                blob_type = azure_data_row[6]
                blob_bytes = azure_data_row[8]
                read = azure_data_row[9]
                blog_bytes = float(blob_bytes)
                # 获取数据量
                num = round(blog_bytes / 1000)
                if num <= 0:
                    num = 1
                # 发起 HTTP 请求，进行压力测试：根据请求的数据类型、读写方法和数据量来发送请求
                self.perform_request(blob_type, read, num)

                # 检查是否超过5分钟
                #elapsed_time = time.time() - start_time
                #if elapsed_time > 300:  # 5分钟 = 300秒
                   #print("已超过5分钟，退出循环")
                    #break

            print("一个周期执行完成")
            # 如果内部循环结束时还没超过5分钟，等待剩余时间
            remaining_time = time.time() - start_time
            print("大致花费时间为：", remaining_time)
            #remaining_time = 300 - (time.time() - start_time)
            #if remaining_time > 0:
                #print(f"等待剩余时间 {remaining_time} 秒")
                #time.sleep(remaining_time)

    # 发起 HTTP 请求，进行压力测试：根据请求的数据类型、读写方法和数据量来发送请求
    def perform_request(self, blob_type, read, num):
        """
        关于数据请求处理大致需要注意：
        - 大规模的数据存入时不能使用redis（内存爆炸）
        - 大规模的数据读取使用redis可以加快响应速度

        设计原则：
        - Redis进行规模以上数据的读取；
        - MySQL进行规模以上数据的存储。
        因此Redis的初始数据应该要尽量大来防止读取数据缺失，MySQL初始数据应该尽量小来方便存储。

        设计分类：
        根据上面的blob_type的分类和前面的设计原则做出如下分类：
        1. 大量的数据请求：视为复杂操作，从 MySQL 数据库中读取数据
        2. 少量的数据请求：视为简单操作，从 Redis 数据库中读取数据

        blob_type的类型大致有(数据大小，数量多少)：
        两个个数据类型是直接按照数据库类型进行划分的（负载均衡）：
        - BlockBlob/（每次请求的数据量可大可小，样本总数量多，使用Redis）
        - BlockBlob/application/octet-stream（每次请求的数据量可大可小，样本总数量多，使用MySQL）
        其他数据类型则按照读写规则进行划分：
        - BlockBlob/application/zip（每次请求的数据量大，样本总数量少）
        - BlockBlob/application/x-zip-compressed（每次请求的数据量大，样本总数量少）
        - BlockBlob/application/json(中等数据)
        - BlockBlob/application/pdf（大数据）
        杂类都使用Redis进行操作：
        - BlockBlob/image/jpeg（小，少，Redis）
        - BlockBlob/image/png（小，少，Redis）
        - BlockBlob/text/plain（小，少，Redis）
        - BlockBlob/text/csv（小，少，Redis）
        - BlockBlob/text/html（小，少，Redis）
        - other
        """
        header = {'Content-Type': 'application/json;charset=UTF-8'}
        # 根据每行的数据类型进行不同的操作
        if blob_type == 'BlockBlob/':
            # 该类型操作 Redis 数据库
            if read == "True":
                # 发起 GET 请求
                url = '/users-re' + '?row=' + str(num)
                #print("Redis数据库发起请求:/users-re?row=" + str(num))
                r = self.client.get(url, headers=header)
            else:
                #print("Redis数据库发起post请求:/users-re")
                # 发起 POST 请求
                r = self.client.post('/users-re', headers=header, json=generate_random_users(num))
        elif blob_type == 'BlockBlob/application/octet-stream':
            # 操作 MySQL 数据库
            if read == "True":
                # 发起 GET 请求
                url = '/users' + '?row=' + str(num)
                #print("MySQL 数据库发起请求:/users-re?row=" + str(num))
                r = self.client.get(url, headers=header)
            else:
                # 发起 POST 请求:如果是插入太多数据就考虑用Redis吧
                if num > 2000:
                    r = self.client.post('/users-re', headers=header, json=generate_random_users(num))
                #print("MySQL 数据库发起post请求:/users-re")
                r = self.client.post('/users', headers=header, json=generate_random_users(num))
        elif blob_type == 'BlockBlob/application/zip' or blob_type == 'BlockBlob/application/x-zip-compressed' or blob_type == 'BlockBlob/application/json' or blob_type == 'BlockBlob/application/pdf':
            # 规模及数据量都在中等的范围内，按照读存方式进行请求发送
            if read == "True":
                # 发起 GET 请求
                url = '/users-re' + '?row=' + str(num)
                #print("Redis数据库发起请求:/users-re?row=" + str(num))
                r = self.client.get(url, headers=header)
            else:
                # 发起 POST 请求:如果是插入太多数据就考虑用Redis吧
                if num > 2000:
                    #print("MySQL数据库发起post请求:/users-re")
                    r = self.client.post('/users-re', headers=header, json=generate_random_users(num))
                #print("MySQL数据库发起post请求:/users")
                r = self.client.post('/users', headers=header, json=generate_random_users(num))
        else:
            # 其他所有格式都使用Redis：主要测量web应用对Redis的性能
            if read == "True":
                # 发起 GET 请求
                url = '/users-re' + '?row=' + str(num)
                #print("Redis数据库发起请求:/users-re?row=" + str(num))
                r = self.client.get(url, headers=header)
                # 断言返回结果中的 "succ" 字段值为 "ok"
                # assert r.status_code == 200
            else:
                #print("Redis数据库发起post请求:/users-re")
                # 发起 POST 请求
                r = self.client.post('/users-re', headers=header, json=generate_random_users(num))


# 用户线程类：定义一个压测用户行为和任务
class MyUser(HttpUser):
    # wait between 3.0 and 10.5 seconds after each task
    # 我们这里用户只执行一次任务，因此不需要进行设置
    # wait_time = between(3.0, 10.5)

    tasks = [TaskLogic]  # 用户执行任务列表，这里只执行一个任务，执行完之后结束

    def on_stop(self):
        # 在用户执行完所有任务后输出信息
        print("一个用户的任务执行完成，该用户线程停止：OK")


if __name__ == '__main__':
    # 使用locust命令行工具运行压力测试
    os.system('locust -f stress_simulator_plus_plus.py --host="http://127.0.0.1:8090"')
