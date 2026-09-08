import { useState } from "react";
import "./UploadMaterials.css";

function UploadMaterials() {
  const [file, setFile] = useState(null);

  return (
    <div className="trainer-page">
      <div className="page-header">
        <span>TRAINER TOOLS</span>
        <h1>Upload Learning Materials</h1>
        <p>Upload content that can be used to generate AI assessments.</p>
      </div>

      <div className="upload-layout">
        <section className="upload-box">
          <div className="upload-icon">📤</div>
          <h2>Upload Learning Material</h2>
          <p>
            PDF, PPT, PPTX, DOC, DOCX and supported learning files
          </p>

          <label className="upload-button">
            Choose File
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
            />
          </label>

          {file && (
            <div className="selected-file">
              <strong>{file.name}</strong>
              <span>{(file.size / 1024 / 1024).toFixed(2)} MB</span>
            </div>
          )}

          <button className="process-button">
            Process Material with AI
          </button>
        </section>

        <section className="trainer-card">
          <h2>Recent Materials</h2>

          <div className="material-row">
            <span>📄 Sampling_Methodology.pdf</span>
            <strong>Processed</strong>
          </div>

          <div className="material-row">
            <span>📊 R_Programming.pptx</span>
            <strong>Processed</strong>
          </div>

          <div className="material-row">
            <span>📄 Data_Visualization.docx</span>
            <strong>Processing</strong>
          </div>
        </section>
      </div>
    </div>
  );
}

export default UploadMaterials;