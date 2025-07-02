package com.huy.husci.utils.modules;

import lombok.Getter;
import lombok.Setter;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import com.huy.husci.repository.entity.Student;

import java.io.IOException;
import java.util.Map;

@Getter
@Setter
public class WebSession {
    private String id;
    private String requestVerificationToken;
    private Map<String, String> sessionCookies;

    public WebSession(Student student) {
        this.id = student.getId();
        boolean loggedIn = false;
        int retries = 10;

        while(!loggedIn && retries-- > 0) {
            try {
                this.login(student);
                loggedIn = true;
            } catch (Exception e) {
                System.err.println("Login thất bại (còn " + retries + " lần thử): " + e.getMessage());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException ignored) {

                }
            }
        }

        if (!loggedIn) {
            System.err.println("Không thể loggin sau nhiều lần thử, tạo session thất bại cho: " + student.getId());
        }
    }

    public void fetchLoginPage() throws IOException {
        String url = "https://student.husc.edu.vn/Account/Login";
        Connection.Response response = Jsoup.connect(url)
                .method(Connection.Method.GET)
                .timeout(10000)
                .execute();

        this.sessionCookies = response.cookies();
        Document loginPage = response.parse();
        Element inputElement = loginPage.selectFirst("input[name=__RequestVerificationToken]");
        if (inputElement != null) {
            this.requestVerificationToken = inputElement.attr("value");
        } else {
            throw new RuntimeException("Không tìm thấy __RequestVerificationToken");
        }
    }

    public void login(Student student) throws IOException {
        fetchLoginPage();

        if (this.requestVerificationToken == null) {
            throw new RuntimeException("Token login null, không thể login");
        }

        String url = "https://student.husc.edu.vn/Account/Login";
        Connection.Response response = Jsoup.connect(url)
                .method(Connection.Method.POST)
                .timeout(10000)
                .data("loginID", student.getId())
                .data("password", student.getPassword())
                .data("__RequestVerificationToken", this.requestVerificationToken)
                .cookies(this.sessionCookies)
                .execute();
        this.sessionCookies = response.cookies();
    }

    public Document fetch(String url) {
        try {
            Connection.Response response = Jsoup.connect(url)
                    .timeout(10000)
                    .cookies(this.sessionCookies)
                    .method(Connection.Method.GET)
                    .execute();
            Document document = response.parse();
            this.sessionCookies = response.cookies();
            return document;
        } catch (IOException e) {
            System.err.println("Lỗi khi fetch: " + url + " -> " + e.getMessage());
            return null;
        }
    }

    public String fetchStudentName() {
        Document document = fetch("https://student.husc.edu.vn/News");
        if (document != null) {
            return document.select("div.hitec-information > h5").text();
        }
        return null;
    }
}
