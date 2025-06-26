package com.huy.husci;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class HusciApplication {
	public static void main(String[] args) {
		SpringApplication.run(HusciApplication.class, args);
	}

}
