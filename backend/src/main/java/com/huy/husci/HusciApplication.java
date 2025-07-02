package com.huy.husci;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.scheduling.annotation.EnableScheduling;

import com.huy.husci.utils.modules.DotenvInitializer;

@SpringBootApplication
@EnableScheduling
public class HusciApplication {
	public static void main(String[] args) {
		new SpringApplicationBuilder(HusciApplication.class)
				.initializers(new DotenvInitializer())
				.run(args);
	}

}
