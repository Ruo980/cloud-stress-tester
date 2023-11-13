package com.example.testweb.controller;

import com.example.testweb.dao.pojo.User;
import com.example.testweb.service.UserService;
import com.example.testweb.util.Result;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class TestController {

    private static final Logger logger = LoggerFactory.getLogger(TestController.class);

    private final UserService userService;

    @GetMapping("/test")
    @ResponseBody
    public String test() {
        // 用于测试的接口，返回字符串 "test"
        return "test";
    }

    /**
     * MySQL: 查询前 row 行的 MySQL 数据库中的用户数据
     *
     * @param row int
     * @return Result
     */
    @GetMapping("/users")
    @ResponseBody
    public Result<List<User>> getUsers(@RequestParam("row") int row) {
        logger.info("Row: {}", row);
        logger.info("Start fetching users");
        List<User> users = null;
        try {
            users = userService.getUsers(row);
            logger.info("Fetching users successful");
            return Result.ok(users);
        } catch (Exception e) {
            logger.error("Error fetching users: {}", e.getMessage());
            return Result.fail(e.getMessage(), users);
        }
    }

    /**
     * MySQL: 将提交的一个用户数据存入到 MySQL 中去。
     *
     * @param user User
     * @return Result
     */
    @PostMapping("/user")
    @ResponseBody
    public Result<Void> addUser(@RequestBody User user) {
        logger.info("Received user: {}", user);
        logger.info("Start inserting user");
        try {
            userService.addUser(user);
            logger.info("Inserting user successful");
            return Result.ok();
        } catch (Exception e) {
            logger.error("Error inserting user: {}", e.getMessage());
            return Result.fail(e.getMessage(), null);
        }
    }

    /**
     * MySQL: 提交大量用户数据进行存储
     *
     * @param users List
     * @return Result
     */
    @PostMapping("/users")
    @ResponseBody
    public Result<Void> addUsers(@RequestBody List<User> users) {
        logger.info("Received users: {}", users);
        logger.info("Start inserting users");
        try {
            userService.addUsers(users);
            logger.info("Inserting users successful");
            return Result.ok();
        } catch (Exception e) {
            logger.error("Error inserting users: {}", e.getMessage());
            return Result.fail(e.getMessage(), null);
        }
    }

    /**
     * Redis: 查询前 row 行的 Redis 数据库中的用户数据
     *
     * @param row int
     * @return Result
     */
    @GetMapping("/users-re")
    @ResponseBody
    public Result<List<User>> getUsersByRedis(@RequestParam("row") int row) {
        logger.info("Row: {}", row);
        logger.info("Start fetching users from Redis");
        List<User> users = null;
        try {
            users = userService.getUsersByRedis(row);
            logger.info("Fetching users successful from Redis");
            return Result.ok(users);
        } catch (Exception e) {
            logger.error("Error fetching users from Redis: {}", e.getMessage());
            return Result.fail(e.getMessage(), users);
        }
    }

    /**
     * Redis: 将提交的一个用户数据存入到 Redis 中去。
     *
     * @param user User
     * @return Result
     */
    @PostMapping("/user-re")
    @ResponseBody
    public Result<Void> addUserByRedis(@RequestBody User user) {
        logger.info("Received user from Redis: {}", user);
        logger.info("Start inserting user from Redis");
        try {
            userService.addUserByRedis(user);
            logger.info("Inserting user successful from Redis");
            return Result.ok();
        } catch (Exception e) {
            logger.error("Error inserting user from Redis: {}", e.getMessage());
            return Result.fail(e.getMessage(), null);
        }
    }

    /**
     * Redis: 提交大量用户数据进行存储
     *
     * @param users List
     * @return Result
     */
    @PostMapping("/users-re")
    @ResponseBody
    public Result<Void> addUsersByRedis(@RequestBody List<User> users) {
        logger.info("Received users from Redis: {}", users);
        logger.info("Start inserting users from Redis");
        try {
            userService.addUsersByRedis(users);
            logger.info("Inserting users successful from Redis");
            return Result.ok();
        } catch (Exception e) {
            logger.error("Error inserting users from Redis: {}", e.getMessage());
            return Result.fail(e.getMessage(), null);
        }
    }
}
