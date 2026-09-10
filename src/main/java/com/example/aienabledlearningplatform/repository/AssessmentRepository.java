package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.Assessment;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AssessmentRepository
        extends JpaRepository<Assessment, Long> {

    List<Assessment> findByEmployeeEmployeeId(Long employeeId);

    List<Assessment> findByCompetencyCompetencyId(Long competencyId);

    List<Assessment> findByEmployeeEmployeeIdAndStatus(
            Long employeeId,
            Assessment.Status status
    );
}