package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.Assessment;
import com.example.aienabledlearningplatform.entity.Competency;
import com.example.aienabledlearningplatform.entity.Employee;
import com.example.aienabledlearningplatform.repository.AssessmentRepository;
import com.example.aienabledlearningplatform.repository.CompetencyRepository;
import com.example.aienabledlearningplatform.repository.EmployeeRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AssessmentService {

    private final AssessmentRepository assessmentRepository;
    private final EmployeeRepository employeeRepository;
    private final CompetencyRepository competencyRepository;

    public AssessmentService(
            AssessmentRepository assessmentRepository,
            EmployeeRepository employeeRepository,
            CompetencyRepository competencyRepository) {

        this.assessmentRepository = assessmentRepository;
        this.employeeRepository = employeeRepository;
        this.competencyRepository = competencyRepository;
    }

    // Get all assessments
    public List<Assessment> getAllAssessments() {
        return assessmentRepository.findAll();
    }

    // Get assessment by ID
    public Assessment getAssessmentById(Long assessmentId) {
        return assessmentRepository.findById(assessmentId)
                .orElseThrow(() ->
                        new RuntimeException("Assessment not found"));
    }

    // Get assessments for an employee
    public List<Assessment> getEmployeeAssessments(Long employeeId) {

        if (!employeeRepository.existsById(employeeId)) {
            throw new RuntimeException("Employee not found");
        }

        return assessmentRepository
                .findByEmployeeEmployeeId(employeeId);
    }

    // Get assessments for a competency
    public List<Assessment> getCompetencyAssessments(
            Long competencyId) {

        if (!competencyRepository.existsById(competencyId)) {
            throw new RuntimeException("Competency not found");
        }

        return assessmentRepository
                .findByCompetencyCompetencyId(competencyId);
    }

    // Create assessment
    public Assessment createAssessment(
            Long employeeId,
            Long competencyId,
            String assessmentName,
            String description,
            Integer passingScore,
            Assessment.Status status) {

        Employee employee = employeeRepository
                .findById(employeeId)
                .orElseThrow(() ->
                        new RuntimeException("Employee not found"));

        Competency competency = null;

        if (competencyId != null) {
            competency = competencyRepository
                    .findById(competencyId)
                    .orElseThrow(() ->
                            new RuntimeException(
                                    "Competency not found"));
        }

        Assessment assessment = new Assessment();

        assessment.setEmployee(employee);
        assessment.setCompetency(competency);
        assessment.setAssessmentName(assessmentName);
        assessment.setDescription(description);
        assessment.setTotalQuestions(0);
        assessment.setPassingScore(passingScore);
        assessment.setStatus(status);

        return assessmentRepository.save(assessment);
    }

    // Update assessment
    public Assessment updateAssessment(
            Long assessmentId,
            Long competencyId,
            String assessmentName,
            String description,
            Integer passingScore,
            Assessment.Status status) {

        Assessment existingAssessment =
                assessmentRepository.findById(assessmentId)
                        .orElseThrow(() ->
                                new RuntimeException(
                                        "Assessment not found"));

        Competency competency = null;

        if (competencyId != null) {
            competency = competencyRepository
                    .findById(competencyId)
                    .orElseThrow(() ->
                            new RuntimeException(
                                    "Competency not found"));
        }

        existingAssessment.setCompetency(competency);
        existingAssessment.setAssessmentName(assessmentName);
        existingAssessment.setDescription(description);
        existingAssessment.setPassingScore(passingScore);
        existingAssessment.setStatus(status);

        return assessmentRepository.save(existingAssessment);
    }

    // Update assessment status
    public Assessment updateStatus(
            Long assessmentId,
            Assessment.Status status) {

        Assessment assessment = getAssessmentById(assessmentId);

        assessment.setStatus(status);

        return assessmentRepository.save(assessment);
    }

    // Delete assessment
    public void deleteAssessment(Long assessmentId) {

        if (!assessmentRepository.existsById(assessmentId)) {
            throw new RuntimeException("Assessment not found");
        }

        assessmentRepository.deleteById(assessmentId);
    }
}