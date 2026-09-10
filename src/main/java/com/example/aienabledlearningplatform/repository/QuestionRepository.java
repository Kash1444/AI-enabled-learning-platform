package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.Question;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface QuestionRepository extends JpaRepository<Question, Long> {

    List<Question> findByAssessmentAssessmentId(Long assessmentId);

    List<Question> findByAssessmentAssessmentIdAndDifficultyLevel(
            Long assessmentId,
            Question.DifficultyLevel difficultyLevel
    );
}