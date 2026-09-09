import { useState } from "react";
import { aiRecommendations } from "../../data/employeeData";
import "./LearningPath.css";

function LearningPath() {
  const [activeStep, setActiveStep] = useState(1);

  const learningSteps = [
    {
      id: 1,
      phase: "PHASE 01",
      title: "Strengthen Statistical Programming",
      skill: "Statistical Programming",
      priority: "High Priority",
      status: "In Progress",
      progress: 25,
      duration: "8 hours",
      description:
        "Build stronger programming skills for statistical analysis, data processing and reproducible workflows.",
      course:
        "Statistical Programming with R",
      provider: "iGOT Karmayogi",
      icon: "💻",
    },

    {
      id: 2,
      phase: "PHASE 02",
      title: "Master Sampling Methodology",
      skill: "Sampling Methodology",
      priority: "High Priority",
      status: "Recommended",
      progress: 0,
      duration: "6 hours",
      description:
        "Strengthen sampling design, estimation techniques and official survey methodology.",
      course:
        "Sampling Techniques for Official Statistics",
      provider: "NSSTA TPAC",
      icon: "📊",
    },

    {
      id: 3,
      phase: "PHASE 03",
      title: "Improve Data Visualization",
      skill: "Data Visualization",
      priority: "Medium Priority",
      status: "Recommended",
      progress: 40,
      duration: "4 hours",
      description:
        "Develop stronger skills for communicating statistical insights through effective visual reporting.",
      course:
        "Data Visualization for Statistical Reporting",
      provider: "iGOT Karmayogi",
      icon: "📈",
    },

    {
      id: 4,
      phase: "PHASE 04",
      title: "Strengthen Digital Governance",
      skill: "Digital Governance",
      priority: "Medium Priority",
      status: "Recommended",
      progress: 0,
      duration: "5 hours",
      description:
        "Improve understanding of digital governance practices and data-driven public services.",
      course:
        "Digital Governance Fundamentals",
      provider: "iGOT Karmayogi",
      icon: "🏛️",
    },
  ];

  const completedCount = learningSteps.filter(
    (step) => step.progress === 100
  ).length;

  const totalHours = learningSteps.reduce(
    (total, step) => total + parseInt(step.duration),
    0
  );

  const overallProgress = Math.round(
    learningSteps.reduce((total, step) => total + step.progress, 0) /
      learningSteps.length
  );

  const handleStepClick = (id) => {
    setActiveStep(id);
  };

  return (
    <div className="learning-path-page">

      {/* ================= HEADER ================= */}

      <div className="learning-path-header">

        <div>
          <div className="learning-breadcrumb">
            Employee Portal / Learning Path
          </div>

          <h1>My Learning Path</h1>

          <p>
            Your AI-generated roadmap for closing competency gaps and
            building role-specific skills.
          </p>
        </div>

        <button className="ai-rebuild-button">
          ✨ Refresh AI Path
        </button>

      </div>


      {/* ================= AI SUMMARY ================= */}

      <section className="learning-ai-summary">

        <div className="ai-summary-icon">
          ✨
        </div>

        <div className="ai-summary-content">

          <div className="ai-summary-label">
            AI-PERSONALIZED LEARNING ROADMAP
          </div>

          <h2>
            Your learning path is optimized for your current skill gaps.
          </h2>

          <p>
            The AI engine prioritizes learning based on competency gaps,
            role requirements and your current learning progress.
          </p>

        </div>

        <div className="ai-summary-score">

          <div className="score-value">
            {overallProgress}%
          </div>

          <div className="score-label">
            Path Progress
          </div>

        </div>

      </section>


      {/* ================= SUMMARY STATS ================= */}

      <section className="learning-stats">

        <div className="learning-stat-card">

          <div className="stat-icon blue">
            🧭
          </div>

          <div>
            <strong>{learningSteps.length}</strong>
            <span>Learning Steps</span>
          </div>

        </div>


        <div className="learning-stat-card">

          <div className="stat-icon orange">
            ⏱
          </div>

          <div>
            <strong>{totalHours} hrs</strong>
            <span>Estimated Learning</span>
          </div>

        </div>


        <div className="learning-stat-card">

          <div className="stat-icon green">
            ✓
          </div>

          <div>
            <strong>{completedCount}</strong>
            <span>Completed</span>
          </div>

        </div>


        <div className="learning-stat-card">

          <div className="stat-icon purple">
            🎯
          </div>

          <div>
            <strong>4</strong>
            <span>Skills Targeted</span>
          </div>

        </div>

      </section>


      {/* ================= ROADMAP ================= */}

      <section className="roadmap-section">

        <div className="section-heading">

          <div>
            <h2>AI Learning Roadmap</h2>

            <p>
              Follow the recommended sequence to close your highest-priority
              competency gaps first.
            </p>
          </div>

          <div className="roadmap-legend">

            <span>
              <i className="legend-current"></i>
              Current
            </span>

            <span>
              <i className="legend-next"></i>
              Recommended
            </span>

          </div>

        </div>


        <div className="roadmap">

          <div className="roadmap-line"></div>

          {learningSteps.map((step) => (

            <div
              key={step.id}
              className={`roadmap-item ${
                activeStep === step.id
                  ? "roadmap-item-active"
                  : ""
              }`}
            >

              {/* Timeline */}

              <div className="roadmap-marker">

                <div
                  className={`roadmap-number ${
                    step.progress > 0
                      ? "roadmap-number-progress"
                      : ""
                  }`}
                >
                  {step.progress === 100
                    ? "✓"
                    : step.id}
                </div>

              </div>


              {/* Content */}

              <div className="roadmap-card">

                <div className="roadmap-card-top">

                  <div>

                    <div className="phase-label">
                      {step.phase}
                    </div>

                    <h3>
                      {step.title}
                    </h3>

                    <div className="skill-name">
                      Target skill:{" "}
                      <strong>{step.skill}</strong>
                    </div>

                  </div>

                  <div className="roadmap-icon">
                    {step.icon}
                  </div>

                </div>


                <div className="roadmap-tags">

                  <span
                    className={
                      step.priority.includes("High")
                        ? "priority-high"
                        : "priority-medium"
                    }
                  >
                    {step.priority}
                  </span>

                  <span className="status-tag">
                    {step.status}
                  </span>

                  <span className="duration-tag">
                    ⏱ {step.duration}
                  </span>

                </div>


                <p className="roadmap-description">
                  {step.description}
                </p>


                {/* Progress */}

                <div className="roadmap-progress-section">

                  <div className="progress-header">

                    <span>
                      Learning Progress
                    </span>

                    <strong>
                      {step.progress}%
                    </strong>

                  </div>

                  <div className="roadmap-progress-track">

                    <div
                      className="roadmap-progress-fill"
                      style={{
                        width: `${step.progress}%`,
                      }}
                    ></div>

                  </div>

                </div>


                {/* Course Recommendation */}

                <div className="course-recommendation">

                  <div className="course-recommendation-icon">
                    {step.icon}
                  </div>

                  <div className="course-recommendation-info">

                    <span>
                      AI Recommended Learning
                    </span>

                    <strong>
                      {step.course}
                    </strong>

                    <small>
                      {step.provider}
                    </small>

                  </div>

                  <button
                    className="course-action-button"
                    onClick={() =>
                      handleStepClick(step.id)
                    }
                  >
                    {step.progress > 0
                      ? "Continue"
                      : "Start Learning"}
                    <span>→</span>
                  </button>

                </div>

              </div>

            </div>

          ))}

        </div>

      </section>


      {/* ================= AI INSIGHT ================= */}

      <section className="learning-insight">

        <div className="insight-icon">
          ✨
        </div>

        <div className="insight-content">

          <div className="insight-title">
            AI Learning Insight
          </div>

          <p>
            Completing the first two learning steps is expected to address
            your highest-priority competency gaps in Statistical Programming
            and Sampling Methodology.
          </p>

        </div>

        <button className="insight-button">
          View Skill Gaps →
        </button>

      </section>

    </div>
  );
}

export default LearningPath;