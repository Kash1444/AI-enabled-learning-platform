package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.QuizAnswer;
import com.example.aienabledlearningplatform.entity.QuizResult;
import com.example.aienabledlearningplatform.service.QuizResultService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/quiz-results")
public class QuizResultController {

    private final QuizResultService quizResultService;

    public QuizResultController(QuizResultService quizResultService) {
        this.quizResultService = quizResultService;
    }

    // Get all quiz results
    @GetMapping
    public ResponseEntity<List<QuizResult>> getAllResults() {
        return ResponseEntity.ok(
                quizResultService.getAllResults()
        );
    }

    // Get result by ID
    @GetMapping("/{resultId}")
    public ResponseEntity<QuizResult> getResultById(
            @PathVariable Long resultId) {

        return ResponseEntity.ok(
                quizResultService.getResultById(resultId)
        );
    }

    // Get all results of an employee
    @GetMapping("/employee/{employeeId}")
    public ResponseEntity<List<QuizResult>> getEmployeeResults(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                quizResultService.getEmployeeResults(employeeId)
        );
    }

    // Get all results of an assessment
    @GetMapping("/assessment/{assessmentId}")
    public ResponseEntity<List<QuizResult>> getAssessmentResults(
            @PathVariable Long assessmentId) {

        return ResponseEntity.ok(
                quizResultService.getAssessmentResults(assessmentId)
        );
    }

    // Get individual answers of a result
    @GetMapping("/{resultId}/answers")
    public ResponseEntity<List<QuizAnswer>> getResultAnswers(
            @PathVariable Long resultId) {

        return ResponseEntity.ok(
                quizResultService.getResultAnswers(resultId)
        );
    }

    // Submit quiz
    @PostMapping("/submit")
    public ResponseEntity<QuizResult> submitQuiz(
            @RequestParam Long employeeId,
            @RequestParam Long assessmentId,
            @RequestBody Map<Long, Character> answers) {

        return ResponseEntity.ok(
                quizResultService.submitQuiz(
                        employeeId,
                        assessmentId,
                        answers
                )
        );
    }
}