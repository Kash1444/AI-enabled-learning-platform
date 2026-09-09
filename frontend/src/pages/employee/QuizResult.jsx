import { useNavigate } from "react-router-dom";
import "./QuizResult.css";

function QuizResult() {
  const navigate = useNavigate();

  return (
    <div className="result-page">
      <div className="result-hero">
        <div className="result-check">✓</div>

        <span>ASSESSMENT COMPLETED</span>

        <h1>Sampling Methodology</h1>

        <p>Your assessment has been evaluated successfully.</p>

        <div className="result-score">84%</div>

        <div className="result-label">Excellent Performance</div>
      </div>

      <div className="result-stats">
        <div>
          <span>Correct Answers</span>
          <strong>8 / 10</strong>
        </div>

        <div>
          <span>Time Taken</span>
          <strong>07:42</strong>
        </div>

        <div>
          <span>Previous Score</span>
          <strong>72%</strong>
        </div>

        <div>
          <span>Improvement</span>
          <strong className="positive">+12%</strong>
        </div>
      </div>

      <div className="result-content">
        <section className="result-card">
          <h2>AI Feedback</h2>

          <div className="feedback-highlight">
            <strong>Great progress!</strong>
            <p>
              Your understanding of sampling concepts has improved
              significantly. You performed particularly well on probability
              sampling and sample design questions.
            </p>
          </div>

          <h3>Areas to strengthen</h3>

          <div className="result-area">
            <span>Non-response bias</span>
            <strong>Needs Practice</strong>
          </div>

          <div className="result-area">
            <span>Sample size determination</span>
            <strong>Needs Practice</strong>
          </div>
        </section>

        <section className="result-card">
          <h2>Competency Update</h2>

          <div className="competency-result">
            <div>
              <span>Sampling Methodology</span>
              <strong>3.5 → 3.9</strong>
            </div>

            <div className="mini-progress">
              <div></div>
            </div>

            <p>
              Your competency profile has been updated based on this
              assessment.
            </p>
          </div>

          <button
            className="result-button"
            onClick={() => navigate("/employee/skill-gaps")}
          >
            View Updated Skill Gaps
          </button>
        </section>
      </div>

      <div className="result-actions">
        <button onClick={() => navigate("/employee/quizzes")}>
          Back to Quizzes
        </button>

        <button onClick={() => navigate("/employee/learning-path")}>
          Continue Learning →
        </button>
      </div>
    </div>
  );
}

export default QuizResult;