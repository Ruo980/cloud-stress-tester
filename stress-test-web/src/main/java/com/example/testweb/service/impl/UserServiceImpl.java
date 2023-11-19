package com.example.testweb.service.impl;

import com.example.testweb.dao.mapper.UserMapper;
import com.example.testweb.dao.pojo.User;
import com.example.testweb.service.UserService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.BoundHashOperations;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import com.fasterxml.jackson.databind.ObjectMapper; // 引入 Jackson ObjectMapper
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserMapper userMapper; // 会自动生成带有该属性的构造函数，这样注入是被推荐的

    private final StringRedisTemplate redisTemplate;

    private final ObjectMapper objectMapper = new ObjectMapper();

    private static final String SORTED_SET_NAME = "users_sorted_set";

    @Override
    public List<User> getUsers(int row) {
        return userMapper.selectUsersByRow(row);
    }

    @Override
    public void addUsers(List<User> users) {
        try {
            for (User user : users) {
                userMapper.insertUser(user);
            }
        } catch (Exception e) {
            throw new RuntimeException("插入用户失败", e);
        }
    }

    @Override
    public void addUser(User user) {
        userMapper.insertUser(user);
    }


    /**
     * 从 Redis 中获取前 row 行用户数据
     * @param row 要获取的行数
     * @return 包含用户数据的列表
     */
    public List<User> getUsersByRedis(int row) {
        // 使用 opsForZSet() 获取有序集合操作对象
        Set<String> userJsonSet = redisTemplate.opsForZSet().range(SORTED_SET_NAME, 0, row - 1);
        // 将 JSON 字符串转换为 User 对象并收集到列表中
        return userJsonSet.stream()
                .map(userJson -> jsonToUser(userJson))
                .collect(Collectors.toList());
    }

    /**
     * 将单个用户插入到 Redis 的有序集合中
     * @param user 要插入的单个用户
     */
    public void addUserByRedis(User user) {
        // 使用 opsForZSet() 将单个用户信息添加到有序集合中
        redisTemplate.opsForZSet().add(SORTED_SET_NAME, userToJson(user), user.getAge());
    }

    /**
     * 将用户集合插入到 Redis 的有序集合中
     * @param users 要插入的用户集合
     */
    public void addUsersByRedis(List<User> users) {
        // 遍历用户集合，使用 opsForZSet() 将用户信息添加到有序集合中
        for (User user : users) {
            redisTemplate.opsForZSet().add(SORTED_SET_NAME, userToJson(user), user.getAge());
        }
    }

    /**
     * 将 User 对象转换为 JSON 字符串
     * @param user 要转换的 User 对象
     * @return JSON 字符串
     */
    private String userToJson(User user) {
        try {
            return objectMapper.writeValueAsString(user);
        } catch (IOException e) {
            throw new RuntimeException("Failed to convert User to JSON", e);
        }
    }

    /**
     * 将 JSON 字符串转换为 User 对象
     * @param userJson JSON 字符串
     * @return User 对象
     */
    private User jsonToUser(String userJson) {
        try {
            return objectMapper.readValue(userJson, User.class);
        } catch (IOException e) {
            throw new RuntimeException("Failed to convert JSON to User", e);
        }
    }



}
