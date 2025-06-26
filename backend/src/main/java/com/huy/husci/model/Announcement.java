package com.huy.husci.model;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Getter
@Setter
@ToString
@Document(collection = "announcements")
public class Announcement {
    @Id
    private String id;
    private String title;
    private String content;
    private String url;

    public Announcement() {}

    public Announcement(String id, String title, String content, String url) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.url = url;
    }
}
