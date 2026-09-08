import "./TrainerDashboard.css";

function TrainerDashboard() {
  return (
    <div className="trainer-page">
      <div className="trainer-header">
        <div>
          <span>TRAINER PORTAL</span>
          <h1>Good morning, Priya 👋</h1>
          <p>Manage learning content and assessments.</p>
        </div>

        <button className="trainer-primary">
          + Upload Material
        </button>
      </div>

      <div className="trainer-kpis">
        <div>
          <span>Learning Materials</span>
          <strong>24</strong>
          <small>+4 this month</small>
        </div>

        <div>
          <span>AI Assessments</span>
          <strong>18</strong>
          <small>+6 this month</small>
        </div>

        <div>
          <span>Learners</span>
          <strong>186</strong>
          <small>12 active today</small>
        </div>

        <div>
          <span>Avg. Assessment Score</span>
          <strong>78%</strong>
          <small>+5% improvement</small>
        </div>
      </div>

      <div className="trainer-grid">
        <section className="trainer-card">
          <h2>Quick Actions</h2>

          <div className="trainer-actions">
            <div>📤 <strong>Upload Material</strong><span>Add PDF, PPT or DOCX</span></div>
            <div>✨ <strong>Generate Assessment</strong><span>Create AI MCQs</span></div>
            <div>📊 <strong>View Learner Results</strong><span>Track performance</span></div>
          </div>
        </section>

        <section className="trainer-card">
          <h2>Recent Activity</h2>

          <div className="trainer-activity">
            <p><strong>Sampling Methodology</strong> assessment generated</p>
            <p><strong>R Programming Basics</strong> material uploaded</p>
            <p><strong>12 learners</strong> completed an assessment</p>
            <p><strong>Data Visualization</strong> assessment published</p>
          </div>
        </section>
      </div>
    </div>
  );
}

export default TrainerDashboard;