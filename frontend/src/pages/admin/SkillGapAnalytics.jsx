import "./AdminPages.css";

function CompetencyAnalytics() {
  const competencies = [
    ["Statistical", "78%", "Strong"],
    ["Technical", "64%", "Moderate"],
    ["Digital Governance", "69%", "Moderate"],
    ["Behavioral / Managerial", "81%", "Strong"],
  ];

  return (
    <div className="admin-page">
      <div className="admin-header">
        <div>
          <span>COMPETENCY INTELLIGENCE</span>
          <h1>Organization Competency</h1>
          <p>Monitor competency levels across the workforce.</p>
        </div>
      </div>

      <div className="admin-grid">
        {competencies.map((item) => (
          <section className="admin-card" key={item[0]}>
            <h2>{item[0]}</h2>
            <strong style={{ fontSize: "32px" }}>{item[1]}</strong>
            <p>{item[2]} competency level</p>

            <div className="mini-progress">
              <div style={{ width: item[1] }}></div>
            </div>
          </section>
        ))}
      </div>

      <div className="admin-highlight admin-section">
        <h3>AI Insight</h3>
        <p>
          Technical competency represents the largest organization-wide
          development opportunity. Targeted learning programmes could
          significantly improve workforce readiness.
        </p>
      </div>
    </div>
  );
}

export default CompetencyAnalytics;