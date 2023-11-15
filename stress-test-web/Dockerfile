# 使用基础的 OpenJDK 镜像
FROM openjdk:17-jdk-alpine

# 设置工作目录
WORKDIR /app

# 复制项目的 JAR 文件到镜像中
COPY target/stress-test-web-1.0.0.jar stress-test-web-1.0.0.jar

# 暴露应用端口（仅仅做声明使用）
EXPOSE 8090

# 启动 Spring Boot 应用
CMD ["java", "-jar", "stress-test-web-1.0.0.jar"]