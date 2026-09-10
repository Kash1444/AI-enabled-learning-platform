package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.SkillGap;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface SkillGapRepository
        extends JpaRepository<SkillGap, Long> {

    List<SkillGap> findByEmployeeEmployeeId(Long employeeId);

    Optional<SkillGap> findByEmployeeEmployeeIdAndCompetencyCompetencyId(
            Long employeeId,
            Long competencyId
    );
}