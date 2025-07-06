package com.huy.husci.repository.entity;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Getter
@Setter
@ToString
//asdf
@Document(collection = "students")
public class Student {
    @Id
    private String id;

    private String name;

    private String password;

    private Boolean status;

    public Student() {}

    public Student(String id, String name, String password, Boolean status) {
        this.id = id;
        this.name = name;
        this.password = password;
        this.status = status;
    }
}
