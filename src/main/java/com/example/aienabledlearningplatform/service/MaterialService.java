package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.Course;
import com.example.aienabledlearningplatform.entity.Material;
import com.example.aienabledlearningplatform.entity.User;
import com.example.aienabledlearningplatform.repository.CourseRepository;
import com.example.aienabledlearningplatform.repository.MaterialRepository;
import com.example.aienabledlearningplatform.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class MaterialService {

    private final MaterialRepository materialRepository;
    private final UserRepository userRepository;
    private final CourseRepository courseRepository;

    public MaterialService(
            MaterialRepository materialRepository,
            UserRepository userRepository,
            CourseRepository courseRepository) {

        this.materialRepository = materialRepository;
        this.userRepository = userRepository;
        this.courseRepository = courseRepository;
    }

    // Get all materials
    public List<Material> getAllMaterials() {
        return materialRepository.findAll();
    }

    // Get material by ID
    public Material getMaterialById(Long materialId) {

        return materialRepository.findById(materialId)
                .orElseThrow(() ->
                        new RuntimeException("Material not found"));
    }

    // Get materials uploaded by a user
    public List<Material> getUserMaterials(Long userId) {

        if (!userRepository.existsById(userId)) {
            throw new RuntimeException("User not found");
        }

        return materialRepository.findByUserUserId(userId);
    }

    // Get materials for a course
    public List<Material> getCourseMaterials(Long courseId) {

        if (!courseRepository.existsById(courseId)) {
            throw new RuntimeException("Course not found");
        }

        return materialRepository.findByCourseCourseId(courseId);
    }

    // Get materials by type
    public List<Material> getMaterialsByType(
            Material.MaterialType materialType) {

        return materialRepository.findByMaterialType(
                materialType
        );
    }

    // Create material
    public Material createMaterial(
            Long userId,
            Long courseId,
            String title,
            String description,
            Material.MaterialType materialType,
            String materialUrl) {

        User user = userRepository.findById(userId)
                .orElseThrow(() ->
                        new RuntimeException("User not found"));

        Course course = null;

        if (courseId != null) {
            course = courseRepository.findById(courseId)
                    .orElseThrow(() ->
                            new RuntimeException("Course not found"));
        }

        if (title == null || title.isBlank()) {
            throw new RuntimeException(
                    "Material title is required");
        }

        if (materialType == null) {
            throw new RuntimeException(
                    "Material type is required");
        }

        if (materialUrl == null || materialUrl.isBlank()) {
            throw new RuntimeException(
                    "Material URL is required");
        }

        Material material = new Material();

        material.setUser(user);
        material.setCourse(course);
        material.setTitle(title);
        material.setDescription(description);
        material.setMaterialType(materialType);
        material.setMaterialUrl(materialUrl);
        material.setUploadedAt(LocalDateTime.now());

        return materialRepository.save(material);
    }

    // Update material
    public Material updateMaterial(
            Long materialId,
            Long courseId,
            String title,
            String description,
            Material.MaterialType materialType,
            String materialUrl) {

        Material existingMaterial =
                materialRepository.findById(materialId)
                        .orElseThrow(() ->
                                new RuntimeException(
                                        "Material not found"));

        Course course = null;

        if (courseId != null) {
            course = courseRepository.findById(courseId)
                    .orElseThrow(() ->
                            new RuntimeException(
                                    "Course not found"));
        }

        if (title == null || title.isBlank()) {
            throw new RuntimeException(
                    "Material title is required");
        }

        if (materialType == null) {
            throw new RuntimeException(
                    "Material type is required");
        }

        if (materialUrl == null || materialUrl.isBlank()) {
            throw new RuntimeException(
                    "Material URL is required");
        }

        existingMaterial.setCourse(course);
        existingMaterial.setTitle(title);
        existingMaterial.setDescription(description);
        existingMaterial.setMaterialType(materialType);
        existingMaterial.setMaterialUrl(materialUrl);

        return materialRepository.save(existingMaterial);
    }

    // Delete material
    public void deleteMaterial(Long materialId) {

        if (!materialRepository.existsById(materialId)) {
            throw new RuntimeException(
                    "Material not found");
        }

        materialRepository.deleteById(materialId);
    }
}