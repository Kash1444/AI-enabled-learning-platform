package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.Course;
import com.example.aienabledlearningplatform.entity.Employee;
import com.example.aienabledlearningplatform.entity.LearningProgress;
import com.example.aienabledlearningplatform.repository.CourseRepository;
import com.example.aienabledlearningplatform.repository.EmployeeRepository;
import com.example.aienabledlearningplatform.repository.LearningProgressRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class LearningProgressService {

    private final LearningProgressRepository learningProgressRepository;
    private final EmployeeRepository employeeRepository;
    private final CourseRepository courseRepository;

    public LearningProgressService(
            LearningProgressRepository learningProgressRepository,
            EmployeeRepository employeeRepository,
            CourseRepository courseRepository) {

        this.learningProgressRepository = learningProgressRepository;
        this.employeeRepository = employeeRepository;
        this.courseRepository = courseRepository;
    }

    // Get all learning progress of an employee
    public List<LearningProgress> getEmployeeProgress(
            Long employeeId) {

        return learningProgressRepository
                .findByEmployeeEmployeeId(employeeId);
    }

    // Get one course progress of an employee
    public LearningProgress getCourseProgress(
            Long employeeId,
            Long courseId) {

        return learningProgressRepository
                .findByEmployeeEmployeeIdAndCourseCourseId(
                        employeeId,
                        courseId
                )
                .orElseThrow(() ->
                        new RuntimeException(
                                "Learning progress not found"
                        ));
    }

    // Start a course
    public LearningProgress startCourse(
            Long employeeId,
            Long courseId) {

        Employee employee = employeeRepository
                .findById(employeeId)
                .orElseThrow(() ->
                        new RuntimeException("Employee not found"));

        Course course = courseRepository
                .findById(courseId)
                .orElseThrow(() ->
                        new RuntimeException("Course not found"));

        // Check whether progress already exists
        LearningProgress progress =
                learningProgressRepository
                        .findByEmployeeEmployeeIdAndCourseCourseId(
                                employeeId,
                                courseId
                        )
                        .orElse(null);

        if (progress != null) {

            progress.setStatus(
                    LearningProgress.Status.IN_PROGRESS
            );

            progress.setLastAccessedAt(
                    LocalDateTime.now()
            );

            return learningProgressRepository.save(progress);
        }

        // Create new progress
        progress = new LearningProgress();

        progress.setEmployee(employee);
        progress.setCourse(course);
        progress.setProgressPercentage(
                BigDecimal.ZERO
        );
        progress.setStatus(
                LearningProgress.Status.IN_PROGRESS
        );

        LocalDateTime now = LocalDateTime.now();

        progress.setStartedAt(now);
        progress.setLastAccessedAt(now);

        return learningProgressRepository.save(progress);
    }

    // Update course progress
    public LearningProgress updateProgress(
            Long employeeId,
            Long courseId,
            BigDecimal progressPercentage) {

        LearningProgress progress =
                getCourseProgress(
                        employeeId,
                        courseId
                );

        if (progressPercentage == null) {
            throw new RuntimeException(
                    "Progress percentage is required"
            );
        }

        // Validate range
        if (progressPercentage.compareTo(
                BigDecimal.ZERO) < 0
                ||
                progressPercentage.compareTo(
                        BigDecimal.valueOf(100)
                ) > 0) {

            throw new RuntimeException(
                    "Progress must be between 0 and 100"
            );
        }

        progress.setProgressPercentage(
                progressPercentage
        );

        progress.setLastAccessedAt(
                LocalDateTime.now()
        );

        // Automatically determine status
        if (progressPercentage.compareTo(
                BigDecimal.ZERO
        ) == 0) {

            progress.setStatus(
                    LearningProgress.Status.NOT_STARTED
            );

        } else if (progressPercentage.compareTo(
                BigDecimal.valueOf(100)
        ) >= 0) {

            progress.setProgressPercentage(
                    BigDecimal.valueOf(100)
            );

            progress.setStatus(
                    LearningProgress.Status.COMPLETED
            );

            progress.setCompletedAt(
                    LocalDateTime.now()
            );

        } else {

            progress.setStatus(
                    LearningProgress.Status.IN_PROGRESS
            );
        }

        return learningProgressRepository.save(progress);
    }

    // Get completed courses
    public List<LearningProgress> getCompletedCourses(
            Long employeeId) {

        return learningProgressRepository
                .findByEmployeeEmployeeIdAndStatus(
                        employeeId,
                        LearningProgress.Status.COMPLETED
                );
    }

    // Get in-progress courses
    public List<LearningProgress> getInProgressCourses(
            Long employeeId) {

        return learningProgressRepository
                .findByEmployeeEmployeeIdAndStatus(
                        employeeId,
                        LearningProgress.Status.IN_PROGRESS
                );
    }
}