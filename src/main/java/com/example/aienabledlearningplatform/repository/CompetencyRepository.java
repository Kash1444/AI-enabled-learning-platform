package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.Competency;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CompetencyRepository
        extends JpaRepository<Competency, Long> {

    Optional<Competency> findByCompetencyName(String competencyName);
}