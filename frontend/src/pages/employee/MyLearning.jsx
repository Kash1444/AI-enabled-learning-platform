import { useState } from "react";
import "./MyLearning.css";

function MyLearning() {
  const [activeTab, setActiveTab] = useState("All");

  const learningItems = [
    {
      id: 1,
      title: "Statistical Programming with R",
      provider: "iGOT Karmayogi",
      type: "Course",
      category: "Technical",
      progress: 65,
      completedLessons: 13,
      totalLessons: 20,
      duration: "8 hours",
      lastActivity: "Today",
      status: "In Progress",
      skill: "Statistical Programming",
      icon: "💻",
    },
    {
      id: 2,
      title: "Data Visualization for Statistical Reporting",
      provider: "iGOT Karmayogi",
      type: "Course",
      category: "Technical",
      progress: 40,
      completedLessons: 4,
      totalLessons: 10,
      duration: "4 hours",
      lastActivity: "Yesterday",
      status: "In Progress",
      skill: "Data Visualization",
      icon: "📊",
    },
    {
      id: 3,
      title: "Sampling Techniques for Official Statistics",
      provider: "NSSTA TPAC",
      type: "Programme",
      category: "Statistical Methodology",
      progress: 0,
      completedLessons: 0,
      totalLessons: 6,
      duration: "6 hours",
      lastActivity: "Not started",
      status: "Not Started",
      skill: "Sampling Methodology",
      icon: "🏛",
    },
    {
      id: 4,
      title: "Fundamentals of Official Statistics",
      provider: "iGOT Karmayogi",
      type: "Course",
      category: "Statistical",
      progress: 100,
      completedLessons: 12,
      totalLessons: 12,
      duration: "5 hours",
      lastActivity: "Aug 28, 2026",
      status: "Completed",
      skill: "Official Statistics",
      icon: "📘",
    },
    {
      id: 5,
      title: "Digital Governance Fundamentals",
      provider: "iGOT Karmayogi",
      type: "Course",
      category: "Digital Governance",
      progress: 0,
      completedLessons: 0,
      totalLessons: 8,
      duration: "5 hours",
      lastActivity: "Not started",
      status: "Not Started",
      skill: "Digital Governance",
      icon: "🏛️",
    },
    {
      id: 6,
      title: "Data Management for Public Sector",
      provider: "iGOT Karmayogi",
      type: "Course",
      category: "Technical",
      progress: 100,
      completedLessons: 10,
      totalLessons: 10,
      duration: "6 hours",
      lastActivity: "Aug 20, 2026",
      status: "Completed",
      skill: "Data Management",
      icon: "🗄️",
    },
  ];

  const filteredItems = learningItems.filter((item) => {
    if (activeTab === "All") return true;

    if (activeTab === "In Progress") {
      return item.status === "In Progress";
    }

    if (activeTab === "Not Started") {
      return item.status === "Not Started";
    }

    if (activeTab === "Completed") {
      return item.status === "Completed";
    }

    return true;
  });

  const inProgress = learningItems.filter(
    (item) => item.status === "In Progress"
  );

  const completed = learningItems.filter(
    (item) => item.status === "Completed"
  );

  const notStarted = learningItems.filter(
    (item) => item.status === "Not Started"
  );

  return (
    <div className="my-learning-page">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="my-learning-header">

        <div>
          <div className="my-learning-breadcrumb">
            Employee Portal / My Learning
          </div>

          <h1>My Learning</h1>

          <p>
            Track your learning journey, continue active courses and
            review your completed training.
          </p>
        </div>

        <div className="learning-overall">

          <div className="overall-circle">
            <strong>68%</strong>
          </div>

          <div>
            <span>Overall Learning</span>
            <strong>Good Progress</strong>
            <small>
              +12% this month
            </small>
          </div>

        </div>

      </div>


      {/* =====================================================
          LEARNING SUMMARY
      ===================================================== */}

      <div className="learning-summary">

        <div className="learning-summary-card">

          <div className="summary-icon blue">
            ▶
          </div>

          <div>
            <strong>{inProgress.length}</strong>
            <span>In Progress</span>
          </div>

        </div>


        <div className="learning-summary-card">

          <div className="summary-icon orange">
            ◷
          </div>

          <div>
            <strong>{notStarted.length}</strong>
            <span>Not Started</span>
          </div>

        </div>


        <div className="learning-summary-card">

          <div className="summary-icon green">
            ✓
          </div>

          <div>
            <strong>{completed.length}</strong>
            <span>Completed</span>
          </div>

        </div>


        <div className="learning-summary-card">

          <div className="summary-icon purple">
            ⏱
          </div>

          <div>
            <strong>18.5h</strong>
            <span>Learning Time</span>
          </div>

        </div>

      </div>


      {/* =====================================================
          CONTINUE LEARNING
      ===================================================== */}

      {inProgress.length > 0 && (

        <section className="continue-section">

          <div className="section-title-row">

            <div>
              <span className="section-label">
                PICK UP WHERE YOU LEFT OFF
              </span>

              <h2>
                Continue Learning
              </h2>
            </div>

            <span className="active-count">
              {inProgress.length} active courses
            </span>

          </div>


          <div className="continue-grid">

            {inProgress.slice(0, 2).map((item) => (

              <div
                className="continue-card"
                key={item.id}
              >

                <div className="continue-top">

                  <div className="learning-course-icon">
                    {item.icon}
                  </div>

                  <span className="in-progress-badge">
                    In Progress
                  </span>

                </div>

                <div className="provider">
                  {item.provider}
                </div>

                <h3>
                  {item.title}
                </h3>

                <p>
                  Continue developing your{" "}
                  <strong>{item.skill}</strong> competency.
                </p>


                <div className="continue-progress-header">

                  <span>
                    Course Progress
                  </span>

                  <strong>
                    {item.progress}%
                  </strong>

                </div>

                <div className="continue-progress-track">

                  <div
                    className="continue-progress-fill"
                    style={{
                      width: `${item.progress}%`,
                    }}
                  ></div>

                </div>


                <div className="continue-meta">

                  <span>
                    ✓ {item.completedLessons}/{item.totalLessons} lessons
                  </span>

                  <span>
                    ◷ {item.duration}
                  </span>

                </div>


                <button className="continue-button">
                  Continue Learning
                  <span>→</span>
                </button>

              </div>

            ))}

          </div>

        </section>

      )}


      {/* =====================================================
          MY COURSES
      ===================================================== */}

      <section className="my-courses-section">

        <div className="courses-heading">

          <div>
            <span className="section-label">
              YOUR LEARNING LIBRARY
            </span>

            <h2>
              My Courses & Programs
            </h2>

            <p>
              All courses and programmes you have enrolled in.
            </p>
          </div>

        </div>


        {/* Tabs */}

        <div className="learning-tabs">

          {[
            "All",
            "In Progress",
            "Not Started",
            "Completed",
          ].map((tab) => (

            <button
              key={tab}
              className={
                activeTab === tab
                  ? "learning-tab active"
                  : "learning-tab"
              }
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>

          ))}

        </div>


        {/* Course List */}

        <div className="learning-list">

          {filteredItems.map((item) => (

            <div
              className="learning-list-item"
              key={item.id}
            >

              <div className="list-course-icon">
                {item.icon}
              </div>


              <div className="list-course-info">

                <div className="list-course-top">

                  <span className="list-provider">
                    {item.provider}
                  </span>

                  <span className="list-type">
                    {item.type}
                  </span>

                </div>

                <h3>
                  {item.title}
                </h3>

                <span className="list-skill">
                  Skill: {item.skill}
                </span>

              </div>


              <div className="list-progress">

                <div className="list-progress-header">

                  <span>
                    Progress
                  </span>

                  <strong>
                    {item.progress}%
                  </strong>

                </div>

                <div className="list-progress-track">

                  <div
                    className={
                      item.progress === 100
                        ? "list-progress-fill completed"
                        : "list-progress-fill"
                    }
                    style={{
                      width: `${item.progress}%`,
                    }}
                  ></div>

                </div>

                <small>
                  {item.completedLessons}/{item.totalLessons} lessons
                </small>

              </div>


              <div className="list-last-activity">

                <span>
                  Last Activity
                </span>

                <strong>
                  {item.lastActivity}
                </strong>

              </div>


              <div className="list-action">

                <button
                  className={
                    item.status === "Completed"
                      ? "review-button"
                      : "open-course-button"
                  }
                >
                  {item.status === "Completed"
                    ? "Review"
                    : item.status === "Not Started"
                    ? "Start"
                    : "Continue"}
                </button>

              </div>

            </div>

          ))}

        </div>


        {filteredItems.length === 0 && (

          <div className="learning-empty">

            <div>📚</div>

            <h3>
              Nothing here yet
            </h3>

            <p>
              Your learning activities will appear here.
            </p>

          </div>

        )}

      </section>


      {/* =====================================================
          AI LEARNING INSIGHT
      ===================================================== */}

      <section className="learning-ai-insight">

        <div className="ai-insight-icon">
          ✨
        </div>

        <div className="ai-insight-content">

          <span>
            AI LEARNING INSIGHT
          </span>

          <h3>
            You're making good progress on your technical skills.
          </h3>

          <p>
            Completing Statistical Programming with R and Data
            Visualization will significantly reduce two of your
            current competency gaps.
          </p>

        </div>

        <button>
          View Skill Gaps →
        </button>

      </section>


      {/* =====================================================
          DEMO NOTE
      ===================================================== */}

      <div className="my-learning-demo-note">

        <span>●</span>

        <div>
          <strong>Demo Environment</strong>

          <p>
            Learning progress shown here is simulated for the prototype.
            In the production platform, progress would be synchronized
            with connected learning platforms such as iGOT and NSSTA.
          </p>
        </div>

      </div>

    </div>
  );
}

export default MyLearning;