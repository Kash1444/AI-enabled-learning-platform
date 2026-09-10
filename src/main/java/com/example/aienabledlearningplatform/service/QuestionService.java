package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.Assessment;
import com.example.aienabledlearningplatform.entity.Question;
import com.example.aienabledlearningplatform.repository.AssessmentRepository;
import com.example.aienabledlearningplatform.repository.QuestionRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class QuestionService {

    private final QuestionRepository questionRepository;
    private final AssessmentRepository assessmentRepository;

    public QuestionService(
            QuestionRepository questionRepository,
            AssessmentRepository assessmentRepository) {

        this.questionRepository = questionRepository;
        this.assessmentRepository = assessmentRepository;
    }

    // Get all questions
    public List<Question> getAllQuestions() {
        return questionRepository.findAll();
    }

    // Get question by ID
    public Question getQuestionById(Long questionId) {

        return questionRepository.findById(questionId)
                .orElseThrow(() ->
                        new RuntimeException("Question not found"));
    }

    // Get all questions for an assessment
    public List<Question> getAssessmentQuestions(Long assessmentId) {

        if (!assessmentRepository.existsById(assessmentId)) {
            throw new RuntimeException("Assessment not found");
        }

        return questionRepository
                .findByAssessmentAssessmentId(assessmentId);
    }

    // Get questions by difficulty
    public List<Question> getQuestionsByDifficulty(
            Long assessmentId,
            Question.DifficultyLevel difficultyLevel) {

        if (!assessmentRepository.existsById(assessmentId)) {
            throw new RuntimeException("Assessment not found");
        }

        return questionRepository
                .findByAssessmentAssessmentIdAndDifficultyLevel(
                        assessmentId,
                        difficultyLevel
                );
    }

    // Create question
    public Question createQuestion(
            Long assessmentId,
            String questionText,
            String optionA,
            String optionB,
            String optionC,
            String optionD,
            Character correctAnswer,
            Integer marks,
            Question.DifficultyLevel difficultyLevel) {

        Assessment assessment = assessmentRepository
                .findById(assessmentId)
                .orElseThrow(() ->
                        new RuntimeException("Assessment not found"));

        // Validate correct answer
        if (correctAnswer == null ||
                !isValidAnswer(correctAnswer)) {

            throw new RuntimeException(
                    "Correct answer must be A, B, C, or D");
        }

        Question question = new Question();

        question.setAssessment(assessment);
        question.setQuestionText(questionText);
        question.setOptionA(optionA);
        question.setOptionB(optionB);
        question.setOptionC(optionC);
        question.setOptionD(optionD);
        question.setCorrectAnswer(
                Character.toUpperCase(correctAnswer)
        );
        question.setMarks(
                marks != null ? marks : 1
        );
        question.setDifficultyLevel(
                difficultyLevel != null
                        ? difficultyLevel
                        : Question.DifficultyLevel.EASY
        );

        Question savedQuestion =
                questionRepository.save(question);

        // Update total question count
        int currentCount =
                assessment.getTotalQuestions() != null
                        ? assessment.getTotalQuestions()
                        : 0;

        assessment.setTotalQuestions(currentCount + 1);

        assessmentRepository.save(assessment);

        return savedQuestion;
    }

    // Update question
    public Question updateQuestion(
            Long questionId,
            String questionText,
            String optionA,
            String optionB,
            String optionC,
            String optionD,
            Character correctAnswer,
            Integer marks,
            Question.DifficultyLevel difficultyLevel) {

        Question existingQuestion =
                questionRepository.findById(questionId)
                        .orElseThrow(() ->
                                new RuntimeException(
                                        "Question not found"));

        if (correctAnswer == null ||
                !isValidAnswer(correctAnswer)) {

            throw new RuntimeException(
                    "Correct answer must be A, B, C, or D");
        }

        existingQuestion.setQuestionText(questionText);
        existingQuestion.setOptionA(optionA);
        existingQuestion.setOptionB(optionB);
        existingQuestion.setOptionC(optionC);
        existingQuestion.setOptionD(optionD);
        existingQuestion.setCorrectAnswer(
                Character.toUpperCase(correctAnswer)
        );
        existingQuestion.setMarks(
                marks != null ? marks : 1
        );
        existingQuestion.setDifficultyLevel(
                difficultyLevel != null
                        ? difficultyLevel
                        : Question.DifficultyLevel.EASY
        );

        return questionRepository.save(existingQuestion);
    }

    // Delete question
    public void deleteQuestion(Long questionId) {

        Question question =
                questionRepository.findById(questionId)
                        .orElseThrow(() ->
                                new RuntimeException(
                                        "Question not found"));

        Assessment assessment =
                question.getAssessment();

        questionRepository.delete(question);

        // Decrease total question count
        if (assessment != null &&
                assessment.getTotalQuestions() != null &&
                assessment.getTotalQuestions() > 0) {

            assessment.setTotalQuestions(
                    assessment.getTotalQuestions() - 1
            );

            assessmentRepository.save(assessment);
        }
    }

    private boolean isValidAnswer(Character answer) {

        char value =
                Character.toUpperCase(answer);

        return value == 'A' ||
                value == 'B' ||
                value == 'C' ||
                value == 'D';
    }
}