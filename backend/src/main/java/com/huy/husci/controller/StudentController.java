package com.huy.husci.controller;

import com.huy.husci.base.BaseEntity;
import com.huy.husci.model.Student;
import com.huy.husci.response.ApiResponse;
import com.huy.husci.response.ApiResponseCode;
import com.huy.husci.service.StudentService;
import org.springframework.web.bind.annotation.*;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/students")
public class StudentController extends BaseEntity {
    private final StudentService studentService;

    public StudentController(StudentService studentService) {
        this.studentService = studentService;
    }

    @PostMapping
    public ApiResponse addStudent(@RequestBody Student student) {
        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
        student.setId(student.getId().toUpperCase());
        returnData.put("student", studentService.addStudent(student));
        return ApiResponse.success(returnData);
    }

    @GetMapping("/{id}")
    public ApiResponse getStudentById(@PathVariable String id) {
        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
        Student student = studentService.getStudentById(id.toUpperCase());
        if (student != null) {
            returnData.put("student", student);
            return ApiResponse.success(returnData);
        } else {
            return ApiResponse.failMessage("Not Found Id: " + id.toUpperCase());
        }
    }

    @PutMapping("/{id}")
    public ApiResponse updateStudent(@PathVariable String id,@RequestBody Student studentUpdated) {
        studentUpdated = studentService.updateStudent(id.toUpperCase(), studentUpdated);
        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
        returnData.put("student", studentUpdated);
        return ApiResponse.success(returnData);
    }

    @DeleteMapping("/{id}")
    public ApiResponse deleteStudent(@PathVariable String id) {
        studentService.deleteStudent(id.toUpperCase());
        return ApiResponse.success();
    }

    @GetMapping
    public ApiResponse getAllStudent() {
        List<Student> studentList = studentService.getAllStudents();
        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
        returnData.put("studentList", studentList);
        return ApiResponse.success(returnData);
    }

    @GetMapping("/emptyname")
    public ApiResponse getStudentMissingFieldName() {
        List<Student> studentList = studentService.findByMissingFieldName();
        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
        returnData.put("studentList", studentList);
        return ApiResponse.success(returnData);
    }

    @PutMapping("/{id}/logout")
    public ApiResponse logout(@PathVariable String id) {
        Student student = studentService.logout(id.toUpperCase());
        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
        returnData.put("student", student);
        return ApiResponse.success(returnData);
    }

    @PutMapping("/{id}/login")
    public ApiResponse login(@PathVariable String id) {
        Student student = studentService.login(id.toUpperCase());
        Map<String, Object> returnData = new LinkedHashMap<String, Object>();
        returnData.put("student", student);
        return ApiResponse.success(returnData);
    }
}
