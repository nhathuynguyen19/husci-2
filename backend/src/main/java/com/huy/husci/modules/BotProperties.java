package com.huy.husci.modules;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Getter
@Setter
@Component
@ConfigurationProperties(prefix = "bot")
public class BotProperties {
    private String token;
    private String baseUrl;
}
