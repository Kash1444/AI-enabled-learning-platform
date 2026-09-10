package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.EmployeeCompetency;
import com.example.aienabledlearningplatform.service.EmployeeCompetencyService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/employee-competencies")
public class EmployeeCompetencyController {

    private final EmployeeCompetencyService employeeCompetencyService;

    public EmployeeCompetencyController(
            EmployeeCompetencyService employeeCompetencyService) {
        this.employeeCompetencyService = employeeCompetencyService;
    }

    // Get all competencies assigned to an employee
    @GetMapping("/employee/{employeeId}")
    public ResponseEntity<List<EmployeeCompetency>> getEmployeeCompetencies(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                employeeCompetencyService
                        .getEmployeeCompetencies(employeeId)
        );
    }

    // Get one specific competency of an employee
    @GetMapping("/employee/{employeeId}/competency/{competencyId}")
    public ResponseEntity<EmployeeCompetency> getEmployeeCompetency(
            @PathVariable Long employeeId,
            @PathVariable Long competencyId) {

        return ResponseEntity.ok(
                employeeCompetencyService
                        .getEmployeeCompetency(
                                employeeId,
                                competencyId
                        )
        );
    }

    // Assign a competency to an employee
    @PostMapping("/employee/{employeeId}/competency/{competencyId}")
    public ResponseEntity<EmployeeCompetency> assignCompetency(
            @PathVariable Long employeeId,
            @PathVariable Long competencyId,
            @RequestParam Integer proficiencyLevel,
            @RequestParam Integer targetLevel) {

        return ResponseEntity.ok(
                employeeCompetencyService.assignCompetency(
                        employeeId,
                        competencyId,
                        proficiencyLevel,
                        targetLevel
                )
        );
    }

    // Update employee competency level
    @PutMapping("/employee/{employeeId}/competency/{competencyId}")
    public ResponseEntity<EmployeeCompetency> updateCompetency(
            @PathVariable Long employeeId,
            @PathVariable Long competencyId,
            @RequestParam Integer proficiencyLevel,
            @RequestParam Integer targetLevel) {

        return ResponseEntity.ok(
                employeeCompetencyService.updateCompetency(
                        employeeId,
                        competencyId,
                        proficiencyLevel,
                        targetLevel
                )
        );
    }
}