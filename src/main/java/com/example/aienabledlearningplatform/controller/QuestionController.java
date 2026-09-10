package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.Question;
import com.example.aienabledlearningplatform.service.QuestionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/questions")
public class QuestionController {

    private final QuestionService questionService;

    public QuestionController(QuestionService questionService) {
        this.questionService = questionService;
    }

    // Get all questions
    @GetMapping
    public ResponseEntity<List<Question>> getAllQuestions() {

        return ResponseEntity.ok(
                questionService.getAllQuestions()
        );
    }

    // Get question by ID
    @GetMapping("/{questionId}")
    public ResponseEntity<Question> getQuestionById(
            @PathVariable Long questionId) {

        return ResponseEntity.ok(
                questionService.getQuestionById(questionId)
        );
    }

    // Get questions for an assessment
    @GetMapping("/assessment/{assessmentId}")
    public ResponseEntity<List<Question>> getAssessmentQuestions(
            @PathVariable Long assessmentId) {

        return ResponseEntity.ok(
                questionService.getAssessmentQuestions(assessmentId)
        );
    }

    // Get questions by difficulty
    @GetMapping("/assessment/{assessmentId}/difficulty")
    public ResponseEntity<List<Question>> getQuestionsByDifficulty(
            @PathVariable Long assessmentId,
            @RequestParam Question.DifficultyLevel difficultyLevel) {

        return ResponseEntity.ok(
                questionService.getQuestionsByDifficulty(
                        assessmentId,
                        difficultyLevel
                )
        );
    }

    // Create question
    @PostMapping
    public ResponseEntity<Question> createQuestion(
            @RequestParam Long assessmentId,
            @RequestParam String questionText,
            @RequestParam String optionA,
            @RequestParam String optionB,
            @RequestParam String optionC,
            @RequestParam String optionD,
            @RequestParam Character correctAnswer,
            @RequestParam(required = false) Integer marks,
            @RequestParam(required = false)
            Question.DifficultyLevel difficultyLevel) {

        return ResponseEntity.ok(
                questionService.createQuestion(
                        assessmentId,
                        questionText,
                        optionA,
                        optionB,
                        optionC,
                        optionD,
                        correctAnswer,
                        marks,
                        difficultyLevel
                )
        );
    }

    // Update question
    @PutMapping("/{questionId}")
    public ResponseEntity<Question> updateQuestion(
            @PathVariable Long questionId,
            @RequestParam String questionText,
            @RequestParam String optionA,
            @RequestParam String optionB,
            @RequestParam String optionC,
            @RequestParam String optionD,
            @RequestParam Character correctAnswer,
            @RequestParam(required = false) Integer marks,
            @RequestParam(required = false)
            Question.DifficultyLevel difficultyLevel) {

        return ResponseEntity.ok(
                questionService.updateQuestion(
                        questionId,
                        questionText,
                        optionA,
                        optionB,
                        optionC,
                        optionD,
                        correctAnswer,
                        marks,
                        difficultyLevel
                )
        );
    }

    // Delete question
    @DeleteMapping("/{questionId}")
    public ResponseEntity<String> deleteQuestion(
            @PathVariable Long questionId) {

        questionService.deleteQuestion(questionId);

        return ResponseEntity.ok(
                "Question deleted successfully"
        );
    }
}