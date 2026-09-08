import { useNavigate } from "react-router-dom";
import { skillGaps } from "../../data/employeeData";
import "./SkillGaps.css";

function SkillGaps() {
  const navigate = useNavigate();

  const totalGaps = skillGaps.length;

  const highPriority = skillGaps.filter(
    (gap) => gap.priority === "High"
  ).length;

  const mediumPriority = skillGaps.filter(
    (gap) => gap.priority === "Medium"
  ).length;

  const totalGap = skillGaps.reduce(
    (sum, gap) => sum + gap.gap,
    0
  );

  const getPriorityClass = (priority) => {
    if (priority === "High") return "priority-high";
    if (priority === "Medium") return "priority-medium";
    return "priority-low";
  };

  return (
    <div className="skill-gaps-page">

      {/* ================= PAGE HEADER ================= */}

      <div className="skill-gaps-header">

        <div>
          <div className="skill-gaps-breadcrumb">
            Employee Portal / Skill Gaps
          </div>

          <h1>
            AI Skill Gap Analysis
          </h1>

          <p>
            Identify the competency areas that require improvement
            for your current role.
          </p>
        </div>

        <button
          className="skill-gaps-learning-button"
          onClick={() => navigate("/employee/learning-path")}
        >
          View Learning Path →
        </button>

      </div>


      {/* ================= SUMMARY ================= */}

      <section className="skill-gap-summary">

        <div className="gap-summary-card">

          <div className="gap-summary-icon blue">
            🎯
          </div>

          <div>
            <span>Total Skill Gaps</span>
            <strong>{totalGaps}</strong>
            <small>Areas requiring development</small>
          </div>

        </div>


        <div className="gap-summary-card">

          <div className="gap-summary-icon red">
            ⚠
          </div>

          <div>
            <span>High Priority</span>
            <strong>{highPriority}</strong>
            <small>Immediate attention recommended</small>
          </div>

        </div>


        <div className="gap-summary-card">

          <div className="gap-summary-icon orange">
            !
          </div>

          <div>
            <span>Medium Priority</span>
            <strong>{mediumPriority}</strong>
            <small>Development recommended</small>
          </div>

        </div>


        <div className="gap-summary-card">

          <div className="gap-summary-icon purple">
            📊
          </div>

          <div>
            <span>Total Competency Gap</span>
            <strong>{totalGap.toFixed(1)}</strong>
            <small>Across identified skill areas</small>
          </div>

        </div>

      </section>


      {/* ================= AI INSIGHT ================= */}

      <section className="ai-gap-banner">

        <div className="ai-gap-banner-icon">
          ✨
        </div>

        <div>

          <h2>
            AI Analysis
          </h2>

          <p>
            Your skill gaps are identified by comparing your current
            competency levels with the competency requirements for
            your role. Higher-priority gaps are recommended for
            immediate learning.
          </p>

        </div>

      </section>


      {/* ================= GAP LIST ================= */}

      <section className="skill-gap-section">

        <div className="section-heading">

          <div>
            <h2>
              Identified Skill Gaps
            </h2>

            <p>
              Current competency compared with the required level.
            </p>
          </div>

          <div className="gap-legend">

            <span>
              <i className="legend-high"></i>
              High Priority
            </span>

            <span>
              <i className="legend-medium"></i>
              Medium Priority
            </span>

          </div>

        </div>


        <div className="skill-gap-grid">

          {skillGaps.map((gap) => {

            const currentPercentage =
              (gap.current / 5) * 100;

            const requiredPercentage =
              (gap.required / 5) * 100;

            return (
              <article
                className="skill-gap-card"
                key={gap.skill}
              >

                {/* Card Header */}

                <div className="skill-gap-card-header">

                  <div>
                    <h3>
                      {gap.skill}
                    </h3>

                    <span
                      className={`priority-badge ${getPriorityClass(
                        gap.priority
                      )}`}
                    >
                      {gap.priority} Priority
                    </span>
                  </div>

                  <div className="gap-number">
                    {gap.gap.toFixed(1)}
                  </div>

                </div>


                {/* Description */}

                <p className="skill-gap-description">
                  {gap.description}
                </p>


                {/* Current */}

                <div className="gap-level-row">

                  <div className="gap-level-label">
                    <span>Current Level</span>
                    <strong>{gap.current}</strong>
                  </div>

                  <div className="gap-progress-track">

                    <div
                      className="gap-progress-current"
                      style={{
                        width: `${currentPercentage}%`,
                      }}
                    ></div>

                  </div>

                </div>


                {/* Required */}

                <div className="gap-level-row">

                  <div className="gap-level-label">
                    <span>Required Level</span>
                    <strong>{gap.required}</strong>
                  </div>

                  <div className="gap-progress-track required">

                    <div
                      className="gap-progress-required"
                      style={{
                        width: `${requiredPercentage}%`,
                      }}
                    ></div>

                  </div>

                </div>


                {/* Gap */}

                <div className="gap-result">

                  <span>
                    Competency Gap
                  </span>

                  <strong>
                    {gap.gap.toFixed(1)}
                  </strong>

                </div>


                {/* AI Recommendation */}

                <div className="gap-recommendation">

                  <div className="recommendation-title">
                    ✨ AI Recommended Action
                  </div>

                  <p>
                    {gap.recommendedAction}
                  </p>

                </div>


                {/* Action */}

                <button
                  className="gap-action-button"
                  onClick={() =>
                    navigate("/employee/learning-path")
                  }
                >
                  View Recommended Learning →
                </button>

              </article>
            );

          })}

        </div>

      </section>


      {/* ================= BOTTOM CTA ================= */}

      <section className="skill-gap-cta">

        <div>

          <h2>
            Ready to close your skill gaps?
          </h2>

          <p>
            Explore your personalized learning path based on
            these competency gaps.
          </p>

        </div>

        <button
          onClick={() =>
            navigate("/employee/learning-path")
          }
        >
          Explore Learning Path →
        </button>

      </section>

    </div>
  );
}

export default SkillGaps;