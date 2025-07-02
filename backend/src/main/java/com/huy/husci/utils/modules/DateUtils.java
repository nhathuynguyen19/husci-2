package com.huy.husci.utils.modules;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Date;

public class DateUtils {
    public static Date parseVietnamTimeToDate(String input) {
        String cleaned = input.replaceAll("[\\[\\]]", ""); // xóa dấu []
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");
        LocalDateTime dateTime = LocalDateTime.parse(cleaned, formatter);
        return Date.from(dateTime.atZone(ZoneId.of("Asia/Ho_Chi_Minh")).toInstant());
    }
}
