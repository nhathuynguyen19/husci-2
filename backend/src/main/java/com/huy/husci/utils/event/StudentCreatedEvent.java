package com.huy.husci.utils.event;

import com.huy.husci.repository.entity.Student;

public class StudentCreatedEvent {
    private final Student student;

    public StudentCreatedEvent(Student createdStudent) {
        this.student = createdStudent;
    }

    public Student getStudent() {
        return student;
    }
}
