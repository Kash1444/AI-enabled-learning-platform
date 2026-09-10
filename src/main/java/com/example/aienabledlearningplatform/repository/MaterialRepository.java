package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.Material;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface MaterialRepository extends JpaRepository<Material, Long> {

    List<Material> findByUserUserId(Long userId);

    List<Material> findByCourseCourseId(Long courseId);

    List<Material> findByMaterialType(Material.MaterialType materialType);
}