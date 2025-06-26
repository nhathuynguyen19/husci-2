package com.huy.husci;

import com.huy.husci.model.Student;
import com.huy.husci.modules.WebSession;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.IOException;

@SpringBootApplication
public class HusciApplication {
	public static void main(String[] args) {
		SpringApplication.run(HusciApplication.class, args);
//		try {
//			Connection.Response response = Jsoup.connect("https://ums.husc.edu.vn/")
//					.method(Connection.Method.GET)
//					.execute();
//			System.out.println(response.parse().select("div.container-fluid > div"));
//		} catch (IOException e) {
//			throw new RuntimeException(e);
//		}
	}
}
