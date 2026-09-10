package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.Competency;
import com.example.aienabledlearningplatform.repository.CompetencyRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CompetencyService {

    private final CompetencyRepository competencyRepository;

    public CompetencyService(CompetencyRepository competencyRepository) {
        this.competencyRepository = competencyRepository;
    }

    // Get all competencies
    public List<Competency> getAllCompetencies() {
        return competencyRepository.findAll();
    }

    // Get competency by ID
    public Competency getCompetencyById(Long competencyId) {

        return competencyRepository.findById(competencyId)
                .orElseThrow(() ->
                        new RuntimeException("Competency not found"));
    }

    // Create competency
    public Competency createCompetency(Competency competency) {
        return competencyRepository.save(competency);
    }

    // Update competency
    public Competency updateCompetency(
            Long competencyId,
            Competency updatedCompetency) {

        Competency existing =
                competencyRepository.findById(competencyId)
                        .orElseThrow(() ->
                                new RuntimeException("Competency not found"));

        existing.setCompetencyName(
                updatedCompetency.getCompetencyName());

        existing.setDescription(
                updatedCompetency.getDescription());

        existing.setCategory(
                updatedCompetency.getCategory());

        existing.setProficiencyLevels(
                updatedCompetency.getProficiencyLevels());

        return competencyRepository.save(existing);
    }

    // Delete competency
    public void deleteCompetency(Long competencyId) {

        if (!competencyRepository.existsById(competencyId)) {
            throw new RuntimeException("Competency not found");
        }

        competencyRepository.deleteById(competencyId);
    }
}