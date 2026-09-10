package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.Competency;
import com.example.aienabledlearningplatform.entity.Course;
import com.example.aienabledlearningplatform.repository.CompetencyRepository;
import com.example.aienabledlearningplatform.repository.CourseRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CourseService {

    private final CourseRepository courseRepository;
    private final CompetencyRepository competencyRepository;

    public CourseService(
            CourseRepository courseRepository,
            CompetencyRepository competencyRepository) {

        this.courseRepository = courseRepository;
        this.competencyRepository = competencyRepository;
    }

    // Get all courses
    public List<Course> getAllCourses() {
        return courseRepository.findAll();
    }

    // Get course by ID
    public Course getCourseById(Long courseId) {
        return courseRepository.findById(courseId)
                .orElseThrow(() ->
                        new RuntimeException("Course not found"));
    }

    // Get courses for a competency
    public List<Course> getCoursesByCompetency(Long competencyId) {

        if (!competencyRepository.existsById(competencyId)) {
            throw new RuntimeException("Competency not found");
        }

        return courseRepository
                .findByCompetencyCompetencyId(competencyId);
    }

    // Get active courses
    public List<Course> getActiveCourses() {
        return courseRepository
                .findByStatus(Course.Status.ACTIVE);
    }

    // Create course
    public Course createCourse(
            String courseName,
            String description,
            Long competencyId,
            Course.DifficultyLevel difficultyLevel,
            java.math.BigDecimal durationHours,
            String courseUrl,
            String provider,
            Course.Status status) {

        Competency competency = null;

        if (competencyId != null) {
            competency = competencyRepository.findById(competencyId)
                    .orElseThrow(() ->
                            new RuntimeException("Competency not found"));
        }

        Course course = new Course();

        course.setCourseName(courseName);
        course.setDescription(description);
        course.setCompetency(competency);
        course.setDifficultyLevel(difficultyLevel);
        course.setDurationHours(durationHours);
        course.setCourseUrl(courseUrl);
        course.setProvider(provider);
        course.setStatus(status);

        return courseRepository.save(course);
    }

    // Update course
    public Course updateCourse(
            Long courseId,
            String courseName,
            String description,
            Long competencyId,
            Course.DifficultyLevel difficultyLevel,
            java.math.BigDecimal durationHours,
            String courseUrl,
            String provider,
            Course.Status status) {

        Course existingCourse = courseRepository.findById(courseId)
                .orElseThrow(() ->
                        new RuntimeException("Course not found"));

        Competency competency = null;

        if (competencyId != null) {
            competency = competencyRepository.findById(competencyId)
                    .orElseThrow(() ->
                            new RuntimeException("Competency not found"));
        }

        existingCourse.setCourseName(courseName);
        existingCourse.setDescription(description);
        existingCourse.setCompetency(competency);
        existingCourse.setDifficultyLevel(difficultyLevel);
        existingCourse.setDurationHours(durationHours);
        existingCourse.setCourseUrl(courseUrl);
        existingCourse.setProvider(provider);
        existingCourse.setStatus(status);

        return courseRepository.save(existingCourse);
    }

    // Delete course
    public void deleteCourse(Long courseId) {

        if (!courseRepository.existsById(courseId)) {
            throw new RuntimeException("Course not found");
        }

        courseRepository.deleteById(courseId);
    }
}