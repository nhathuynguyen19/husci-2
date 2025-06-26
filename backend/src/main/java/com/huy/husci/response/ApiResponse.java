package com.huy.husci.response;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.io.Serializable;

@JsonIgnoreProperties(ignoreUnknown = true)
public class ApiResponse implements Serializable {
    private Integer code;
    private String msg;
    private Object data;

    public ApiResponse() {}

    public ApiResponse(Integer code, String msg, Object data) {
        this.code = code;
        this.msg = msg;
        this.data = data;
    }

    public Integer getCode() {
        return code;
    }

    public void setCode(Integer code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }

    public static ApiResponse success() {
        ApiResponse result = new ApiResponse();
        result.setResultCode(ApiResponseCode.SUCCESS);
        return result;
    }

    public static ApiResponse success(Object data) {
        ApiResponse result = new ApiResponse();
        result.setResultCode(ApiResponseCode.SUCCESS);
        result.setData(data);
        return result;
    }

    public static ApiResponse failMessage(String message) {
        ApiResponse result = new ApiResponse();
        result.setCode(ApiResponseCode.FAILED.getCode());
        result.setMsg(message);
        return result;
    }

    private void setResultCode(ApiResponseCode apiResponseCode) {
        this.code = apiResponseCode.getCode();
        this.msg = apiResponseCode.getMessage();
    }

}
