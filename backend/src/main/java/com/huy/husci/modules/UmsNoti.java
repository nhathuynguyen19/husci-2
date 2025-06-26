package com.huy.husci.modules;

import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import java.io.IOException;

public class UmsNoti {

    public Document fetch(String url) {
        try {
            Connection.Response response = Jsoup.connect(url)
                    .method(Connection.Method.GET)
                    .timeout(10000)
                    .execute();
            return response.parse();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
