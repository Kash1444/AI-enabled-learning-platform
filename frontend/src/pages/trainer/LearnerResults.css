import "./LearnerResults.css";

function LearnerResults() {
  const learners = [
    ["Arun Kumar", "Sampling Methodology", "84%", "Excellent"],
    ["Meena Sharma", "Sampling Methodology", "76%", "Good"],
    ["Rahul Singh", "R Programming", "68%", "Needs Practice"],
    ["Anita Verma", "Data Visualization", "91%", "Excellent"],
    ["Vikram Rao", "R Programming", "72%", "Good"],
  ];

  return (
    <div className="trainer-page">
      <div className="page-header">
        <span>LEARNER ANALYTICS</span>
        <h1>Learner Results</h1>
        <p>Track assessment performance and competency improvement.</p>
      </div>

      <div className="learner-result-stats">
        <div><span>Total Attempts</span><strong>186</strong></div>
        <div><span>Average Score</span><strong>78%</strong></div>
        <div><span>Pass Rate</span><strong>86%</strong></div>
        <div><span>Needs Support</span><strong>14%</strong></div>
      </div>

      <div className="learner-table">
        <div className="learner-head">
          <span>Learner</span>
          <span>Assessment</span>
          <span>Score</span>
          <span>Performance</span>
        </div>

        {learners.map((learner) => (
          <div className="learner-row" key={learner[0]}>
            <strong>{learner[0]}</strong>
            <span>{learner[1]}</span>
            <strong>{learner[2]}</strong>
            <span>{learner[3]}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default LearnerResults;