import { useState } from "react";
import "./IGOTCourses.css";

function IGOTCourses() {
  const [activeCategory, setActiveCategory] = useState("All");
  const [search, setSearch] = useState("");

  const courses = [
    {
      id: 1,
      title: "Statistical Programming with R",
      category: "Statistical",
      level: "Intermediate",
      duration: "8 hours",
      progress: 25,
      status: "In Progress",
      description:
        "Learn R programming techniques for statistical analysis, data processing and reproducible workflows.",
      skill: "Statistical Programming",
      priority: "Recommended",
      icon: "💻",
    },
    {
      id: 2,
      title: "Data Visualization for Statistical Reporting",
      category: "Technical",
      level: "Intermediate",
      duration: "4 hours",
      progress: 40,
      status: "In Progress",
      description:
        "Develop effective visualizations for communicating statistical findings and official reports.",
      skill: "Data Visualization",
      priority: "Recommended",
      icon: "📊",
    },
    {
      id: 3,
      title: "Fundamentals of Official Statistics",
      category: "Statistical",
      level: "Beginner",
      duration: "5 hours",
      progress: 100,
      status: "Completed",
      description:
        "Understand the principles, standards and practices behind official statistics.",
      skill: "Official Statistics",
      priority: "Completed",
      icon: "📘",
    },
    {
      id: 4,
      title: "Digital Governance Fundamentals",
      category: "Digital Governance",
      level: "Beginner",
      duration: "5 hours",
      progress: 0,
      status: "Not Started",
      description:
        "Build an understanding of digital governance, public service delivery and data-driven administration.",
      skill: "Digital Governance",
      priority: "Recommended",
      icon: "🏛️",
    },
    {
      id: 5,
      title: "Advanced Statistical Methods",
      category: "Statistical",
      level: "Advanced",
      duration: "10 hours",
      progress: 0,
      status: "Not Started",
      description:
        "Explore advanced statistical methods used in government surveys and analytical studies.",
      skill: "Statistical Methods",
      priority: "Available",
      icon: "📈",
    },
    {
      id: 6,
      title: "Data Management for Public Sector",
      category: "Technical",
      level: "Intermediate",
      duration: "6 hours",
      progress: 0,
      status: "Not Started",
      description:
        "Learn practical approaches to managing, validating and organizing public-sector data.",
      skill: "Data Management",
      priority: "Available",
      icon: "🗄️",
    },
  ];

  const categories = [
    "All",
    "Statistical",
    "Technical",
    "Digital Governance",
  ];

  const filteredCourses = courses.filter((course) => {
    const matchesCategory =
      activeCategory === "All" ||
      course.category === activeCategory;

    const matchesSearch =
      course.title
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      course.skill
        .toLowerCase()
        .includes(search.toLowerCase());

    return matchesCategory && matchesSearch;
  });

  return (
    <div className="igot-page">

      {/* ================= HEADER ================= */}

      <div className="igot-header">

        <div>
          <div className="igot-breadcrumb">
            Employee Portal / iGOT Courses
          </div>

          <h1>iGOT Karmayogi Courses</h1>

          <p>
            Explore learning programmes recommended for your role,
            competencies and skill gaps.
          </p>
        </div>

        <div className="igot-source-badge">
          <span>●</span>
          Mock iGOT Integration
        </div>

      </div>


      {/* ================= AI RECOMMENDATION ================= */}

      <section className="igot-ai-banner">

        <div className="igot-ai-icon">
          ✨
        </div>

        <div className="igot-ai-content">

          <span className="igot-ai-label">
            AI RECOMMENDED FOR YOU
          </span>

          <h2>
            3 courses match your current competency gaps
          </h2>

          <p>
            Based on your Statistical Programming, Data Visualization
            and Digital Governance competency requirements.
          </p>

        </div>

        <button
          className="igot-ai-button"
          onClick={() => setActiveCategory("All")}
        >
          View Recommendations →
        </button>

      </section>


      {/* ================= STATS ================= */}

      <div className="igot-stats">

        <div className="igot-stat">

          <div className="igot-stat-icon blue">
            📚
          </div>

          <div>
            <strong>24</strong>
            <span>Available Courses</span>
          </div>

        </div>


        <div className="igot-stat">

          <div className="igot-stat-icon green">
            ✓
          </div>

          <div>
            <strong>8</strong>
            <span>Completed</span>
          </div>

        </div>


        <div className="igot-stat">

          <div className="igot-stat-icon orange">
            ▶
          </div>

          <div>
            <strong>2</strong>
            <span>In Progress</span>
          </div>

        </div>


        <div className="igot-stat">

          <div className="igot-stat-icon purple">
            🎯
          </div>

          <div>
            <strong>3</strong>
            <span>AI Recommended</span>
          </div>

        </div>

      </div>


      {/* ================= FILTER BAR ================= */}

      <div className="igot-toolbar">

        <div className="igot-search">

          <span>⌕</span>

          <input
            type="text"
            placeholder="Search courses or skills..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

        </div>


        <div className="igot-categories">

          {categories.map((category) => (

            <button
              key={category}
              className={
                activeCategory === category
                  ? "category-active"
                  : ""
              }
              onClick={() => setActiveCategory(category)}
            >
              {category}
            </button>

          ))}

        </div>

      </div>


      {/* ================= COURSE HEADER ================= */}

      <div className="igot-course-heading">

        <div>
          <h2>
            {activeCategory === "All"
              ? "Recommended & Available Courses"
              : `${activeCategory} Courses`}
          </h2>

          <p>
            {filteredCourses.length} courses available
          </p>
        </div>

        <select className="igot-sort">
          <option>Recommended</option>
          <option>Newest</option>
          <option>Duration</option>
          <option>Difficulty</option>
        </select>

      </div>


      {/* ================= COURSE GRID ================= */}

      <div className="igot-course-grid">

        {filteredCourses.map((course) => (

          <div
            className="igot-course-card"
            key={course.id}
          >

            {/* Card top */}

            <div className="igot-card-top">

              <div className="igot-course-icon">
                {course.icon}
              </div>

              <span
                className={
                  course.priority === "Recommended"
                    ? "course-recommended"
                    : course.priority === "Completed"
                    ? "course-completed"
                    : "course-available"
                }
              >
                {course.priority}
              </span>

            </div>


            {/* Title */}

            <h3>
              {course.title}
            </h3>

            <p className="igot-course-description">
              {course.description}
            </p>


            {/* Metadata */}

            <div className="igot-course-meta">

              <span>
                📂 {course.category}
              </span>

              <span>
                ◉ {course.level}
              </span>

              <span>
                ⏱ {course.duration}
              </span>

            </div>


            {/* Skill */}

            <div className="igot-skill">

              <span>
                Target Skill
              </span>

              <strong>
                {course.skill}
              </strong>

            </div>


            {/* Progress */}

            {course.progress > 0 && (

              <div className="igot-progress">

                <div className="igot-progress-header">

                  <span>
                    Your Progress
                  </span>

                  <strong>
                    {course.progress}%
                  </strong>

                </div>

                <div className="igot-progress-track">

                  <div
                    className="igot-progress-fill"
                    style={{
                      width: `${course.progress}%`,
                    }}
                  ></div>

                </div>

              </div>

            )}


            {/* Action */}

            <button
              className={
                course.status === "Completed"
                  ? "igot-course-button completed-button"
                  : "igot-course-button"
              }
            >
              {course.status === "Completed"
                ? "✓ Completed"
                : course.status === "In Progress"
                ? "Continue Learning"
                : "Start Learning"}

              {course.status !== "Completed" && (
                <span>→</span>
              )}
            </button>

          </div>

        ))}

      </div>


      {/* ================= EMPTY STATE ================= */}

      {filteredCourses.length === 0 && (

        <div className="igot-empty">

          <div>
            🔍
          </div>

          <h3>
            No courses found
          </h3>

          <p>
            Try another search term or category.
          </p>

        </div>

      )}


      {/* ================= DEMO NOTE ================= */}

      <div className="igot-demo-note">

        <span>ⓘ</span>

        <div>
          <strong>
            Demo Environment
          </strong>

          <p>
            Course information shown here is simulated for the prototype.
            In the final system, this catalogue would be connected to
            iGOT Karmayogi APIs.
          </p>
        </div>

      </div>

    </div>
  );
}

export default IGOTCourses;