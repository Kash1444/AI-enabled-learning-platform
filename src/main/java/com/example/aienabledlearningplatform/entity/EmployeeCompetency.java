package com.example.aienabledlearningplatform.entity;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(
        name = "employee_competencies",
        uniqueConstraints = @UniqueConstraint(
                columnNames = {"employee_id", "competency_id"}
        )
)
public class EmployeeCompetency {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "employee_competency_id")
    private Long employeeCompetencyId;

    @ManyToOne
    @JoinColumn(name = "employee_id", nullable = false)
    private Employee employee;

    @ManyToOne
    @JoinColumn(name = "competency_id", nullable = false)
    private Competency competency;

    @Column(name = "proficiency_level")
    private Integer proficiencyLevel;

    @Column(name = "target_level")
    private Integer targetLevel;

    @Column(name = "last_assessed_date")
    private LocalDate lastAssessedDate;

    public Long getEmployeeCompetencyId() {
        return employeeCompetencyId;
    }

    public void setEmployeeCompetencyId(Long employeeCompetencyId) {
        this.employeeCompetencyId = employeeCompetencyId;
    }

    public Employee getEmployee() {
        return employee;
    }

    public void setEmployee(Employee employee) {
        this.employee = employee;
    }

    public Competency getCompetency() {
        return competency;
    }

    public void setCompetency(Competency competency) {
        this.competency = competency;
    }

    public Integer getProficiencyLevel() {
        return proficiencyLevel;
    }

    public void setProficiencyLevel(Integer proficiencyLevel) {
        this.proficiencyLevel = proficiencyLevel;
    }

    public Integer getTargetLevel() {
        return targetLevel;
    }

    public void setTargetLevel(Integer targetLevel) {
        this.targetLevel = targetLevel;
    }

    public LocalDate getLastAssessedDate() {
        return lastAssessedDate;
    }

    public void setLastAssessedDate(LocalDate lastAssessedDate) {
        this.lastAssessedDate = lastAssessedDate;
    }
}