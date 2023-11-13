package com.example.testweb.util;

import lombok.Data;

@Data
public class Result<T> {
    /** 响应状态码 */
    private Long code;
    /** 响应消息 */
    private String msg;
    /** 响应数据 */
    private T data;


    /**
     * 响应成功结果
     * @param msg 响应消息
     * @param data 响应数据
     */
    public static<T> Result<T> ok(String msg, T data) {
        return ok(ResponseStatusEnum.SUCCESS.getCode(), msg, data);
    }

    /**
     * 响应成功结果
     * @param data 响应数据
     */
    public static<T> Result<T> ok(T data) {
        return ok(ResponseStatusEnum.SUCCESS.getCode(), ResponseStatusEnum.SUCCESS.getMsg(), data);
    }

    /**
     * 响应成功结果
     */
    public static<T> Result<T> ok() {
        return ok(ResponseStatusEnum.SUCCESS.getCode(), ResponseStatusEnum.SUCCESS.getMsg(), null);
    }

    /**
     * 响应成功结果
     * @param responseStatusEnum 成功类型的枚举类
     * @param data 响应数据
     */
    public static<T> Result<T> ok(ResponseStatusEnum responseStatusEnum, T data) {
        return ok(responseStatusEnum.getCode(), responseStatusEnum.getMsg(), data);
    }

    /**
     * 响应失败结果
     * @param msg 响应消息
     * @param data 响应数据
     */
    public static<T> Result<T> fail(String msg, T data) {
        return fail(ResponseStatusEnum.FAIL.getCode(), msg, data);
    }

    /**
     * 响应失败结果
     * @param data 响应数据
     */
    public static<T> Result<T> fail(T data) {
        return fail(ResponseStatusEnum.FAIL.getCode(), ResponseStatusEnum.FAIL.getMsg(), data);
    }

    /**
     * 响应失败结果
     */
    public static<T> Result<T> fail() {
        return fail(ResponseStatusEnum.FAIL.getCode(), ResponseStatusEnum.FAIL.getMsg(), null);
    }

    /**
     * 响应失败结果
     * @param responseStatusEnum 失败类型的枚举类
     * @param data 响应数据
     */
    public static<T> Result<T> fail(ResponseStatusEnum responseStatusEnum, T data) {
        return fail(responseStatusEnum.getCode(), responseStatusEnum.getMsg(), data);
    }

    private Result(Long code, String msg, T data) {
        this.code = code;
        this.msg = msg;
        this.data = data;
    }

    /**
     * 响应成功结果
     * @param code 响应状态码
     * @param msg 响应消息
     * @param data 响应数据
     */
    private static<T> Result<T> ok(Long code, String msg, T data) {
        return new Result<T>(code, msg, data);
    }

    /**
     * 响应失败结果
     * @param code 响应状态码
     * @param msg 响应消息
     * @param data 响应数据
     */
    private static<T> Result<T> fail(Long code, String msg, T data) {
        return new Result<T>(code, msg, data);
    }
}