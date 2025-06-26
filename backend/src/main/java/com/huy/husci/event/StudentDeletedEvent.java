package com.huy.husci.event;

import com.huy.husci.model.Student;

public class StudentDeletedEvent {
    private final Student deletetedStudent;

    public StudentDeletedEvent(Student deletetedStudent) {
        this.deletetedStudent = deletetedStudent;
    }

    public Student getDeletetedStudent() {
        return deletetedStudent;
    }
}
