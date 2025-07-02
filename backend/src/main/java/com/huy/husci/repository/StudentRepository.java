package com.huy.husci.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import com.huy.husci.repository.entity.Student;

import java.util.List;

public interface StudentRepository extends MongoRepository<Student, String> {
    @Query("{'name': ''}")
    List<Student> findByMissingFieldName();
}
