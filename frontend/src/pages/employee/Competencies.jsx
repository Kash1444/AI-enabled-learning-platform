import { competencyOverview } from "../../data/employeeData";
import "./Competencies.css";

function Competencies() {
  const competencyItems = competencyOverview;

    const totalCurrent = competencyItems.reduce(
    (sum, item) => sum + item.current,
    0
    );

    const totalRequired = competencyItems.reduce(
    (sum, item) => sum + item.required,
    0
    );

  const overallPercentage = Math.round(
    (totalCurrent / totalRequired) * 100
  );

  return (
    <div className="competencies-page">

      {/* Header */}

      <div className="competencies-header">

        <div>
          <div className="competencies-breadcrumb">
            Employee Portal / Competencies
          </div>

          <h1>My Competencies</h1>

          <p>
            View your current competency levels against the requirements
            of your role.
          </p>
        </div>

        <button className="assessment-button">
          ✨ Start AI Assessment
        </button>

      </div>


      {/* Overall Competency */}

      <section className="overall-competency-card">

        <div className="overall-score">

          <div className="score-circle">
            <span>{overallPercentage}%</span>
          </div>

          <div>
            <h2>Overall Competency</h2>

            <p>
              Your current competency level across all competency
              domains.
            </p>

            <span className="score-status">
              ● Good Progress
            </span>
          </div>

        </div>


        <div className="overall-stats">

          <div>
            <strong>{totalCurrent.toFixed(1)}</strong>
            <span>Current Score</span>
          </div>

          <div>
            <strong>{totalRequired.toFixed(1)}</strong>
            <span>Required Score</span>
          </div>

          <div>
            <strong>
              {(totalRequired - totalCurrent).toFixed(1)}
            </strong>
            <span>Total Gap</span>
          </div>

        </div>

      </section>


      {/* Competency Domains */}

      <div className="competency-section-title">

        <div>
          <h2>Competency Domains</h2>

          <p>
            Current competency compared with the level required
            for your role.
          </p>
        </div>

        <div className="competency-legend">
          <span>
            <i className="legend-current"></i>
            Current
          </span>

          <span>
            <i className="legend-required"></i>
            Required
          </span>
        </div>

      </div>


      <div className="competency-grid">

        {competencyItems.map((data) => {

          const gap = data.required - data.current;

          const currentPercentage =
            (data.current / 5) * 100;

          const requiredPercentage =
            (data.required / 5) * 100;

          return (
            <section
              className="competency-card"
              key={name}
            >

                <div className="competency-card-header">

                    <div>
                        <h3>{data.domain}</h3>

                        <p>
                        Competency domain
                        </p>
                    </div>

                    <div className="competency-score">
                        {data.current}
                        <span>/ 5</span>
                </div>

                </div>


              {/* Current */}

              <div className="competency-level">

                <div className="level-label">
                  <span>Current Level</span>

                  <strong>
                    {data.current}
                  </strong>
                </div>

                <div className="level-track">

                  <div
                    className="level-current"
                    style={{
                      width: `${currentPercentage}%`,
                    }}
                  ></div>

                </div>

              </div>


              {/* Required */}

              <div className="competency-level">

                <div className="level-label">
                  <span>Required Level</span>

                  <strong>
                    {data.required}
                  </strong>
                </div>

                <div className="level-track required-track">

                  <div
                    className="level-required"
                    style={{
                      width: `${requiredPercentage}%`,
                    }}
                  ></div>

                </div>

              </div>


              <div className="competency-gap">

                <span>Competency Gap</span>

                <strong>
                  {gap.toFixed(1)}
                </strong>

              </div>

            </section>
          );
        })}

      </div>


      {/* AI Assessment */}

      <section className="ai-assessment-card">

        <div className="ai-assessment-icon">
          ✨
        </div>

        <div className="ai-assessment-content">

          <h2>AI Competency Assessment</h2>

          <p>
            Take an AI-powered assessment to validate your current
            competency levels. The assessment can identify strengths,
            detect knowledge gaps and help improve your personalized
            learning recommendations.
          </p>

          <div className="assessment-features">

            <span>✓ Adaptive Questions</span>

            <span>✓ Instant Evaluation</span>

            <span>✓ AI Feedback</span>

            <span>✓ Competency Update</span>

          </div>

        </div>

        <button className="assessment-start-button">
          Start Assessment →
        </button>

      </section>

    </div>
  );
}

export default Competencies;