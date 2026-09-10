package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.Competency;
import com.example.aienabledlearningplatform.service.CompetencyService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/competencies")
public class CompetencyController {

    private final CompetencyService competencyService;

    public CompetencyController(CompetencyService competencyService) {
        this.competencyService = competencyService;
    }

    // Get all competencies
    @GetMapping
    public ResponseEntity<List<Competency>> getAllCompetencies() {

        return ResponseEntity.ok(
                competencyService.getAllCompetencies()
        );
    }

    // Get competency by ID
    @GetMapping("/{competencyId}")
    public ResponseEntity<Competency> getCompetencyById(
            @PathVariable Long competencyId) {

        return ResponseEntity.ok(
                competencyService.getCompetencyById(competencyId)
        );
    }

    // Create competency
    @PostMapping
    public ResponseEntity<Competency> createCompetency(
            @RequestBody Competency competency) {

        return ResponseEntity.ok(
                competencyService.createCompetency(competency)
        );
    }

    // Update competency
    @PutMapping("/{competencyId}")
    public ResponseEntity<Competency> updateCompetency(
            @PathVariable Long competencyId,
            @RequestBody Competency competency) {

        return ResponseEntity.ok(
                competencyService.updateCompetency(
                        competencyId,
                        competency
                )
        );
    }

    // Delete competency
    @DeleteMapping("/{competencyId}")
    public ResponseEntity<String> deleteCompetency(
            @PathVariable Long competencyId) {

        competencyService.deleteCompetency(competencyId);

        return ResponseEntity.ok(
                "Competency deleted successfully"
        );
    }
}