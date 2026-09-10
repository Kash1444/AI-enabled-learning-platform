package com.example.aienabledlearningplatform.service;

import com.example.aienabledlearningplatform.entity.Course;
import com.example.aienabledlearningplatform.entity.CourseRecommendation;
import com.example.aienabledlearningplatform.entity.SkillGap;
import com.example.aienabledlearningplatform.repository.CourseRecommendationRepository;
import com.example.aienabledlearningplatform.repository.CourseRepository;
import com.example.aienabledlearningplatform.repository.SkillGapRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class CourseRecommendationService {

    private final CourseRecommendationRepository recommendationRepository;
    private final SkillGapRepository skillGapRepository;
    private final CourseRepository courseRepository;

    public CourseRecommendationService(
            CourseRecommendationRepository recommendationRepository,
            SkillGapRepository skillGapRepository,
            CourseRepository courseRepository) {

        this.recommendationRepository = recommendationRepository;
        this.skillGapRepository = skillGapRepository;
        this.courseRepository = courseRepository;
    }

    // Get all recommendations for an employee
    public List<CourseRecommendation> getEmployeeRecommendations(
            Long employeeId) {

        return recommendationRepository
                .findByEmployeeEmployeeId(employeeId);
    }

    // Get only active recommendations
    public List<CourseRecommendation> getActiveRecommendations(
            Long employeeId) {

        List<CourseRecommendation> recommendations =
                recommendationRepository
                        .findByEmployeeEmployeeIdAndStatus(
                                employeeId,
                                CourseRecommendation.Status.RECOMMENDED
                        );

        recommendations.addAll(
                recommendationRepository
                        .findByEmployeeEmployeeIdAndStatus(
                                employeeId,
                                CourseRecommendation.Status.STARTED
                        )
        );

        return recommendations;
    }

    // Generate recommendations from employee skill gaps
    public List<CourseRecommendation> generateRecommendations(
            Long employeeId) {

        List<SkillGap> skillGaps =
                skillGapRepository
                        .findByEmployeeEmployeeId(employeeId);

        List<CourseRecommendation> recommendations =
                new ArrayList<>();

        for (SkillGap skillGap : skillGaps) {

            // Ignore resolved gaps
            if (skillGap.getStatus() ==
                    SkillGap.Status.RESOLVED) {
                continue;
            }

            Long competencyId =
                    skillGap.getCompetency()
                            .getCompetencyId();

            List<Course> courses =
                    courseRepository
                            .findByCompetencyCompetencyId(
                                    competencyId
                            );

            for (Course course : courses) {

                // Only recommend active courses
                if (course.getStatus() !=
                        Course.Status.ACTIVE) {
                    continue;
                }

                // Avoid duplicate recommendation
                if (recommendationRepository
                        .findByEmployeeEmployeeIdAndCourseCourseId(
                                employeeId,
                                course.getCourseId()
                        )
                        .isPresent()) {
                    continue;
                }

                BigDecimal score =
                        calculateRecommendationScore(
                                skillGap,
                                course
                        );

                CourseRecommendation recommendation =
                        new CourseRecommendation();

                recommendation.setEmployee(
                        skillGap.getEmployee()
                );

                recommendation.setCourse(course);

                recommendation.setSkillGap(skillGap);

                recommendation.setRecommendationScore(score);

                recommendation.setReason(
                        buildRecommendationReason(
                                skillGap,
                                course
                        )
                );

                recommendation.setStatus(
                        CourseRecommendation.Status.RECOMMENDED
                );

                recommendation.setRecommendedAt(
                        LocalDateTime.now()
                );

                recommendations.add(
                        recommendationRepository.save(
                                recommendation
                        )
                );
            }
        }

        return recommendations;
    }

    // Calculate recommendation score
    private BigDecimal calculateRecommendationScore(
            SkillGap skillGap,
            Course course) {

        BigDecimal gapScore =
                skillGap.getGapScore();

        if (gapScore == null) {
            gapScore = BigDecimal.ZERO;
        }

        /*
         * Basic scoring:
         * Higher skill gap = higher recommendation priority.
         *
         * Current gap score is already between 0 and 100.
         */
        BigDecimal score = gapScore;

        // Give a small boost to higher-priority gaps
        switch (skillGap.getPriority()) {

            case CRITICAL:
                score = score.add(BigDecimal.valueOf(15));
                break;

            case HIGH:
                score = score.add(BigDecimal.valueOf(10));
                break;

            case MEDIUM:
                score = score.add(BigDecimal.valueOf(5));
                break;

            case LOW:
                break;
        }

        // Cap score at 100
        if (score.compareTo(
                BigDecimal.valueOf(100)
        ) > 0) {

            score = BigDecimal.valueOf(100);
        }

        return score.setScale(
                2,
                RoundingMode.HALF_UP
        );
    }

    // Build explanation for recommendation
    private String buildRecommendationReason(
            SkillGap skillGap,
            Course course) {

        return "Recommended for "
                + skillGap.getCompetency()
                .getCompetencyName()
                + " because the employee has a "
                + skillGap.getPriority()
                + "-priority skill gap with "
                + skillGap.getGapScore()
                + "% gap score. "
                + "Course difficulty: "
                + course.getDifficultyLevel()
                + ".";
    }

    // Update recommendation status
    public CourseRecommendation updateStatus(
            Long recommendationId,
            CourseRecommendation.Status status) {

        CourseRecommendation recommendation =
                recommendationRepository
                        .findById(recommendationId)
                        .orElseThrow(() ->
                                new RuntimeException(
                                        "Recommendation not found"
                                ));

        recommendation.setStatus(status);

        return recommendationRepository.save(
                recommendation
        );
    }
}