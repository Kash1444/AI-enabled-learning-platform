import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./NSSTAPrograms.css";

const programs = [
  {
    id: 1,
    title: "Sampling Techniques for Official Statistics",
    category: "Statistical Methodology",
    provider: "NSSTA TPAC",
    duration: "6 Hours",
    level: "Intermediate",
    mode: "Instructor-led",
    skill: "Sampling Methodology",
    currentLevel: 2.8,
    requiredLevel: 4.2,
    priority: "High Priority",
    recommended: true,
    description:
      "Strengthen sampling design, estimation techniques and official survey methodology.",
    reason:
      "AI identified Sampling Methodology as one of your highest-priority competency gaps.",
  },

  {
    id: 2,
    title: "Advanced Survey Methodology",
    category: "Statistical Methodology",
    provider: "NSSTA TPAC",
    duration: "8 Hours",
    level: "Advanced",
    mode: "Instructor-led",
    skill: "Survey Methodology",
    currentLevel: 3.1,
    requiredLevel: 4.2,
    priority: "Medium Priority",
    recommended: false,
    description:
      "Develop advanced understanding of survey design, estimation and statistical quality.",
    reason:
      "Recommended to strengthen your broader statistical methodology capabilities.",
  },

  {
    id: 3,
    title: "Official Statistics: Concepts and Practices",
    category: "Official Statistics",
    provider: "NSSTA",
    duration: "5 Hours",
    level: "Beginner",
    mode: "Blended",
    skill: "Official Statistics",
    currentLevel: 3.8,
    requiredLevel: 4.5,
    priority: "Medium Priority",
    recommended: false,
    description:
      "Build a strong foundation in concepts, standards and practices used in official statistics.",
    reason:
      "Helps strengthen domain knowledge required for your current statistical role.",
  },

  {
    id: 4,
    title: "Statistical Data Quality Management",
    category: "Official Statistics",
    provider: "NSSTA TPAC",
    duration: "4 Hours",
    level: "Intermediate",
    mode: "Online",
    skill: "Data Quality",
    currentLevel: 3.4,
    requiredLevel: 4.2,
    priority: "Medium Priority",
    recommended: false,
    description:
      "Learn practical approaches for maintaining quality, accuracy and consistency in statistical data.",
    reason:
      "Supports improvement in statistical data management and reporting.",
  },

  {
    id: 5,
    title: "Data Governance for Public Sector",
    category: "Data & Technology",
    provider: "NSSTA",
    duration: "4 Hours",
    level: "Intermediate",
    mode: "Online",
    skill: "Digital Governance",
    currentLevel: 3.2,
    requiredLevel: 4.0,
    priority: "Medium Priority",
    recommended: false,
    description:
      "Understand data governance principles and their application in public-sector statistical systems.",
    reason:
      "Recommended to address your Digital Governance competency gap.",
  },

  {
    id: 6,
    title: "Leadership for Statistical Officers",
    category: "Leadership & Management",
    provider: "NSSTA TPAC",
    duration: "3 Hours",
    level: "Intermediate",
    mode: "Instructor-led",
    skill: "Behavioral / Managerial",
    currentLevel: 4.0,
    requiredLevel: 4.2,
    priority: "Low Priority",
    recommended: false,
    description:
      "Develop leadership, communication and team-management capabilities for statistical officers.",
    reason:
      "Supports continuous development of behavioural and managerial competencies.",
  },
];

const categories = [
  "All Programs",
  "Statistical Methodology",
  "Official Statistics",
  "Data & Technology",
  "Leadership & Management",
];

