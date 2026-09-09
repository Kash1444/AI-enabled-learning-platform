import "./AdminPages.css";

function TrainingAnalytics() {
  return (
    <div className="admin-page">
      <div className="admin-header">
        <div>
          <span>TRAINING ANALYTICS</span>
          <h1>Training Performance</h1>
          <p>Monitor learning participation and outcomes.</p>
        </div>
      </div>

      <div className="admin-kpis">
        <div><span>Courses Completed</span><strong>4,862</strong></div>
        <div><span>Learning Hours</span><strong>18,420</strong></div>
        <div><span>Avg Completion</span><strong>76%</strong></div>
        <div><span>Assessment Score</span><strong>79%</strong></div>
      </div>

      <section className="admin-card admin-section">
        <h2>Training Providers</h2>

        {[
          ["iGOT Karmayogi", "2,486 completions"],
          ["NSSTA TPAC", "1,328 completions"],
          ["Internal Training", "742 completions"],
          ["External Programmes", "306 completions"],
        ].map((item) => (
          <div className="admin-list-row" key={item[0]}>
            <span>{item[0]}</span>
            <strong>{item[1]}</strong>
          </div>
        ))}
      </section>
    </div>
  );
}

export default TrainingAnalytics;