package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.LearningProgress;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface LearningProgressRepository
        extends JpaRepository<LearningProgress, Long> {

    List<LearningProgress> findByEmployeeEmployeeId(Long employeeId);

    List<LearningProgress> findByCourseCourseId(Long courseId);

    Optional<LearningProgress>
    findByEmployeeEmployeeIdAndCourseCourseId(
            Long employeeId,
            Long courseId
    );

    List<LearningProgress>
    findByEmployeeEmployeeIdAndStatus(
            Long employeeId,
            LearningProgress.Status status
    );
}