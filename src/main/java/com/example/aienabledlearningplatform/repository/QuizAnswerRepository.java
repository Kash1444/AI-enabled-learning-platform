package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.QuizAnswer;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface QuizAnswerRepository
        extends JpaRepository<QuizAnswer, Long> {

    List<QuizAnswer> findByResultResultId(Long resultId);

    List<QuizAnswer> findByQuestionQuestionId(Long questionId);
}