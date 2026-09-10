package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.Assessment;
import com.example.aienabledlearningplatform.entity.Employee;
import com.example.aienabledlearningplatform.entity.Question;
import com.example.aienabledlearningplatform.entity.QuizAnswer;
import com.example.aienabledlearningplatform.entity.QuizResult;
import com.example.aienabledlearningplatform.repository.AssessmentRepository;
import com.example.aienabledlearningplatform.repository.EmployeeRepository;
import com.example.aienabledlearningplatform.repository.QuestionRepository;
import com.example.aienabledlearningplatform.repository.QuizAnswerRepository;
import com.example.aienabledlearningplatform.repository.QuizResultRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Service
public class QuizResultService {

    private final QuizResultRepository quizResultRepository;
    private final QuizAnswerRepository quizAnswerRepository;
    private final EmployeeRepository employeeRepository;
    private final AssessmentRepository assessmentRepository;
    private final QuestionRepository questionRepository;

    public QuizResultService(
            QuizResultRepository quizResultRepository,
            QuizAnswerRepository quizAnswerRepository,
            EmployeeRepository employeeRepository,
            AssessmentRepository assessmentRepository,
            QuestionRepository questionRepository) {

        this.quizResultRepository = quizResultRepository;
        this.quizAnswerRepository = quizAnswerRepository;
        this.employeeRepository = employeeRepository;
        this.assessmentRepository = assessmentRepository;
        this.questionRepository = questionRepository;
    }

    // Get all quiz results
    public List<QuizResult> getAllResults() {
        return quizResultRepository.findAll();
    }

    // Get result by ID
    public QuizResult getResultById(Long resultId) {

        return quizResultRepository.findById(resultId)
                .orElseThrow(() ->
                        new RuntimeException("Quiz result not found"));
    }

    // Get all results of an employee
    public List<QuizResult> getEmployeeResults(Long employeeId) {

        if (!employeeRepository.existsById(employeeId)) {
            throw new RuntimeException("Employee not found");
        }

        return quizResultRepository
                .findByEmployeeEmployeeId(employeeId);
    }

    // Get all results of an assessment
    public List<QuizResult> getAssessmentResults(Long assessmentId) {

        if (!assessmentRepository.existsById(assessmentId)) {
            throw new RuntimeException("Assessment not found");
        }

        return quizResultRepository
                .findByAssessmentAssessmentId(assessmentId);
    }

    // Get answers of a quiz result
    public List<QuizAnswer> getResultAnswers(Long resultId) {

        if (!quizResultRepository.existsById(resultId)) {
            throw new RuntimeException("Quiz result not found");
        }

        return quizAnswerRepository
                .findByResultResultId(resultId);
    }

    // Submit quiz and calculate result
    @Transactional
    public QuizResult submitQuiz(
            Long employeeId,
            Long assessmentId,
            Map<Long, Character> answers) {

        Employee employee = employeeRepository
                .findById(employeeId)
                .orElseThrow(() ->
                        new RuntimeException("Employee not found"));

        Assessment assessment = assessmentRepository
                .findById(assessmentId)
                .orElseThrow(() ->
                        new RuntimeException("Assessment not found"));

        if (assessment.getStatus() != Assessment.Status.ACTIVE) {
            throw new RuntimeException(
                    "Assessment is not active");
        }

        if (answers == null || answers.isEmpty()) {
            throw new RuntimeException(
                    "No answers submitted");
        }

        List<Question> questions =
                questionRepository
                        .findByAssessmentAssessmentId(
                                assessmentId);

        if (questions.isEmpty()) {
            throw new RuntimeException(
                    "Assessment has no questions");
        }

        BigDecimal score = BigDecimal.ZERO;
        BigDecimal totalMarks = BigDecimal.ZERO;

        QuizResult quizResult = new QuizResult();

        quizResult.setEmployee(employee);
        quizResult.setAssessment(assessment);
        quizResult.setAttemptedAt(LocalDateTime.now());

        // Calculate total marks
        for (Question question : questions) {

            if (question.getMarks() != null) {

                totalMarks = totalMarks.add(
                        BigDecimal.valueOf(
                                question.getMarks()
                        )
                );
            }
        }

        // Save initial result
        quizResult.setScore(BigDecimal.ZERO);
        quizResult.setTotalMarks(totalMarks);
        quizResult.setPercentage(BigDecimal.ZERO);
        quizResult.setPassed(false);

        QuizResult savedResult =
                quizResultRepository.save(quizResult);

        // Evaluate each answer
        for (Question question : questions) {

            Character selectedAnswer =
                    answers.get(question.getQuestionId());

            if (selectedAnswer == null) {
                continue;
            }

            selectedAnswer =
                    Character.toUpperCase(selectedAnswer);

            boolean correct =
                    selectedAnswer.equals(
                            Character.toUpperCase(
                                    question.getCorrectAnswer()
                            )
                    );

            BigDecimal marksObtained =
                    correct
                            ? BigDecimal.valueOf(
                            question.getMarks()
                    )
                            : BigDecimal.ZERO;

            if (correct) {
                score = score.add(marksObtained);
            }

            QuizAnswer quizAnswer =
                    new QuizAnswer();

            quizAnswer.setResult(savedResult);
            quizAnswer.setQuestion(question);
            quizAnswer.setSelectedAnswer(selectedAnswer);
            quizAnswer.setIsCorrect(correct);
            quizAnswer.setMarksObtained(marksObtained);

            quizAnswerRepository.save(quizAnswer);
        }

        // Calculate percentage
        BigDecimal percentage =
                BigDecimal.ZERO;

        if (totalMarks.compareTo(BigDecimal.ZERO) > 0) {

            percentage = score
                    .multiply(BigDecimal.valueOf(100))
                    .divide(
                            totalMarks,
                            2,
                            RoundingMode.HALF_UP
                    );
        }

        // Determine pass/fail
        BigDecimal passingScore =
                assessment.getPassingScore() != null
                        ? BigDecimal.valueOf(
                        assessment.getPassingScore())
                        : BigDecimal.ZERO;

        boolean passed =
                percentage.compareTo(passingScore) >= 0;

        savedResult.setScore(score);
        savedResult.setTotalMarks(totalMarks);
        savedResult.setPercentage(percentage);
        savedResult.setPassed(passed);

        return quizResultRepository.save(savedResult);
    }
}