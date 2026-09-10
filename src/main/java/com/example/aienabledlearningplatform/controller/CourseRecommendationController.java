package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.CourseRecommendation;
import com.example.aienabledlearningplatform.service.CourseRecommendationService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/course-recommendations")
public class CourseRecommendationController {

    private final CourseRecommendationService
            courseRecommendationService;

    public CourseRecommendationController(
            CourseRecommendationService courseRecommendationService) {

        this.courseRecommendationService =
                courseRecommendationService;
    }

    // Get all recommendations for an employee
    @GetMapping("/employee/{employeeId}")
    public ResponseEntity<List<CourseRecommendation>>
    getEmployeeRecommendations(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                courseRecommendationService
                        .getEmployeeRecommendations(employeeId)
        );
    }

    // Get active recommendations
    @GetMapping("/employee/{employeeId}/active")
    public ResponseEntity<List<CourseRecommendation>>
    getActiveRecommendations(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                courseRecommendationService
                        .getActiveRecommendations(employeeId)
        );
    }

    // Generate recommendations
    @PostMapping("/employee/{employeeId}/generate")
    public ResponseEntity<List<CourseRecommendation>>
    generateRecommendations(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                courseRecommendationService
                        .generateRecommendations(employeeId)
        );
    }

    // Update recommendation status
    @PutMapping("/{recommendationId}/status")
    public ResponseEntity<CourseRecommendation>
    updateStatus(
            @PathVariable Long recommendationId,
            @RequestParam CourseRecommendation.Status status) {

        return ResponseEntity.ok(
                courseRecommendationService
                        .updateStatus(
                                recommendationId,
                                status
                        )
        );
    }
}