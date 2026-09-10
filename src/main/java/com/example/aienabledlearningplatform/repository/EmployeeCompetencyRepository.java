package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.EmployeeCompetency;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface EmployeeCompetencyRepository
        extends JpaRepository<EmployeeCompetency, Long> {

    List<EmployeeCompetency> findByEmployeeEmployeeId(Long employeeId);

    Optional<EmployeeCompetency> findByEmployeeEmployeeIdAndCompetencyCompetencyId(
            Long employeeId,
            Long competencyId
    );
}