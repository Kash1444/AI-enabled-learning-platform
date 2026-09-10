package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.SkillGap;
import com.example.aienabledlearningplatform.service.SkillGapService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/skill-gaps")
public class SkillGapController {

    private final SkillGapService skillGapService;

    public SkillGapController(SkillGapService skillGapService) {
        this.skillGapService = skillGapService;
    }

    // Get all skill gaps of an employee
    @GetMapping("/employee/{employeeId}")
    public ResponseEntity<List<SkillGap>> getEmployeeSkillGaps(
            @PathVariable Long employeeId) {

        return ResponseEntity.ok(
                skillGapService.getEmployeeSkillGaps(employeeId)
        );
    }

    // Get one specific skill gap
    @GetMapping("/employee/{employeeId}/competency/{competencyId}")
    public ResponseEntity<SkillGap> getSkillGap(
            @PathVariable Long employeeId,
            @PathVariable Long competencyId) {

        return ResponseEntity.ok(
                skillGapService.getSkillGap(
                        employeeId,
                        competencyId
                )
        );
    }

    // Calculate skill gap automatically
    @PostMapping("/employee/{employeeId}/competency/{competencyId}/calculate")
    public ResponseEntity<SkillGap> calculateSkillGap(
            @PathVariable Long employeeId,
            @PathVariable Long competencyId) {

        return ResponseEntity.ok(
                skillGapService.calculateSkillGap(
                        employeeId,
                        competencyId
                )
        );
    }
}