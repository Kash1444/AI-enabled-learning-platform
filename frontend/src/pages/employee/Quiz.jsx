import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Quiz.css";

function Quiz() {
  const navigate = useNavigate();

  const quizzes = [
    {
      id: 1,
      title: "Sampling Methodology",
      description:
        "Test your understanding of sampling techniques used in official statistics.",
      questions: 10,
      duration: "10 min",
      difficulty: "Intermediate",
      score: null,
      status: "Recommended",
    },
    {
      id: 2,
      title: "Statistical Programming with R",
      description:
        "Assess your knowledge of R programming and statistical data analysis.",
      questions: 15,
      duration: "15 min",
      difficulty: "Intermediate",
      score: 80,
      status: "Completed",
    },
    {
      id: 3,
      title: "Data Visualization",
      description:
        "Evaluate your ability to select and interpret statistical visualizations.",
      questions: 10,
      duration: "10 min",
      difficulty: "Beginner",
      score: null,
      status: "Available",
    },
  ];

  const [selectedQuiz, setSelectedQuiz] = useState(null);

  const startQuiz = (quiz) => {
    setSelectedQuiz(quiz);
  };

  const confirmStart = () => {
    navigate("/employee/quiz/1");
  };

  return (
    <div className="quiz-page">
      <div className="page-header">
        <div>
          <span className="page-eyebrow">ASSESSMENT CENTER</span>
          <h1>Quizzes</h1>
          <p>
            Strengthen your competencies through AI-powered assessments.
          </p>
        </div>

        <div className="quiz-header-stat">
          <strong>2</strong>
          <span>Assessments Available</span>
        </div>
      </div>

      <div className="ai-quiz-banner">
        <div className="ai-banner-icon">✨</div>
        <div>
          <h3>AI-Powered Assessment</h3>
          <p>
            Questions are generated from your learning materials and aligned
            with your competency gaps.
          </p>
        </div>
      </div>

      <div className="quiz-summary">
        <div>
          <span>Total Attempts</span>
          <strong>6</strong>
        </div>

        <div>
          <span>Average Score</span>
          <strong>78%</strong>
        </div>

        <div>
          <span>Highest Score</span>
          <strong>92%</strong>
        </div>

        <div>
          <span>Competency Growth</span>
          <strong>+8%</strong>
        </div>
      </div>

      <section className="quiz-section">
        <div className="section-heading">
          <div>
            <h2>Available Assessments</h2>
            <p>Assessments recommended based on your skill gaps.</p>
          </div>
        </div>

        <div className="quiz-grid">
          {quizzes.map((quiz) => (
            <div className="quiz-card" key={quiz.id}>
              <div className="quiz-card-top">
                <span
                  className={`quiz-status ${
                    quiz.status === "Completed"
                      ? "completed"
                      : quiz.status === "Recommended"
                      ? "recommended"
                      : ""
                  }`}
                >
                  {quiz.status}
                </span>

                <span className="difficulty">
                  {quiz.difficulty}
                </span>
              </div>

              <h3>{quiz.title}</h3>

              <p>{quiz.description}</p>

              <div className="quiz-meta">
                <span>📝 {quiz.questions} Questions</span>
                <span>⏱ {quiz.duration}</span>
              </div>

              {quiz.score !== null && (
                <div className="previous-score">
                  Previous Score
                  <strong>{quiz.score}%</strong>
                </div>
              )}

              <button
                className="quiz-action"
                onClick={() => startQuiz(quiz)}
              >
                {quiz.score !== null ? "Retake Assessment" : "Start Assessment"}
              </button>
            </div>
          ))}
        </div>
      </section>

      {selectedQuiz && (
        <div className="quiz-modal-overlay">
          <div className="quiz-modal">
            <button
              className="modal-close"
              onClick={() => setSelectedQuiz(null)}
            >
              ×
            </button>

            <div className="modal-icon">📝</div>

            <h2>{selectedQuiz.title}</h2>

            <p>
              You are about to start a {selectedQuiz.questions}-question
              assessment.
            </p>

            <div className="modal-info">
              <div>
                <span>Questions</span>
                <strong>{selectedQuiz.questions}</strong>
              </div>

              <div>
                <span>Duration</span>
                <strong>{selectedQuiz.duration}</strong>
              </div>
            </div>

            <div className="modal-warning">
              Once started, the assessment timer will begin.
            </div>

            <button className="modal-start" onClick={confirmStart}>
              Start Quiz
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Quiz;