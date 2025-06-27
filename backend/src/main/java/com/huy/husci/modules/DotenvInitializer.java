package com.huy.husci.modules;

import io.github.cdimascio.dotenv.Dotenv;
import io.github.cdimascio.dotenv.DotenvEntry;
import org.springframework.context.ApplicationContextInitializer;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.Map;

public class DotenvInitializer implements ApplicationContextInitializer<ConfigurableApplicationContext> {
    @Override
    public void initialize(ConfigurableApplicationContext context) {
        Dotenv dotenv = Dotenv.configure()
                .systemProperties() // ưu tiên biến hệ thống (Render)
                .ignoreIfMissing()  // nếu không có .env thì bỏ qua
                .load();

        for (DotenvEntry entry : dotenv.entries()) {
            // nếu biến chưa tồn tại trong System, thì set vào
            if (System.getProperty(entry.getKey()) == null) {
                System.setProperty(entry.getKey(), entry.getValue());
            }
        }
    }
}
