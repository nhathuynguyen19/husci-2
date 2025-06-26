package com.huy.husci.modules;

import com.huy.husci.model.Student;
import lombok.Getter;
import lombok.Setter;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

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
        this.login(student);
    }

    public void fetchLoginPage() {
        try {
            String url = "https://student.husc.edu.vn/Account/Login";
            Connection.Response response = Jsoup.connect(url)
                    .method(Connection.Method.GET)
                    .execute();
            this.sessionCookies = response.cookies();
            Document loginPage = response.parse();
            Element inputElement = loginPage.selectFirst("input[name=__RequestVerificationToken]");
            if (inputElement != null) {
                this.requestVerificationToken = inputElement.attr("value");
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void login(Student student) {
        try {
            String url = "https://student.husc.edu.vn/Account/Login";
            fetchLoginPage();
            Connection.Response response = Jsoup.connect(url)
                    .method(Connection.Method.POST)
                    .data("loginID", student.getId())
                    .data("password", student.getPassword())
                    .data("__RequestVerificationToken", this.requestVerificationToken)
                    .cookies(this.sessionCookies)
                    .execute();
            this.sessionCookies = response.cookies();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public Document fetch(String url) {
        try {
            Connection.Response response = Jsoup.connect(url)
                    .cookies(this.sessionCookies)
                    .method(Connection.Method.GET)
                    .execute();
            Document document = response.parse();
            this.sessionCookies = response.cookies();
            return document;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public String fetchStudentName() {
        try {
            String url = "https://student.husc.edu.vn/News";
            Document document = fetch(url);
            return document.select("div.hitec-information > h5").text();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
