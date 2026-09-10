import { useState } from "react";
import "./GenerateAssessment.css";
import { generateAssessment } from "../../services/assessmentService";

function GenerateAssessment() {
  const [generated, setGenerated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [questions, setQuestions] = useState([]);

  const handleGenerate = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await generateAssessment({
        materialId: "demo-material",
        competency: "Sampling Methodology",
        domain: "Statistical",
        numQuestions: 10,
        difficulty: "Intermediate",
        employeeId: "EMP001",
      });

      const generatedQuestions =
        response?.questions ||
        response?.assessment?.questions ||
        [];

      setQuestions(generatedQuestions);
      setGenerated(true);
    } catch (err) {
      console.error("Assessment generation error:", err);
      setError(
        "Unable to generate the assessment. Please make sure the AI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generator-page">
      <div className="page-header">
        <span>AI ASSESSMENT GENERATOR</span>
        <h1>Generate Assessment</h1>
        <p>Create competency-aligned MCQs from learning materials.</p>
      </div>

      <div className="generator-layout">
        <section className="generator-card">
          <h2>Assessment Configuration</h2>

          <label>Learning Material</label>
          <select>
            <option>Sampling_Methodology.pdf</option>
            <option>R_Programming.pptx</option>
            <option>Data_Visualization.docx</option>
          </select>

          <label>Competency</label>
          <select>
            <option>Sampling Methodology</option>
            <option>Statistical Programming</option>
            <option>Data Visualization</option>
          </select>

          <label>Number of Questions</label>
          <select>
            <option>10</option>
            <option>15</option>
            <option>20</option>
          </select>

          <label>Difficulty</label>

          <div className="difficulty-options">
            <button>Easy</button>
            <button className="selected">Intermediate</button>
            <button>Advanced</button>
          </div>

          <button
            className="generate-button"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? "Generating..." : "✨ Generate with AI"}
          </button>

          {error && (
            <p style={{ marginTop: "15px" }}>
              {error}
            </p>
          )}
        </section>

        <section className="generator-preview">
          {!generated ? (
            <div className="empty-generator">
              <div>✨</div>
              <h2>AI Assessment Preview</h2>
              <p>
                Configure the assessment and click generate to create
                questions.
              </p>
            </div>
          ) : (
            <div>
              <div className="generated-header">
                <div>
                  <span>GENERATED</span>
                  <h2>Sampling Methodology Assessment</h2>
                </div>

                <strong>
                  {questions.length || 10} Questions
                </strong>
              </div>

              {questions.length > 0 ? (
                questions.map((question, index) => (
                  <div
                    className="generated-question"
                    key={question.id || index}
                  >
                    <span>Question {index + 1}</span>

                    <h3>
                      {question.question ||
                        question.text ||
                        "Generated question"}
                    </h3>

                    {question.options?.map((option, optionIndex) => (
                      <p key={optionIndex}>
                        {String.fromCharCode(65 + optionIndex)}.{" "}
                        {typeof option === "string"
                          ? option
                          : option.text || option.label}
                      </p>
                    ))}
                  </div>
                ))
              ) : (
                <div className="generated-question">
                  <span>AI RESPONSE</span>
                  <h3>
                    The backend generated an assessment, but its
                    question format needs to be mapped to the UI.
                  </h3>
                </div>
              )}

              <button className="publish-button">
                Publish Assessment
              </button>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default GenerateAssessment;