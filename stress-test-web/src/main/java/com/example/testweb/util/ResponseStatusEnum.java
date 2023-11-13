package com.example.testweb.util;

import lombok.Getter;

@Getter
public enum ResponseStatusEnum {
    // 根据需要添加合适的code码
    FAIL(500L, "失败"),
    SUCCESS(200L, "成功");

    private final Long code;
    private final String msg;
    ResponseStatusEnum(Long code, String msg) {
        this.code = code;
        this.msg = msg;
    }

}