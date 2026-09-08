import {
  employeeProfile,
  dashboardSummary,
  competencyOverview,
  skillGaps,
  aiRecommendations,
  learningProgress,
  recentActivity,
} from "../../data/employeeData";

import "./EmployeeDashboard.css";

function EmployeeDashboard() {
  return (

    
    <div className="employee-dashboard">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="dashboard-header">

        <div>
          <div className="dashboard-breadcrumb">
            Employee Portal / Dashboard
          </div>

          <h1 className="dashboard-heading">
            Good morning, {employeeProfile.name.split(" ")[0]} 👋
          </h1>

          <p className="dashboard-subheading">
            Here's your competency and learning overview.
          </p>
        </div>

        <div className="dashboard-header-right">

          <button className="notification-button">
            🔔
            <span className="notification-dot"></span>
          </button>

          <div className="profile-mini">

            <div className="avatar">
              {getInitials(employeeProfile.name)}
            </div>

            <div>
              <div className="profile-name">
                {employeeProfile.name}
              </div>

              <div className="profile-role">
                {employeeProfile.designation}
              </div>
            </div>

          </div>

        </div>

      </header>


      {/* =====================================================
          EMPLOYEE PROFILE BANNER
      ===================================================== */}

      <section className="profile-banner">

        <div className="profile-banner-left">

          <div className="large-avatar">
            {getInitials(employeeProfile.name)}
          </div>

          <div>

            <h2 className="profile-banner-name">
              {employeeProfile.name}
            </h2>

            <p className="profile-banner-role">
              {employeeProfile.designation} •{" "}
              {employeeProfile.department}
            </p>

            <p className="profile-banner-org">
              {employeeProfile.organization}
            </p>

          </div>

        </div>


        <div className="profile-stats">

          <div className="profile-stats-item">
            <strong>
              {employeeProfile.experience}
            </strong>

            <span>
              Years Experience
            </span>
          </div>


          <div className="profile-stats-item">
            <strong>
              {employeeProfile.education}
            </strong>

            <span>
              Education
            </span>
          </div>


          <div className="profile-stats-item">
            <strong>
              {employeeProfile.location}
            </strong>

            <span>
              Location
            </span>
          </div>

        </div>

      </section>


      {/* =====================================================
          KPI CARDS
      ===================================================== */}

      <section className="kpi-grid">

        {/* Overall Competency */}

        <div className="kpi-card">

          <div className="kpi-top">

            <div className="kpi-icon">
              🎯
            </div>

            <span className="kpi-change">
              ↑ {dashboardSummary.competencyChange}%
            </span>

          </div>

          <div className="kpi-value">
            {dashboardSummary.overallCompetency}%
          </div>

          <div className="kpi-title">
            Overall Competency
          </div>

          <div className="kpi-subtitle">
            Across all competency domains
          </div>

        </div>


        {/* Skill Gaps */}

        <div className="kpi-card">

          <div className="kpi-top">

            <div className="kpi-icon">
              ⚠️
            </div>

            <span className="kpi-warning">
              {dashboardSummary.highPriorityGaps} High
            </span>

          </div>

          <div className="kpi-value">
            {dashboardSummary.totalSkillGaps}
          </div>

          <div className="kpi-title">
            Skill Gaps
          </div>

          <div className="kpi-subtitle">
            {dashboardSummary.mediumPriorityGaps} medium priority
          </div>

        </div>


        {/* Learning Progress */}

        <div className="kpi-card">

          <div className="kpi-top">

            <div className="kpi-icon">
              📚
            </div>

            <span className="kpi-change">
              ↑ {dashboardSummary.learningProgressChange}%
            </span>

          </div>

          <div className="kpi-value">
            {dashboardSummary.learningProgress}%
          </div>

          <div className="kpi-title">
            Learning Progress
          </div>

          <div className="kpi-subtitle">
            Overall learning journey
          </div>

        </div>


        {/* Courses Completed */}

        <div className="kpi-card">

          <div className="kpi-top">

            <div className="kpi-icon">
              ✓
            </div>

            <span className="kpi-change">
              ↑ {dashboardSummary.coursesCompletedChange}%
            </span>

          </div>

          <div className="kpi-value">
            {dashboardSummary.coursesCompleted}
          </div>

          <div className="kpi-title">
            Courses Completed
          </div>

          <div className="kpi-subtitle">
            Successfully completed
          </div>

        </div>

      </section>


      {/* =====================================================
          COMPETENCY + SKILL GAP
      ===================================================== */}

      <section className="dashboard-main-grid">


        {/* ================= COMPETENCY ================= */}

        <div className="dashboard-card">

          <div className="dashboard-card-header">

            <div>
              <h2 className="dashboard-card-title">
                Competency Overview
              </h2>

              <p className="dashboard-card-subtitle">
                Current competency compared with role requirements
              </p>
            </div>

            <button className="text-button">
              View Details →
            </button>

          </div>


          <div className="competency-container">

            {competencyOverview.map((item) => {

              const currentPercentage =
                (item.current / 5) * 100;

              const requiredPercentage =
                (item.required / 5) * 100;

              return (

                <div
                  className="competency-row"
                  key={item.domain}
                >

                  <div className="competency-header">

                    <span className="competency-name">
                      {item.domain}
                    </span>

                    <span className="competency-score">
                      {item.current} / {item.required}
                    </span>

                  </div>


                  <div className="competency-track">

                    <div
                      className="current-competency"
                      style={{
                        width: `${currentPercentage}%`,
                      }}
                    />

                    <div
                      className="required-marker"
                      style={{
                        left: `${requiredPercentage}%`,
                      }}
                    />

                  </div>


                  <div className="competency-legend">

                    <span>
                      Current: {item.current}
                    </span>

                    <span>
                      Required: {item.required}
                    </span>

                  </div>

                </div>

              );

            })}

          </div>


          <div className="competency-key">

            <span>
              <i className="legend-current"></i>
              Current Level
            </span>

            <span>
              <i className="legend-required"></i>
              Required Level
            </span>

          </div>

        </div>


        {/* ================= SKILL GAPS ================= */}

        <div className="dashboard-card">

          <div className="dashboard-card-header">

            <div>
              <h2 className="dashboard-card-title">
                AI Skill Gap Analysis
              </h2>

              <p className="dashboard-card-subtitle">
                Prioritized areas for development
              </p>
            </div>

            <span className="ai-badge">
              ✨ AI Powered
            </span>

          </div>


          <div className="skill-gap-summary">

            <div className="gap-circle">

              <strong>
                {dashboardSummary.totalSkillGaps}
              </strong>

              <span>
                Gaps
              </span>

            </div>


            <div>

              <div className="high-gap">
                ● {dashboardSummary.highPriorityGaps} High Priority
              </div>

              <div className="medium-gap">
                ● {dashboardSummary.mediumPriorityGaps} Medium Priority
              </div>

            </div>

          </div>


          <div className="skill-gap-preview">

            {skillGaps.slice(0, 2).map((gap) => (

              <div
                className="skill-gap-preview-item"
                key={gap.id}
              >

                <div className="skill-gap-preview-top">

                  <strong>
                    {gap.skill}
                  </strong>

                  <span
                    className={`priority-badge ${
                      gap.priority === "High"
                        ? "high-priority"
                        : "medium-priority"
                    }`}
                  >
                    {gap.priority}
                  </span>

                </div>

                <p>
                  {gap.description}
                </p>

              </div>

            ))}

          </div>


          <button className="outline-button">
            View All Skill Gaps →
          </button>

        </div>

      </section>


      {/* =====================================================
          AI RECOMMENDED LEARNING
      ===================================================== */}

      <section>

        <div className="dashboard-section-heading">

          <div>

            <h2 className="dashboard-section-title">
              AI Recommended Learning
            </h2>

            <p className="dashboard-section-subtitle">
              Personalized recommendations based on your skill gaps
            </p>

          </div>

          <button className="text-button">
            View Learning Path →
          </button>

        </div>


        <div className="course-grid">

          {aiRecommendations.map((course) => (

            <div
              className="course-card"
              key={course.id}
            >

              <div className="course-top">

                <div className="course-icon">
                  📘
                </div>

                <span className="provider-badge">
                  {course.provider}
                </span>

              </div>


              <h3 className="course-title">
                {course.title}
              </h3>


              <p className="course-reason">
                {course.reason}
              </p>


              <div className="course-meta">

                <span>
                  ⏱ {course.duration}
                </span>

                <span>
                  • {course.level}
                </span>

              </div>


              {course.progress !== undefined && (

                <div className="course-progress">

                  <div className="course-progress-header">

                    <span>
                      Progress
                    </span>

                    <strong>
                      {course.progress}%
                    </strong>

                  </div>

                  <div className="progress-track">

                    <div
                      className="progress-fill"
                      style={{
                        width: `${course.progress}%`,
                      }}
                    />

                  </div>

                </div>

              )}


              <button className="primary-button">
                {course.progress
                  ? "Continue Learning"
                  : "Start Learning"}
              </button>

            </div>

          ))}

        </div>

      </section>


      {/* =====================================================
          LEARNING PROGRESS + RECENT ACTIVITY
      ===================================================== */}

      <section className="bottom-grid">


        {/* Learning Progress */}

        <div className="dashboard-card">

          <div className="dashboard-card-header">

            <div>

              <h2 className="dashboard-card-title">
                Current Learning Progress
              </h2>

              <p className="dashboard-card-subtitle">
                Your active and completed learning
              </p>

            </div>

            <button className="text-button">
              View All
            </button>

          </div>


          <div>

            {learningProgress.map((item) => (

              <div
                className="learning-item"
                key={item.id}
              >

                <div className="learning-top">

                  <div>

                    <div className="learning-title">
                      {item.title}
                    </div>

                    <div className="learning-provider">
                      {item.provider}
                    </div>

                  </div>

                  <strong>
                    {item.progress}%
                  </strong>

                </div>


                <div className="progress-track">

                  <div
                    className="progress-fill"
                    style={{
                      width: `${item.progress}%`,
                    }}
                  />

                </div>

              </div>

            ))}

          </div>

        </div>


        {/* Recent Activity */}

        <div className="dashboard-card">

          <div className="dashboard-card-header">

            <div>

              <h2 className="dashboard-card-title">
                Recent Activity
              </h2>

              <p className="dashboard-card-subtitle">
                Your latest learning activities
              </p>

            </div>

          </div>


          <div>

            {recentActivity.map((activity) => (

              <div
                className="activity-item"
                key={activity.id}
              >

                <div className="activity-icon">
                  {activity.icon || "✓"}
                </div>

                <div className="activity-content">

                  <div className="activity-title">
                    {activity.title}
                  </div>

                  <div className="activity-time">
                    {activity.time}
                  </div>

                </div>

                <span className="activity-status">
                  {activity.status || "Done"}
                </span>

              </div>

            ))}

          </div>

        </div>

      </section>


      {/* =====================================================
          AI ASSISTANT BANNER
      ===================================================== */}

      <section className="ai-banner">

        <div className="ai-banner-icon">
          ✨
        </div>

        <div className="ai-banner-content">

          <h3 className="ai-banner-title">
            Need help with your learning?
          </h3>

          <p className="ai-banner-text">
            Ask the AI Learning Assistant about your skill gaps,
            recommended courses, competencies, or assessments.
          </p>

        </div>

        <button className="ai-button">
          Ask AI Assistant →
        </button>

      </section>

    </div>
  );
}


/* ============================================================
   HELPER
   ============================================================ */

function getInitials(name) {
  if (!name) return "";

  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}


export default EmployeeDashboard;