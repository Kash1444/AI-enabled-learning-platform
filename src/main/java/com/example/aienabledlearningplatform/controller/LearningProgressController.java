package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.LearningProgress;
import com.example.aienabledlearningplatform.service.LearningProgressService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;

@RestController
@RequestMapping("/api/learning-progress")
public class LearningProgressController {

    private final LearningProgressService learningProgressService;

    public LearningProgressController(
            LearningProgressService learningProgressService) {
        this.learningProgressService = learningProgressService;
    }

    // Get all progress of an employee
    @GetMapping("/employee/{employeeId}")
    public ResponseEntity<List<LearningProgress>> getEmployeeProgress(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                learningProgressService
                        .getEmployeeProgress(employeeId)
        );
    }

    // Get progress for a specific course
    @GetMapping("/employee/{employeeId}/course/{courseId}")
    public ResponseEntity<LearningProgress> getCourseProgress(
            @PathVariable Long employeeId,
            @PathVariable Long courseId) {

        return ResponseEntity.ok(
                learningProgressService
                        .getCourseProgress(
                                employeeId,
                                courseId
                        )
        );
    }

    // Start a course
    @PostMapping("/employee/{employeeId}/course/{courseId}/start")
    public ResponseEntity<LearningProgress> startCourse(
            @PathVariable Long employeeId,
            @PathVariable Long courseId) {

        return ResponseEntity.ok(
                learningProgressService
                        .startCourse(
                                employeeId,
                                courseId
                        )
        );
    }

    // Update progress
    @PutMapping("/employee/{employeeId}/course/{courseId}")
    public ResponseEntity<LearningProgress> updateProgress(
            @PathVariable Long employeeId,
            @PathVariable Long courseId,
            @RequestParam BigDecimal progressPercentage) {

        return ResponseEntity.ok(
                learningProgressService
                        .updateProgress(
                                employeeId,
                                courseId,
                                progressPercentage
                        )
        );
    }

    // Get completed courses
    @GetMapping("/employee/{employeeId}/completed")
    public ResponseEntity<List<LearningProgress>> getCompletedCourses(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                learningProgressService
                        .getCompletedCourses(employeeId)
        );
    }

    // Get in-progress courses
    @GetMapping("/employee/{employeeId}/in-progress")
    public ResponseEntity<List<LearningProgress>> getInProgressCourses(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                learningProgressService
                        .getInProgressCourses(employeeId)
        );
    }
}