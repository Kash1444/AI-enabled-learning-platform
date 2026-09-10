package com.example.aienabledlearningplatform.entity;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "course_recommendations")
public class CourseRecommendation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "recommendation_id")
    private Long recommendationId;

    @ManyToOne
    @JoinColumn(name = "employee_id", nullable = false)
    private Employee employee;

    @ManyToOne
    @JoinColumn(name = "course_id", nullable = false)
    private Course course;

    @ManyToOne
    @JoinColumn(name = "skill_gap_id")
    private SkillGap skillGap;

    @Column(name = "recommendation_score")
    private BigDecimal recommendationScore;

    @Column(columnDefinition = "TEXT")
    private String reason;

    @Enumerated(EnumType.STRING)
    @Column(name = "status")
    private Status status = Status.RECOMMENDED;

    @Column(name = "recommended_at")
    private LocalDateTime recommendedAt;

    public enum Status {
        RECOMMENDED,
        STARTED,
        COMPLETED,
        DISMISSED
    }

    public Long getRecommendationId() {
        return recommendationId;
    }

    public void setRecommendationId(Long recommendationId) {
        this.recommendationId = recommendationId;
    }

    public Employee getEmployee() {
        return employee;
    }

    public void setEmployee(Employee employee) {
        this.employee = employee;
    }

    public Course getCourse() {
        return course;
    }

    public void setCourse(Course course) {
        this.course = course;
    }

    public SkillGap getSkillGap() {
        return skillGap;
    }

    public void setSkillGap(SkillGap skillGap) {
        this.skillGap = skillGap;
    }

    public BigDecimal getRecommendationScore() {
        return recommendationScore;
    }

    public void setRecommendationScore(BigDecimal recommendationScore) {
        this.recommendationScore = recommendationScore;
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    public Status getStatus() {
        return status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }

    public LocalDateTime getRecommendedAt() {
        return recommendedAt;
    }

    public void setRecommendedAt(LocalDateTime recommendedAt) {
        this.recommendedAt = recommendedAt;
    }
}