package com.example.aienabledlearningplatform.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    @GetMapping("/api/test")
    public String test() {
        return "JWT authentication working";
    }

    @GetMapping("/api/employee/test")
    public String employeeTest() {
        return "Employee access granted";
    }

    @GetMapping("/api/trainer/test")
    public String trainerTest() {
        return "Trainer access granted";
    }

    @GetMapping("/api/admin/test")
    public String adminTest() {
        return "Admin access granted";
    }
}