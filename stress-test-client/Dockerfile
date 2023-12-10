# 使用官方的 Python 镜像作为基础镜像
FROM python:3.11.5

# 设置工作目录：在容器根目录中创建工作文件夹/app
WORKDIR /app

# 复制项目文件到容器指定的工作目录
COPY . /app

# 安装项目依赖
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# 暴露 Locust Web 界面
EXPOSE 8089

# 执行 Locust 命令启动项目
CMD ["venv/bin/locust", "-f", "stress_simulator.py", "--host=http://127.0.0.1:8090"]