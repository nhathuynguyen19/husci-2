package com.huy.husci.event;

import com.huy.husci.model.Student;

public class StudentCreatedEvent {
    private final Student student;

    public StudentCreatedEvent(Student createdStudent) {
        this.student = createdStudent;
    }

    public Student getStudent() {
        return student;
    }
}
