import { useState } from "react";
import "./GenerateAssessment.css";

function GenerateAssessment() {
  const [generated, setGenerated] = useState(false);

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
            onClick={() => setGenerated(true)}
          >
            ✨ Generate with AI
          </button>
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
                <strong>10 Questions</strong>
              </div>

              <div className="generated-question">
                <span>Question 1</span>
                <h3>
                  Which sampling method gives every population member an
                  equal probability of selection?
                </h3>

                <p>A. Convenience Sampling</p>
                <p>B. Simple Random Sampling ✓</p>
                <p>C. Purposive Sampling</p>
                <p>D. Snowball Sampling</p>
              </div>

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