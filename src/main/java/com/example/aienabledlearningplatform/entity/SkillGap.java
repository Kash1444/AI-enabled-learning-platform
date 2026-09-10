package com.example.aienabledlearningplatform.entity;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "skill_gaps")
public class SkillGap {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "skill_gap_id")
    private Long skillGapId;

    @ManyToOne
    @JoinColumn(name = "employee_id", nullable = false)
    private Employee employee;

    @ManyToOne
    @JoinColumn(name = "competency_id", nullable = false)
    private Competency competency;

    @Column(name = "current_level", nullable = false)
    private Integer currentLevel = 0;

    @Column(name = "required_level", nullable = false)
    private Integer requiredLevel = 5;

    @Column(name = "gap_score")
    private BigDecimal gapScore;

    @Enumerated(EnumType.STRING)
    @Column(name = "priority")
    private Priority priority = Priority.MEDIUM;

    @Column(name = "identified_at")
    private LocalDateTime identifiedAt;

    @Enumerated(EnumType.STRING)
    @Column(name = "status")
    private Status status = Status.OPEN;

    public enum Priority {
        LOW,
        MEDIUM,
        HIGH,
        CRITICAL
    }

    public enum Status {
        OPEN,
        IN_PROGRESS,
        RESOLVED
    }

    public Long getSkillGapId() {
        return skillGapId;
    }

    public void setSkillGapId(Long skillGapId) {
        this.skillGapId = skillGapId;
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

    public Integer getCurrentLevel() {
        return currentLevel;
    }

    public void setCurrentLevel(Integer currentLevel) {
        this.currentLevel = currentLevel;
    }

    public Integer getRequiredLevel() {
        return requiredLevel;
    }

    public void setRequiredLevel(Integer requiredLevel) {
        this.requiredLevel = requiredLevel;
    }

    public BigDecimal getGapScore() {
        return gapScore;
    }

    public void setGapScore(BigDecimal gapScore) {
        this.gapScore = gapScore;
    }

    public Priority getPriority() {
        return priority;
    }

    public void setPriority(Priority priority) {
        this.priority = priority;
    }

    public LocalDateTime getIdentifiedAt() {
        return identifiedAt;
    }

    public void setIdentifiedAt(LocalDateTime identifiedAt) {
        this.identifiedAt = identifiedAt;
    }

    public Status getStatus() {
        return status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }
}