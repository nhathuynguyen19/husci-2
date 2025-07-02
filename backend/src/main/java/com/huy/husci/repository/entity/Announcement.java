package com.huy.husci.repository.entity;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.sql.Timestamp;
import java.util.Date;

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
    private Date dateCreate;

    public Announcement() {}

    public Announcement(String id, String title, String content, String url, Date dateCreate) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.url = url;
        this.dateCreate = dateCreate;
    }
}
