package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.QuizResult;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface QuizResultRepository
        extends JpaRepository<QuizResult, Long> {

    List<QuizResult> findByEmployeeEmployeeId(Long employeeId);

    List<QuizResult> findByAssessmentAssessmentId(Long assessmentId);

    List<QuizResult> findByEmployeeEmployeeIdAndAssessmentAssessmentId(
            Long employeeId,
            Long assessmentId
    );
}