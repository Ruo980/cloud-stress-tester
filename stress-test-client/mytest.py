import time

import requests

url = "http://192.168.192.130/"
counter = 0

while True:
    counter += 1
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Request #{counter} to {url} successful")
        else:
            print(f"Request #{counter} to {url} failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Request #{counter} to {url} failed: {e}")
    # 每隔100毫秒发起一次请求
    time.sleep(0.1)