function NSSTAPrograms() {
  const navigate = useNavigate();

  const [activeCategory, setActiveCategory] = useState("All Programs");
  const [search, setSearch] = useState("");

  const filteredPrograms = programs.filter((program) => {
    const matchesCategory =
      activeCategory === "All Programs" ||
      program.category === activeCategory;

    const matchesSearch =
      program.title.toLowerCase().includes(search.toLowerCase()) ||
      program.skill.toLowerCase().includes(search.toLowerCase());

    return matchesCategory && matchesSearch;
  });

  const recommendedPrograms = programs.filter(
    (program) => program.recommended
  );

  return (
    <div className="nssta-page">

      {/* ================= HEADER ================= */}

      <div className="nssta-header">

        <div>
          <div className="nssta-breadcrumb">
            Employee Portal / NSSTA Programs
          </div>

          <h1>
            NSSTA Programs
          </h1>

          <p>
            Professional development programmes aligned with your
            competency requirements and career role.
          </p>
        </div>

        <div className="nssta-header-badge">
          <span>🏛</span>
          <div>
            <strong>NSSTA</strong>
            <small>
              National Statistical Systems Training Academy
            </small>
          </div>
        </div>

      </div>


      {/* ================= AI RECOMMENDATION ================= */}

      <section className="nssta-ai-banner">

        <div className="nssta-ai-icon">
          ✨
        </div>

        <div className="nssta-ai-content">

          <div className="nssta-ai-label">
            AI PERSONALIZED RECOMMENDATION
          </div>

          <h2>
            Your highest-priority NSSTA recommendation
          </h2>

          <p>
            Based on your competency profile, <strong>
            Sampling Techniques for Official Statistics
            </strong> is recommended as your next training programme.
          </p>

        </div>

        <button
          className="nssta-ai-button"
          onClick={() => {
            document
              .getElementById("recommended-program")
              ?.scrollIntoView({ behavior: "smooth" });
          }}
        >
          View Recommendation →
        </button>

      </section>


      {/* ================= MY LEARNING ================= */}

      <section className="nssta-learning-summary">

        <div className="nssta-summary-icon">
          📚
        </div>

        <div className="nssta-summary-content">
          <span>MY NSSTA LEARNING</span>
          <strong>1 Programme Recommended</strong>
          <small>
            Continue building competencies through NSSTA professional
            development programmes.
          </small>
        </div>

        <div className="nssta-summary-progress">

          <div className="nssta-progress-top">
            <span>Current Progress</span>
            <strong>0%</strong>
          </div>

          <div className="nssta-progress-track">
            <div
              className="nssta-progress-fill"
              style={{ width: "0%" }}
            ></div>
          </div>

          <small>
            No NSSTA programme started yet
          </small>

        </div>

      </section>


      {/* ================= RECOMMENDED ================= */}

      <section
        className="nssta-recommended"
        id="recommended-program"
      >

        <div className="nssta-section-heading">

          <div>
            <span className="nssta-section-label">
              AI CURATED
            </span>

            <h2>
              Recommended for You
            </h2>

            <p>
              Programmes selected based on your current competency gaps.
            </p>
          </div>

          <div className="nssta-match">
            <span>✦</span>
            Personalized Match
          </div>

        </div>


        {recommendedPrograms.map((program) => (

          <div
            className="nssta-featured-card"
            key={program.id}
          >

            <div className="nssta-featured-left">

              <div className="nssta-program-icon">
                🏛
              </div>

              <div>

                <div className="nssta-program-meta">

                  <span className="nssta-provider">
                    {program.provider}
                  </span>

                  <span className="nssta-high-priority">
                    {program.priority}
                  </span>

                </div>

                <h3>
                  {program.title}
                </h3>

                <p>
                  {program.description}
                </p>

                <div className="nssta-program-details">

                  <span>◷ {program.duration}</span>
                  <span>◈ {program.level}</span>
                  <span>▣ {program.mode}</span>

                </div>

              </div>

            </div>


            <div className="nssta-featured-right">

              <div className="nssta-gap-box">

                <span>Competency Gap</span>

                <strong>
                  {(program.requiredLevel - program.currentLevel).toFixed(1)}
                </strong>

                <small>
                  {program.skill}
                </small>

              </div>

              <div className="nssta-reason">

                <span>✨ Why AI recommends this</span>

                <p>
                  {program.reason}
                </p>

              </div>

              <button
                className="nssta-primary-button"
                onClick={() =>
                  alert(
                    "Demo: NSSTA programme enrollment will be connected to the real NSSTA system in the production version."
                  )
                }
              >
                View Programme →
              </button>

            </div>

          </div>

        ))}

      </section>


      {/* ================= SEARCH / FILTER ================= */}

      <section className="nssta-catalog">

        <div className="nssta-catalog-header">

          <div>
            <h2>
              Explore NSSTA Programs
            </h2>

            <p>
              Browse programmes across different competency areas.
            </p>
          </div>

          <div className="nssta-search-wrapper">
            <span>⌕</span>

            <input
              type="text"
              placeholder="Search programs..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

        </div>


        {/* Categories */}

        <div className="nssta-category-list">

          {categories.map((category) => (

            <button
              key={category}
              className={
                activeCategory === category
                  ? "nssta-category active"
                  : "nssta-category"
              }
              onClick={() => setActiveCategory(category)}
            >
              {category}
            </button>

          ))}

        </div>


        {/* Program Grid */}

        <div className="nssta-program-grid">

          {filteredPrograms.map((program) => (

            <div
              className="nssta-program-card"
              key={program.id}
            >

              <div className="nssta-card-top">

                <div className="nssta-small-icon">
                  🏛
                </div>

                <span className="nssta-provider-badge">
                  {program.provider}
                </span>

              </div>


              <span className="nssta-category-tag">
                {program.category}
              </span>

              <h3>
                {program.title}
              </h3>

              <p>
                {program.description}
              </p>


              <div className="nssta-card-details">

                <span>◷ {program.duration}</span>
                <span>◈ {program.level}</span>
                <span>▣ {program.mode}</span>

              </div>


              <div className="nssta-skill-row">

                <span>
                  Skill addressed
                </span>

                <strong>
                  {program.skill}
                </strong>

              </div>


              <button
                className="nssta-outline-button"
                onClick={() =>
                  alert(
                    "Demo programme details. Real NSSTA integration will be added later."
                  )
                }
              >
                View Details →
              </button>

            </div>

          ))}

        </div>

      </section>


      {/* ================= DEMO NOTE ================= */}

      <div className="nssta-demo-note">

        <span>●</span>

        <div>
          <strong>Demo Environment</strong>

          <p>
            NSSTA programme information shown here is mock data for
            demonstration purposes. In the production platform,
            programmes will be retrieved from the official NSSTA
            training catalogue through an authorized integration.
          </p>
        </div>

      </div>

    </div>
  );
}

export default NSSTAPrograms;