package com.example.aienabledlearningplatform.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "competencies")
public class Competency {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "competency_id")
    private Long competencyId;

    @Column(name = "competency_name", nullable = false, unique = true)
    private String competencyName;

    @Column(columnDefinition = "TEXT")
    private String description;

    private String category;

    @Column(name = "proficiency_levels", columnDefinition = "TEXT")
    private String proficiencyLevels;

    public Long getCompetencyId() {
        return competencyId;
    }

    public void setCompetencyId(Long competencyId) {
        this.competencyId = competencyId;
    }

    public String getCompetencyName() {
        return competencyName;
    }

    public void setCompetencyName(String competencyName) {
        this.competencyName = competencyName;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getProficiencyLevels() {
        return proficiencyLevels;
    }

    public void setProficiencyLevels(String proficiencyLevels) {
        this.proficiencyLevels = proficiencyLevels;
    }
}