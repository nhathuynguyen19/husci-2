package com.huy.husci.modules;

import com.huy.husci.model.Announcement;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Objects;

public class Ums {

    public static Document fetch() {
        String url = "https://ums.husc.edu.vn";
        int retries = 10;
        while (retries-- > 0) {
            try {
                Connection.Response response = Jsoup.connect(url)
                        .timeout(10_000)
                        .userAgent("Mozilla/5.0")
                        .method(Connection.Method.GET)
                        .execute();
                return response.parse();
            } catch (IOException e) {
                System.err.println("Fetch thất bại (còn " + retries + " lần thử): " + e.getMessage());
                try {
                    Thread.sleep(1000); // đợi trước khi thử lại
                } catch (InterruptedException ignored) {}
            }
        }
        throw new RuntimeException("Không thể fetch sau nhiều lần thử");
    }

    public static String cleanId(String input) {
        // chuyen ve chu thuong
        String lower = input.toLowerCase();
        // thay khoang trang thanh dau -
        String replaced = lower.replaceAll("\\s+", "-");
        // xoa tat ca ky tu khong phai a-z 0-9
        String clean = replaced.replaceAll("[^a-z0-9-]", "");
        // gộp -- lại thành -
        clean = clean.replaceAll("-{2,}", "-");
        // loai dau - dau hoac cuoi neu co
        clean = clean.replaceAll("^-+", "").replaceAll("-+$", "");
        return clean;
    }

    public static List<Announcement> fetchAnnouncementsOnPage() {
        List<Announcement> announcements = new ArrayList<>();
        try {
            Document document = fetch();
            Element element = document.selectFirst("div.container-fluid");
            Elements elements = new Elements();
            if (element != null) {
                elements = element.select("div > div");
            }

            for (Element e : elements) {
                String id;
                String title;
                String content;
                String url;
                Date dateCreate;

                id = cleanId(Objects.requireNonNull(e.selectFirst("div > p > a")).attr("href"));
                title = e.select("div > p > a").text();
                content = e.select("div > p").get(1).text();
                url = "https://ums.husc.edu.vn/" + e.select("div > p > a").attr("href");
                dateCreate = DateUtils.parseVietnamTimeToDate(e.select("div > p > small").text());

                Announcement announcement = new Announcement(id, title, content, url, dateCreate);
                announcements.add(announcement);
            }
            return announcements;
        } catch (Exception e) {
            System.err.println("Lỗi khi lấy thông báo từ web" + e.getMessage());
        }
        return announcements;
    }
}
