package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.Employee;
import com.example.aienabledlearningplatform.service.EmployeeService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/employee")
public class EmployeeController {

    private final EmployeeService employeeService;

    public EmployeeController(EmployeeService employeeService) {
        this.employeeService = employeeService;
    }

    // Get employee profile by employee ID
    @GetMapping("/{employeeId}")
    public ResponseEntity<Employee> getEmployee(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                employeeService.getEmployeeById(employeeId)
        );
    }

    // Get employee profile using user ID
    @GetMapping("/user/{userId}")
    public ResponseEntity<Employee> getEmployeeByUserId(
            @PathVariable Long userId) {

        System.out.println("========== EMPLOYEE CONTROLLER REACHED ==========");
        System.out.println("USER ID: " + userId);

        return ResponseEntity.ok(
                employeeService.getEmployeeByUserId(userId)
        );
    }

    // Get all employees
    @GetMapping
    public ResponseEntity<List<Employee>> getAllEmployees() {

        return ResponseEntity.ok(
                employeeService.getAllEmployees()
        );
    }

    // Create employee
    @PostMapping
    public ResponseEntity<Employee> createEmployee(
            @RequestBody Employee employee) {

        return ResponseEntity.ok(
                employeeService.createEmployee(employee)
        );
    }

    // Update employee
    @PutMapping("/{employeeId}")
    public ResponseEntity<Employee> updateEmployee(
            @PathVariable Long employeeId,
            @RequestBody Employee employee) {

        return ResponseEntity.ok(
                employeeService.updateEmployee(
                        employeeId,
                        employee
                )
        );
    }
}