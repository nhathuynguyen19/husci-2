package com.huy.husci.service;

import com.huy.husci.repository.StudentRepository;
import com.huy.husci.repository.entity.Student;
import com.huy.husci.utils.event.StudentCreatedEvent;
import com.huy.husci.utils.event.StudentDeletedEvent;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class StudentService {
    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private ApplicationEventPublisher publisher;

    public boolean isStudent(String id) {
        return studentRepository.findById(id).isPresent();
    }

    public StudentService(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    public Student addStudent(Student student) {
        if (!isStudent(student.getId())) {
            Student saved = studentRepository.save(student);
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

    public List<Student> findByMissingFieldName() {
        return studentRepository.findByMissingFieldName();
    }

    public Student logout(String id) {
        Optional<Student> studentOptional = studentRepository.findById(id);
        if (studentOptional.isPresent()) {
            Student studentLogout = studentOptional.get();
            publisher.publishEvent(new StudentDeletedEvent(studentLogout));
            studentLogout.setStatus(false);
            this.updateStudent(id, studentLogout);
            return studentLogout;
        }
        return null;
    }

    public Student login(String id) {
        Optional<Student> studentOptional = studentRepository.findById(id);
        if (studentOptional.isPresent()) {
            Student studentLogin = studentOptional.get();
            studentLogin.setStatus(true);
            publisher.publishEvent(new StudentCreatedEvent(studentLogin));
            this.updateStudent(id, studentLogin);
            return studentLogin;
        }
        return null;
    }
}
