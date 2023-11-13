-- 创建数据库test（如果不存在）
CREATE DATABASE IF NOT EXISTS test;
USE test;

-- 创建表user
CREATE TABLE IF NOT EXISTS user (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    nickname VARCHAR(50),
    age INT,
    class VARCHAR(50),
    student_id VARCHAR(50)
    );

-- 插入200条随机数据
INSERT INTO user (nickname, age, class, student_id)
SELECT
    CONCAT('User', LPAD(ROW_NUMBER() OVER(), 3, '0')) AS nickname,
    FLOOR(RAND() * 30) + 18 AS age,
    CONCAT('Class', FLOOR(RAND() * 5) + 1) AS class,
    CONCAT('S', LPAD(FLOOR(RAND() * 10000), 4, '0')) AS student_id
FROM
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) AS t1,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) AS t2,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) AS t3,
    (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) AS t4;

-- 查询插入的数据
SELECT * FROM user;