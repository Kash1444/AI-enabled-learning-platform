import "./AdminPages.css";

function Reports() {
  const reports = [
    ["Workforce Competency Report", "Organization-wide competency summary"],
    ["Skill Gap Report", "Priority capability gaps"],
    ["Training Effectiveness Report", "Learning and assessment outcomes"],
    ["Future Skills Report", "Emerging skill requirements"],
  ];

  return (
    <div className="admin-page">
      <div className="admin-header">
        <div>
          <span>REPORTING CENTER</span>
          <h1>Reports</h1>
          <p>Generate management reports from workforce intelligence.</p>
        </div>
      </div>

      <div className="admin-grid">
        {reports.map((report) => (
          <section className="admin-card" key={report[0]}>
            <div style={{ fontSize: "30px" }}>📊</div>
            <h2>{report[0]}</h2>
            <p>{report[1]}</p>

            <button className="admin-primary">
              Generate Report
            </button>
          </section>
        ))}
      </div>
    </div>
  );
}

export default Reports;