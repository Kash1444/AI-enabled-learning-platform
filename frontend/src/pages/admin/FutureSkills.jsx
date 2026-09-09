import "./AdminPages.css";

function FutureSkills() {
  const skills = [
    ["AI & Machine Learning", "High", "78% projected demand"],
    ["Advanced Statistical Computing", "High", "72% projected demand"],
    ["Data Engineering", "High", "68% projected demand"],
    ["Data Visualization", "Medium", "61% projected demand"],
    ["Digital Governance", "Medium", "57% projected demand"],
  ];

  return (
    <div className="admin-page">
      <div className="admin-header">
        <div>
          <span>FUTURE SKILLS INTELLIGENCE</span>
          <h1>Emerging Workforce Skills</h1>
          <p>AI-powered view of future capability requirements.</p>
        </div>
      </div>

      <div className="admin-highlight">
        <h3>✨ AI Workforce Prediction</h3>
        <p>
          The organization is expected to see increasing demand for AI,
          advanced analytics, statistical computing and data engineering
          capabilities over the coming years.
        </p>
      </div>

      <section className="admin-card admin-section">
        <h2>Priority Future Skills</h2>

        {skills.map((skill) => (
          <div className="admin-list-row" key={skill[0]}>
            <span>{skill[0]}</span>
            <strong>{skill[1]} · {skill[2]}</strong>
          </div>
        ))}
      </section>
    </div>
  );
}

export default FutureSkills;