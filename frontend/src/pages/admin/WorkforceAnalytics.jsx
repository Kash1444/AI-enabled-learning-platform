import "./AdminPages.css";

function WorkforceAnalytics() {
  return (
    <div className="admin-page">
      <div className="admin-header">
        <div>
          <span>WORKFORCE ANALYTICS</span>
          <h1>Workforce Analytics</h1>
          <p>Understand workforce composition and capability.</p>
        </div>
      </div>

      <div className="admin-kpis">
        <div><span>Statistical Officers</span><strong>412</strong></div>
        <div><span>Technical Staff</span><strong>286</strong></div>
        <div><span>Managers</span><strong>164</strong></div>
        <div><span>Other Roles</span><strong>386</strong></div>
      </div>

      <section className="admin-card admin-section">
        <h2>Department Workforce</h2>

        {[
          ["National Statistical Office", "428"],
          ["Economic Statistics Division", "296"],
          ["Social Statistics Division", "247"],
          ["Data & Technology Division", "182"],
          ["Administration", "95"],
        ].map((item) => (
          <div className="admin-list-row" key={item[0]}>
            <span>{item[0]}</span>
            <strong>{item[1]} employees</strong>
          </div>
        ))}
      </section>
    </div>
  );
}

export default WorkforceAnalytics;