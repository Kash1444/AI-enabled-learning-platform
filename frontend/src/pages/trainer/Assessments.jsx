import "./Assessments.css";

function Assessments() {
  const assessments = [
    ["Sampling Methodology", "10", "Published", "84%"],
    ["Statistical Programming with R", "15", "Published", "78%"],
    ["Data Visualization", "10", "Draft", "-"],
    ["Official Statistics Fundamentals", "20", "Published", "91%"],
  ];

  return (
    <div className="trainer-page">
      <div className="page-header">
        <span>ASSESSMENT MANAGEMENT</span>
        <h1>Generated Assessments</h1>
        <p>Manage AI-generated assessments and learner attempts.</p>
      </div>

      <div className="assessment-table">
        <div className="assessment-head">
          <span>Assessment</span>
          <span>Questions</span>
          <span>Status</span>
          <span>Average</span>
          <span>Action</span>
        </div>

        {assessments.map((assessment) => (
          <div className="assessment-row" key={assessment[0]}>
            <strong>{assessment[0]}</strong>
            <span>{assessment[1]}</span>
            <span className={assessment[2] === "Published" ? "published" : "draft"}>
              {assessment[2]}
            </span>
            <span>{assessment[3]}</span>
            <button>View</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Assessments;