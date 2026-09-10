package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.Employee;
import com.example.aienabledlearningplatform.entity.EmployeeCompetency;
import com.example.aienabledlearningplatform.entity.Competency;
import com.example.aienabledlearningplatform.repository.EmployeeCompetencyRepository;
import com.example.aienabledlearningplatform.repository.EmployeeRepository;
import com.example.aienabledlearningplatform.repository.CompetencyRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class EmployeeCompetencyService {

    private final EmployeeCompetencyRepository employeeCompetencyRepository;
    private final EmployeeRepository employeeRepository;
    private final CompetencyRepository competencyRepository;

    public EmployeeCompetencyService(
            EmployeeCompetencyRepository employeeCompetencyRepository,
            EmployeeRepository employeeRepository,
            CompetencyRepository competencyRepository) {

        this.employeeCompetencyRepository = employeeCompetencyRepository;
        this.employeeRepository = employeeRepository;
        this.competencyRepository = competencyRepository;
    }

    public List<EmployeeCompetency> getEmployeeCompetencies(
            Long employeeId) {

        return employeeCompetencyRepository
                .findByEmployeeEmployeeId(employeeId);
    }

    public EmployeeCompetency getEmployeeCompetency(
            Long employeeId,
            Long competencyId) {

        return employeeCompetencyRepository
                .findByEmployeeEmployeeIdAndCompetencyCompetencyId(
                        employeeId,
                        competencyId
                )
                .orElseThrow(() ->
                        new RuntimeException(
                                "Employee competency not found"
                        ));
    }

    public EmployeeCompetency assignCompetency(
            Long employeeId,
            Long competencyId,
            Integer proficiencyLevel,
            Integer targetLevel) {

        Employee employee = employeeRepository
                .findById(employeeId)
                .orElseThrow(() ->
                        new RuntimeException("Employee not found"));

        Competency competency = competencyRepository
                .findById(competencyId)
                .orElseThrow(() ->
                        new RuntimeException("Competency not found"));

        if (employeeCompetencyRepository
                .findByEmployeeEmployeeIdAndCompetencyCompetencyId(
                        employeeId,
                        competencyId
                ).isPresent()) {

            throw new RuntimeException(
                    "Competency already assigned to employee"
            );
        }

        EmployeeCompetency employeeCompetency =
                new EmployeeCompetency();

        employeeCompetency.setEmployee(employee);
        employeeCompetency.setCompetency(competency);
        employeeCompetency.setProficiencyLevel(proficiencyLevel);
        employeeCompetency.setTargetLevel(targetLevel);
        employeeCompetency.setLastAssessedDate(LocalDate.now());

        return employeeCompetencyRepository.save(
                employeeCompetency
        );
    }

    public EmployeeCompetency updateCompetency(
            Long employeeId,
            Long competencyId,
            Integer proficiencyLevel,
            Integer targetLevel) {

        EmployeeCompetency existing =
                getEmployeeCompetency(
                        employeeId,
                        competencyId
                );

        existing.setProficiencyLevel(proficiencyLevel);
        existing.setTargetLevel(targetLevel);
        existing.setLastAssessedDate(LocalDate.now());

        return employeeCompetencyRepository.save(existing);
    }
}