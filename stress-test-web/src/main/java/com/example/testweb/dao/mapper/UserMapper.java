package com.example.testweb.dao.mapper;

import com.example.testweb.dao.pojo.User;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;


public interface UserMapper {

    /**
     * User 表查询：遍历表中所有数据
     *
     * @return List
     */
    List<User> selectUsersByRow(int row);

    /**
     * User 表插入：将指定数据插入表中
     *
     * @param user User
     * @return int
     */
    int insertUser(User user);

    /**
     * User 表插入：将大规模的数据批量插入表中
     *
     * @param users List<User>
     * @return int
     */
    int batchInsertUsers(List<User> users);
}
