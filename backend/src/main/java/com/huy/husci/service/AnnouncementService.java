package com.huy.husci.service;

import com.huy.husci.event.StudentCreatedEvent;
import com.huy.husci.event.StudentDeletedEvent;
import com.huy.husci.model.Announcement;
import com.huy.husci.model.Student;
import com.huy.husci.repository.AnnouncementRepository;
import com.huy.husci.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;

import java.util.List;
import java.util.Optional;

public class AnnouncementService {
    @Autowired
    private AnnouncementRepository announcementRepository;

    @Autowired
    private ApplicationEventPublisher publisher;

    public boolean isAnnouncement(String id) {
        return announcementRepository.findById(id).isPresent();
    }

    public AnnouncementService(AnnouncementRepository announcementRepository) {
        this.announcementRepository = announcementRepository;
    }

    public Announcement addAnnouncement(Announcement announcement) {
        if (!isAnnouncement(announcement.getId())) {
            Announcement saved = announcementRepository.save(announcement);
            publisher.publishEvent(new StudentCreatedEvent(saved));
            return saved;
        }
        return null;
    }

    public Student getStudentById(String id) {
        return studentRepository.findById(id).orElse(null);
    }

    public Student updateStudent(String id, Student updatedStudent) {
        Optional<Student> optionalStudent = studentRepository.findById(id);
        if (optionalStudent.isPresent()) {
            Student existingStudent = optionalStudent.get();
            existingStudent.setName(updatedStudent.getName());
            existingStudent.setPassword(updatedStudent.getPassword());
            existingStudent.setStatus(updatedStudent.getStatus());
            return studentRepository.save(existingStudent);
        } else {
            throw new IllegalArgumentException("Student with id: " + id + " not found!");
        }
    }

    public void deleteStudent(String id) {
        Optional<Student> student = studentRepository.findById(id);
        if (student.isPresent()) {
            Student deleted = student.get();
            studentRepository.deleteById(id);
            publisher.publishEvent(new StudentDeletedEvent(deleted));
        }
    }

    public List<Student> getAllStudents() {
        return studentRepository.findAll();
    }
}
