package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.Employee;
import com.example.aienabledlearningplatform.repository.EmployeeRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EmployeeService {

    private final EmployeeRepository employeeRepository;

    public EmployeeService(EmployeeRepository employeeRepository) {
        this.employeeRepository = employeeRepository;
    }

    // Get employee by employee ID
    public Employee getEmployeeById(Long employeeId) {

        return employeeRepository.findById(employeeId)
                .orElseThrow(() ->
                        new RuntimeException("Employee not found"));
    }

    // Get employee profile using user ID
    public Employee getEmployeeByUserId(Long userId) {

        return employeeRepository.findByUserUserId(userId)
                .orElseThrow(() ->
                        new RuntimeException("Employee profile not found"));
    }

    // Get all employees
    public List<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    // Create employee
    public Employee createEmployee(Employee employee) {
        return employeeRepository.save(employee);
    }

    // Update employee
    public Employee updateEmployee(
            Long employeeId,
            Employee updatedEmployee) {

        Employee existingEmployee =
                employeeRepository.findById(employeeId)
                        .orElseThrow(() ->
                                new RuntimeException("Employee not found"));

        existingEmployee.setEmployeeCode(
                updatedEmployee.getEmployeeCode());

        existingEmployee.setFirstName(
                updatedEmployee.getFirstName());

        existingEmployee.setLastName(
                updatedEmployee.getLastName());

        existingEmployee.setDepartment(
                updatedEmployee.getDepartment());

        existingEmployee.setDesignation(
                updatedEmployee.getDesignation());

        existingEmployee.setJoiningDate(
                updatedEmployee.getJoiningDate());

        existingEmployee.setPhone(
                updatedEmployee.getPhone());

        return employeeRepository.save(existingEmployee);
    }
}