import "./AdminPages.css";

function AdminDashboard() {
  return (
    <div className="admin-page">
      <div className="admin-header">
        <div>
          <span>ADMINISTRATION</span>
          <h1>Workforce Intelligence Dashboard</h1>
          <p>Organization-wide competency and learning overview.</p>
        </div>
      </div>

      <div className="admin-kpis">
        <div><span>Total Employees</span><strong>1,248</strong></div>
        <div><span>Avg Competency</span><strong>71%</strong></div>
        <div><span>Active Learners</span><strong>864</strong></div>
        <div><span>Skill Gaps</span><strong>326</strong></div>
      </div>

      <div className="admin-grid">
        <section className="admin-card">
          <h2>Competency Distribution</h2>
          <div className="admin-chart">
            <div className="chart-bar" style={{ height: "55%" }}></div>
            <div className="chart-bar" style={{ height: "72%" }}></div>
            <div className="chart-bar" style={{ height: "63%" }}></div>
            <div className="chart-bar" style={{ height: "84%" }}></div>
            <div className="chart-bar" style={{ height: "70%" }}></div>
          </div>
        </section>

        <section className="admin-card">
          <h2>Priority Areas</h2>

          <div className="admin-list-row">
            <span>Statistical Programming</span>
            <strong>128 gaps</strong>
          </div>

          <div className="admin-list-row">
            <span>Data Visualization</span>
            <strong>96 gaps</strong>
          </div>

          <div className="admin-list-row">
            <span>Digital Governance</span>
            <strong>74 gaps</strong>
          </div>

          <div className="admin-list-row">
            <span>Sampling Methodology</span>
            <strong>58 gaps</strong>
          </div>
        </section>
      </div>
    </div>
  );
}

export default AdminDashboard;