package com.huy.husci.event;

import com.huy.husci.model.Student;

public class StudentDeletedEvent {
    private final Student student;

    public StudentDeletedEvent(Student student) {
        this.student = student;
    }

    public Student getStudent() {
        return student;
    }
}
