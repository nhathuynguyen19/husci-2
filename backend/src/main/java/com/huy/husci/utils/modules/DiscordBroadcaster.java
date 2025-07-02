package com.huy.husci.utils.modules;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;

@Component
public class DiscordBroadcaster {
    private static final HttpClient client = HttpClient.newHttpClient();
    private static final ObjectMapper mapper = new ObjectMapper();
    private static BotProperties botProperties = new BotProperties();

    public DiscordBroadcaster(BotProperties botProperties) {
        DiscordBroadcaster.botProperties = botProperties;
    }

    public static void broadcastMessage(String message) {
        try {
            List<String> guildIds = getGuilds();

            for (String guildId : guildIds) {
                String channelId = getFirstTextChannel(guildId);
                if (channelId != null) {
                    sendMessage(channelId, message);
                }
                Thread.sleep(1000); // tránh bị rate limit
            }
        } catch (Exception e) {
            System.err.println("Lỗi khi gửi tin nhắn: " + e.getMessage());
        }
    }

    private static List<String> getGuilds() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(botProperties.getBaseUrl() + "/users/@me/guilds"))
                .header("Authorization", botProperties.getToken())
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        JsonNode json = mapper.readTree(response.body());

        List<String> ids = new ArrayList<>();
        for (JsonNode guild : json) {
            ids.add(guild.get("id").asText());
        }
        return ids;
    }

    private static String getFirstTextChannel(String guildId) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(botProperties.getBaseUrl() + "/guilds/" + guildId + "/channels"))
                .header("Authorization", botProperties.getToken())
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        JsonNode json = mapper.readTree(response.body());

        String firstTextChannelId = null;
        int minPosition = Integer.MAX_VALUE;

        for (JsonNode ch : json) {
            if (ch.has("type") && ch.get("type").asInt() == 0) { // type == 0 là text
                int position = ch.has("position") ? ch.get("position").asInt() : Integer.MAX_VALUE;
                if (position < minPosition) {
                    minPosition = position;
                    firstTextChannelId = ch.get("id").asText();
                }
            }
        }

        return firstTextChannelId;
    }

    private static void sendMessage(String channelId, String content) throws Exception {
        String jsonBody = mapper.createObjectNode()
                .put("content", content)
                .toString();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(botProperties.getBaseUrl() + "/channels/" + channelId + "/messages"))
                .header("Authorization", botProperties.getToken())
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        client.send(request, HttpResponse.BodyHandlers.ofString());
    }
}
