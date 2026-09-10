package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.Assessment;
import com.example.aienabledlearningplatform.service.AssessmentService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/assessments")
public class AssessmentController {

    private final AssessmentService assessmentService;

    public AssessmentController(
            AssessmentService assessmentService) {

        this.assessmentService = assessmentService;
    }

    // Get all assessments
    @GetMapping
    public ResponseEntity<List<Assessment>> getAllAssessments() {

        return ResponseEntity.ok(
                assessmentService.getAllAssessments()
        );
    }

    // Get assessment by ID
    @GetMapping("/{assessmentId}")
    public ResponseEntity<Assessment> getAssessmentById(
            @PathVariable Long assessmentId) {

        return ResponseEntity.ok(
                assessmentService.getAssessmentById(
                        assessmentId
                )
        );
    }

    // Get assessments for an employee
    @GetMapping("/employee/{employeeId}")
    public ResponseEntity<List<Assessment>>
    getEmployeeAssessments(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                assessmentService.getEmployeeAssessments(
                        employeeId
                )
        );
    }

    // Get assessments for a competency
    @GetMapping("/competency/{competencyId}")
    public ResponseEntity<List<Assessment>>
    getCompetencyAssessments(
            @PathVariable Long competencyId) {

        return ResponseEntity.ok(
                assessmentService.getCompetencyAssessments(
                        competencyId
                )
        );
    }

    // Create assessment
    @PostMapping
    public ResponseEntity<Assessment> createAssessment(
            @RequestParam Long employeeId,
            @RequestParam(required = false) Long competencyId,
            @RequestParam String assessmentName,
            @RequestParam(required = false) String description,
            @RequestParam Integer passingScore,
            @RequestParam Assessment.Status status) {

        return ResponseEntity.ok(
                assessmentService.createAssessment(
                        employeeId,
                        competencyId,
                        assessmentName,
                        description,
                        passingScore,
                        status
                )
        );
    }

    // Update assessment
    @PutMapping("/{assessmentId}")
    public ResponseEntity<Assessment> updateAssessment(
            @PathVariable Long assessmentId,
            @RequestParam(required = false) Long competencyId,
            @RequestParam String assessmentName,
            @RequestParam(required = false) String description,
            @RequestParam Integer passingScore,
            @RequestParam Assessment.Status status) {

        return ResponseEntity.ok(
                assessmentService.updateAssessment(
                        assessmentId,
                        competencyId,
                        assessmentName,
                        description,
                        passingScore,
                        status
                )
        );
    }

    // Update assessment status
    @PutMapping("/{assessmentId}/status")
    public ResponseEntity<Assessment> updateStatus(
            @PathVariable Long assessmentId,
            @RequestParam Assessment.Status status) {

        return ResponseEntity.ok(
                assessmentService.updateStatus(
                        assessmentId,
                        status
                )
        );
    }

    // Delete assessment
    @DeleteMapping("/{assessmentId}")
    public ResponseEntity<String> deleteAssessment(
            @PathVariable Long assessmentId) {

        assessmentService.deleteAssessment(assessmentId);

        return ResponseEntity.ok(
                "Assessment deleted successfully"
        );
    }
}