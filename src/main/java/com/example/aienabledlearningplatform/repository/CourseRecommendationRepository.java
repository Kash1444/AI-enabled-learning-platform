package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.CourseRecommendation;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface CourseRecommendationRepository
        extends JpaRepository<CourseRecommendation, Long> {

    List<CourseRecommendation>
    findByEmployeeEmployeeId(Long employeeId);

    List<CourseRecommendation>
    findByEmployeeEmployeeIdAndStatus(
            Long employeeId,
            CourseRecommendation.Status status
    );

    Optional<CourseRecommendation>
    findByEmployeeEmployeeIdAndCourseCourseId(
            Long employeeId,
            Long courseId
    );

    List<CourseRecommendation>
    findBySkillGapSkillGapId(Long skillGapId);
}