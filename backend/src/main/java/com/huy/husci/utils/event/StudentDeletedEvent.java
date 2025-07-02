package com.huy.husci.utils.event;

import com.huy.husci.repository.entity.Student;

public class StudentDeletedEvent {
    private final Student student;

    public StudentDeletedEvent(Student student) {
        this.student = student;
    }

    public Student getStudent() {
        return student;
    }
}
