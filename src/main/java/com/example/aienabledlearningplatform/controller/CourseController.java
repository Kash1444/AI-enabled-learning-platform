package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.Course;
import com.example.aienabledlearningplatform.service.CourseService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;

@RestController
@RequestMapping("/api/courses")
public class CourseController {

    private final CourseService courseService;

    public CourseController(CourseService courseService) {
        this.courseService = courseService;
    }

    // Get all courses
    @GetMapping
    public ResponseEntity<List<Course>> getAllCourses() {
        return ResponseEntity.ok(
                courseService.getAllCourses()
        );
    }

    // Get course by ID
    @GetMapping("/{courseId}")
    public ResponseEntity<Course> getCourseById(
            @PathVariable Long courseId) {

        return ResponseEntity.ok(
                courseService.getCourseById(courseId)
        );
    }

    // Get courses by competency
    @GetMapping("/competency/{competencyId}")
    public ResponseEntity<List<Course>> getCoursesByCompetency(
            @PathVariable Long competencyId) {

        return ResponseEntity.ok(
                courseService.getCoursesByCompetency(
                        competencyId
                )
        );
    }

    // Get active courses
    @GetMapping("/active")
    public ResponseEntity<List<Course>> getActiveCourses() {

        return ResponseEntity.ok(
                courseService.getActiveCourses()
        );
    }

    // Create course
    @PostMapping
    public ResponseEntity<Course> createCourse(
            @RequestParam String courseName,
            @RequestParam(required = false) String description,
            @RequestParam(required = false) Long competencyId,
            @RequestParam Course.DifficultyLevel difficultyLevel,
            @RequestParam BigDecimal durationHours,
            @RequestParam(required = false) String courseUrl,
            @RequestParam(required = false) String provider,
            @RequestParam Course.Status status) {

        return ResponseEntity.ok(
                courseService.createCourse(
                        courseName,
                        description,
                        competencyId,
                        difficultyLevel,
                        durationHours,
                        courseUrl,
                        provider,
                        status
                )
        );
    }

    // Update course
    @PutMapping("/{courseId}")
    public ResponseEntity<Course> updateCourse(
            @PathVariable Long courseId,
            @RequestParam String courseName,
            @RequestParam(required = false) String description,
            @RequestParam(required = false) Long competencyId,
            @RequestParam Course.DifficultyLevel difficultyLevel,
            @RequestParam BigDecimal durationHours,
            @RequestParam(required = false) String courseUrl,
            @RequestParam(required = false) String provider,
            @RequestParam Course.Status status) {

        return ResponseEntity.ok(
                courseService.updateCourse(
                        courseId,
                        courseName,
                        description,
                        competencyId,
                        difficultyLevel,
                        durationHours,
                        courseUrl,
                        provider,
                        status
                )
        );
    }

    // Delete course
    @DeleteMapping("/{courseId}")
    public ResponseEntity<String> deleteCourse(
            @PathVariable Long courseId) {

        courseService.deleteCourse(courseId);

        return ResponseEntity.ok(
                "Course deleted successfully"
        );
    }
}