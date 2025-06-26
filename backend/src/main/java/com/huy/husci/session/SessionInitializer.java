package com.huy.husci.session;

import com.huy.husci.event.StudentCreatedEvent;
import com.huy.husci.event.StudentDeletedEvent;
import com.huy.husci.model.Student;
import com.huy.husci.modules.WebSession;
import com.huy.husci.service.StudentService;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class SessionInitializer implements CommandLineRunner {
    @Autowired
    private StudentService studentService;

    @Getter
    private final List<WebSession> webSessions = new ArrayList<>();

    @Override
    public void run(String... args) {
        try {
            String loginUrl = "https://student.husc.edu.vn";
            List<Student> studentList = studentService.getAllStudents();
            for (Student student : studentList) {
                if (student.getStatus().equals(true)) {
                    WebSession webSession = new WebSession(student);
                    System.out.println("Create Session For " + student.getId());

                    if (student.getName() == null || student.getName().isEmpty()) {
                        student.setName(webSession.fetchStudentName());
                        studentService.updateStudent(student.getId(), student);
                        System.out.print(" Updated Name: " + webSession.getId() + "(" + student.getName() + ")");
                    }
                    webSessions.add(webSession);
                }
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @EventListener
    public void handleStudentCreated(StudentCreatedEvent event) {
        try {
            Student student = event.getStudent();

            if (student.getStatus().equals(true)) {
                WebSession webSession = new WebSession(student);
                System.out.println("Create Session For " + student.getId());

                if (student.getName() == null || student.getName().isEmpty()) {
                    student.setName(webSession.fetchStudentName());
                    studentService.updateStudent(student.getId(), student);
                    System.out.print(" Updated Name: " + webSession.getId() + "(" + student.getName() + ")");
                }
                webSessions.add(webSession);
            }

        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @EventListener
    public void handleStudentDeleted(StudentDeletedEvent event) {
        try {
            Student student = event.getDeletetedStudent();

            webSessions.removeIf(ws -> ws.getId().equals(student.getId()));
            System.out.println("Remove Session For " + student.getId());
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
