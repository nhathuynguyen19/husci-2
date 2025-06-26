package com.huy.husci.session;

import com.huy.husci.event.StudentCreatedEvent;
import com.huy.husci.event.StudentDeletedEvent;
import com.huy.husci.model.Announcement;
import com.huy.husci.model.Student;
import com.huy.husci.modules.DiscordBroadcaster;
import com.huy.husci.modules.Ums;
import com.huy.husci.modules.WebSession;
import com.huy.husci.service.AnnouncementService;
import com.huy.husci.service.StudentService;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

@Component
public class SessionInitializer implements CommandLineRunner {
    @Autowired
    private StudentService studentService;

    @Autowired
    private AnnouncementService announcementService;

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
            System.err.println("Lỗi khi tạo sessions");
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
            Student student = event.getStudent();

            webSessions.removeIf(ws -> ws.getId().equals(student.getId()));
            System.out.println("Remove Session For " + student.getId());
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Scheduled(fixedRate = 10000)
    public void checkAnnouncementsEvery10Seconds() {
        List<Announcement> announcements = Ums.fetchAnnouncementsOnPage();

        for (Announcement announcement : announcements) {
            if (!announcementService.isAnnouncement(announcement.getId())) {
                try {
                    announcementService.addAnnouncement(announcement);
                    System.out.println("New Announment Id: " + announcement.getId());

                    String message = "[";
                    message += announcement.getTitle() + "](";
                    message += announcement.getUrl() + ")\n`";

                    Date newDate = announcement.getDateCreate();
                    String inputDate = newDate.toString();
                    SimpleDateFormat inputFormat = new SimpleDateFormat("EEE MMM dd HH:mm:ss z yyyy");
                    Date date = inputFormat.parse(inputDate);
                    SimpleDateFormat outputFormat = new SimpleDateFormat("dd/MM/yyyy HH:mm");
                    outputFormat.setTimeZone(TimeZone.getTimeZone("GMT+07:00"));
                    String dateResult = outputFormat.format(date);

                    message += dateResult + "`\n";
                    message += announcement.getContent();

                    DiscordBroadcaster.broadcastMessage(message);
                } catch (ParseException e) {
                    throw new RuntimeException(e);
                }
            }
        }
    }
}
