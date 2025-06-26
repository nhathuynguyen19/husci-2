package com.huy.husci.response;

public enum ApiResponseCode {
    SUCCESS(1, "success"),
    FAILED(0, "failed");

    private Integer code;
    private String message;

    ApiResponseCode(Integer code, String message) {
        this.code = code;
        this.message = message;
    }

    public Integer getCode() {
        return this.code;
    }

    public String getMessage() {
        return this.message;
    }

    public static String getMessageByName(String name) {
        for (ApiResponseCode item : ApiResponseCode.values()) {
            if (name.equals(item.name())) {
                return item.message;
            }
        }
        return null;
    }

    public static Integer getCodeByName(String name) {
        for (ApiResponseCode item : ApiResponseCode.values()) {
            if (name.equals(item.name())) {
                return item.code;
            }
        }
        return null;
    }

    @Override
    public String toString() {
        return this.name();
    }
}
