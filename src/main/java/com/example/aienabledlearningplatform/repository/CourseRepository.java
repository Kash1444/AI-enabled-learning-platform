package com.example.aienabledlearningplatform.repository;

import com.example.aienabledlearningplatform.entity.Course;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CourseRepository
        extends JpaRepository<Course, Long> {

    List<Course> findByCompetencyCompetencyId(Long competencyId);

    List<Course> findByStatus(Course.Status status);
}