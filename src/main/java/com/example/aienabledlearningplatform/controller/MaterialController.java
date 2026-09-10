package com.example.aienabledlearningplatform.controller;

import com.example.aienabledlearningplatform.entity.Material;
import com.example.aienabledlearningplatform.service.MaterialService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/materials")
public class MaterialController {

    private final MaterialService materialService;

    public MaterialController(MaterialService materialService) {
        this.materialService = materialService;
    }

    // Get all materials
    @GetMapping
    public ResponseEntity<List<Material>> getAllMaterials() {

        return ResponseEntity.ok(
                materialService.getAllMaterials()
        );
    }

    // Get material by ID
    @GetMapping("/{materialId}")
    public ResponseEntity<Material> getMaterialById(
            @PathVariable Long materialId) {

        return ResponseEntity.ok(
                materialService.getMaterialById(materialId)
        );
    }

    // Get materials uploaded by a user
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<Material>> getUserMaterials(
            @PathVariable Long userId) {

        return ResponseEntity.ok(
                materialService.getUserMaterials(userId)
        );
    }

    // Get materials associated with a course
    @GetMapping("/course/{courseId}")
    public ResponseEntity<List<Material>> getCourseMaterials(
            @PathVariable Long courseId) {

        return ResponseEntity.ok(
                materialService.getCourseMaterials(courseId)
        );
    }

    // Get materials by type
    @GetMapping("/type/{materialType}")
    public ResponseEntity<List<Material>> getMaterialsByType(
            @PathVariable Material.MaterialType materialType) {

        return ResponseEntity.ok(
                materialService.getMaterialsByType(
                        materialType
                )
        );
    }

    // Create material
    @PostMapping
    public ResponseEntity<Material> createMaterial(
            @RequestParam Long userId,
            @RequestParam(required = false) Long courseId,
            @RequestParam String title,
            @RequestParam(required = false) String description,
            @RequestParam Material.MaterialType materialType,
            @RequestParam String materialUrl) {

        return ResponseEntity.ok(
                materialService.createMaterial(
                        userId,
                        courseId,
                        title,
                        description,
                        materialType,
                        materialUrl
                )
        );
    }

    // Update material
    @PutMapping("/{materialId}")
    public ResponseEntity<Material> updateMaterial(
            @PathVariable Long materialId,
            @RequestParam(required = false) Long courseId,
            @RequestParam String title,
            @RequestParam(required = false) String description,
            @RequestParam Material.MaterialType materialType,
            @RequestParam String materialUrl) {

        return ResponseEntity.ok(
                materialService.updateMaterial(
                        materialId,
                        courseId,
                        title,
                        description,
                        materialType,
                        materialUrl
                )
        );
    }

    // Delete material
    @DeleteMapping("/{materialId}")
    public ResponseEntity<String> deleteMaterial(
            @PathVariable Long materialId) {

        materialService.deleteMaterial(materialId);

        return ResponseEntity.ok(
                "Material deleted successfully"
        );
    }
}