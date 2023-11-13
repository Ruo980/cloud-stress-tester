import redis
import json
import faker

# 初始化 Faker
fake = faker.Faker()

# 初始化 Redis 连接
redis_host = '127.0.0.1'  # Redis 主机地址
redis_port = 6379  # Redis 端口号
redis_db = 0  # Redis 数据库索引
redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

# 有序集合名称
sorted_set_name = 'users_sorted_set'

def insert_users_to_redis(user_list):
    """
    插入用户集合到 Redis 有序集合中
    """
    for user in user_list:
        redis_conn.zadd(sorted_set_name, {json.dumps(user): user['age']})

def query_users_by_row(row):
    """
    查询前 row 行用户数据
    """
    result = []
    # ZRANGE 返回有序集中，指定区间内的成员
    users = redis_conn.zrange(sorted_set_name, 0, row - 1)
    for user_json in users:
        user = json.loads(user_json)
        result.append(user)
    return result

# 生成用户数据
users_to_insert = []
for _ in range(600):
    user = {
        'nickname': fake.user_name(),
        'age': fake.random_int(min=18, max=60)
    }
    users_to_insert.append(user)

# 测试脚本执行情况：

# 插入用户数据
insert_users_to_redis(users_to_insert)

# 查询前 10 行数据
result = query_users_by_row(10)
print("前 10 行数据：", result)
