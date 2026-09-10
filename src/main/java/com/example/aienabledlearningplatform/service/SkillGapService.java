package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.EmployeeCompetency;
import com.example.aienabledlearningplatform.entity.SkillGap;
import com.example.aienabledlearningplatform.repository.EmployeeCompetencyRepository;
import com.example.aienabledlearningplatform.repository.SkillGapRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;

@Service
public class SkillGapService {

    private final SkillGapRepository skillGapRepository;
    private final EmployeeCompetencyRepository employeeCompetencyRepository;

    public SkillGapService(
            SkillGapRepository skillGapRepository,
            EmployeeCompetencyRepository employeeCompetencyRepository) {

        this.skillGapRepository = skillGapRepository;
        this.employeeCompetencyRepository = employeeCompetencyRepository;
    }

    // Get all skill gaps of an employee
    public List<SkillGap> getEmployeeSkillGaps(Long employeeId) {

        return skillGapRepository
                .findByEmployeeEmployeeId(employeeId);
    }

    // Get one specific skill gap
    public SkillGap getSkillGap(
            Long employeeId,
            Long competencyId) {

        return skillGapRepository
                .findByEmployeeEmployeeIdAndCompetencyCompetencyId(
                        employeeId,
                        competencyId
                )
                .orElseThrow(() ->
                        new RuntimeException(
                                "Skill gap not found"
                        ));
    }

    // Automatically calculate and create/update skill gap
    public SkillGap calculateSkillGap(
            Long employeeId,
            Long competencyId) {

        EmployeeCompetency employeeCompetency =
                employeeCompetencyRepository
                        .findByEmployeeEmployeeIdAndCompetencyCompetencyId(
                                employeeId,
                                competencyId
                        )
                        .orElseThrow(() ->
                                new RuntimeException(
                                        "Employee competency not found"
                                ));

        Integer currentLevel =
                employeeCompetency.getProficiencyLevel();

        Integer requiredLevel =
                employeeCompetency.getTargetLevel();

        if (currentLevel == null) {
            currentLevel = 0;
        }

        if (requiredLevel == null) {
            requiredLevel = 5;
        }

        // Calculate raw gap
        int gap = requiredLevel - currentLevel;

        // Calculate gap score as percentage
        BigDecimal gapScore;

        if (requiredLevel <= 0) {
            gapScore = BigDecimal.ZERO;
        } else {
            gapScore = BigDecimal.valueOf(gap)
                    .divide(
                            BigDecimal.valueOf(requiredLevel),
                            2,
                            RoundingMode.HALF_UP
                    )
                    .multiply(BigDecimal.valueOf(100));
        }

        // Prevent negative score
        if (gapScore.compareTo(BigDecimal.ZERO) < 0) {
            gapScore = BigDecimal.ZERO;
        }

        // Maximum score = 100
        if (gapScore.compareTo(BigDecimal.valueOf(100)) > 0) {
            gapScore = BigDecimal.valueOf(100);
        }

        SkillGap skillGap =
                skillGapRepository
                        .findByEmployeeEmployeeIdAndCompetencyCompetencyId(
                                employeeId,
                                competencyId
                        )
                        .orElseGet(SkillGap::new);

        skillGap.setEmployee(
                employeeCompetency.getEmployee()
        );

        skillGap.setCompetency(
                employeeCompetency.getCompetency()
        );

        skillGap.setCurrentLevel(currentLevel);
        skillGap.setRequiredLevel(requiredLevel);
        skillGap.setGapScore(gapScore);

        // Determine priority
        if (gap <= 0) {

            skillGap.setPriority(
                    SkillGap.Priority.LOW
            );

            skillGap.setStatus(
                    SkillGap.Status.RESOLVED
            );

        } else if (gapScore.compareTo(
                BigDecimal.valueOf(20)) <= 0) {

            skillGap.setPriority(
                    SkillGap.Priority.LOW
            );

            skillGap.setStatus(
                    SkillGap.Status.OPEN
            );

        } else if (gapScore.compareTo(
                BigDecimal.valueOf(40)) <= 0) {

            skillGap.setPriority(
                    SkillGap.Priority.MEDIUM
            );

            skillGap.setStatus(
                    SkillGap.Status.OPEN
            );

        } else if (gapScore.compareTo(
                BigDecimal.valueOf(60)) <= 0) {

            skillGap.setPriority(
                    SkillGap.Priority.HIGH
            );

            skillGap.setStatus(
                    SkillGap.Status.OPEN
            );

        } else {

            skillGap.setPriority(
                    SkillGap.Priority.CRITICAL
            );

            skillGap.setStatus(
                    SkillGap.Status.OPEN
            );
        }

        return skillGapRepository.save(skillGap);
    }
}