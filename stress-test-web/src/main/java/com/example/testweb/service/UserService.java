package com.example.testweb.service;

import com.example.testweb.dao.pojo.User;

import java.util.List;

/**
 * 用户管理的服务接口。
 */
public interface UserService {

    /**
     * MySQL:检索到指定行数的用户列表。
     *
     * @param row 要检索的行数。
     * @return 用户列表。
     */
    List<User> getUsers(int row);

    /**
     * MySQL:添加用户列表。
     *
     * @param users 要添加的用户列表。
     */
    void addUsers(List<User> users);

    /**
     * MySQL:添加单个用户。
     *
     * @param user 要添加的用户。
     */
    void addUser(User user);

    /**
     * Redis:中检索指定行数的用户列表。
     *
     * @param row 要检索的行数。
     * @return 从Redis中获取的用户列表。
     */
    List<User> getUsersByRedis(int row);

    /**
     * Redis: 将单个用户添加到 Redis。
     *
     * @param user User 要添加到 Redis 中的用户
     */
    void addUserByRedis(User user);

    /**
     * Redis:将用户列表添加到 Redis。
     *
     * @param users 要添加到 Redis 的用户列表。
     */
    void addUsersByRedis(List<User> users);
}
