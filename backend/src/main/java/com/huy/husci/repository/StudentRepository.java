package com.huy.husci.repository;

import com.huy.husci.model.Student;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import java.util.List;

public interface StudentRepository extends MongoRepository<Student, String> {
    @Query("{'name': ''}")
    List<Student> findByMissingFieldName();
}
