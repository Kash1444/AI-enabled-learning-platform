import { NavLink, useNavigate } from "react-router-dom";

function Sidebar() {
  const navigate = useNavigate();

  const menuItems = [
    {
      section: "MAIN",
      items: [
        {
          name: "Dashboard",
          path: "/employee/dashboard",
          icon: "⌂",
        },
        {
          name: "My Profile",
          path: "/employee/profile",
          icon: "👤",
        },
        {
          name: "Competencies",
          path: "/employee/competencies",
          icon: "🎯",
        },
        {
          name: "Skill Gaps",
          path: "/employee/skill-gaps",
          icon: "⚠",
        },
      ],
    },

    {
      section: "LEARNING",
      items: [
        {
          name: "Learning Path",
          path: "/employee/learning-path",
          icon: "🧭",
        },
        {
          name: "iGOT Courses",
          path: "/employee/igot",
          icon: "📚",
        },
        {
          name: "NSSTA Programs",
          path: "/employee/nssta",
          icon: "🏛",
        },
        {
          name: "My Learning",
          path: "/employee/learning",
          icon: "▶",
        },
      ],
    },

    {
      section: "ASSESSMENT",
      items: [
        {
          name: "Quizzes",
          path: "/employee/quizzes",
          icon: "✓",
        },
        {
          name: "Results",
          path: "/employee/results",
          icon: "📊",
        },
      ],
    },

    {
      section: "AI",
      items: [
        {
          name: "AI Assistant",
          path: "/employee/ai-assistant",
          icon: "✨",
        },
      ],
    },
  ];

  const handleLogout = () => {
    localStorage.removeItem("authUser");
    navigate("/");
  };

  return (
    <aside className="employee-sidebar">

      {/* ================= LOGO ================= */}

      <div className="sidebar-brand">

        <div className="sidebar-brand-icon">
          AI
        </div>

        <div>
          <div className="sidebar-brand-title">
            Skill Intelligence
          </div>

          <div className="sidebar-brand-subtitle">
            Official Statistics
          </div>
        </div>

      </div>


      {/* ================= NAVIGATION ================= */}

      <nav className="sidebar-navigation">

        {menuItems.map((section) => (

          <div
            className="sidebar-section"
            key={section.section}
          >

            <div className="sidebar-section-title">
              {section.section}
            </div>

            {section.items.map((item) => (

              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `sidebar-link ${
                    isActive ? "sidebar-link-active" : ""
                  }`
                }
              >

                <span className="sidebar-link-icon">
                  {item.icon}
                </span>

                <span>
                  {item.name}
                </span>

              </NavLink>

            ))}

          </div>

        ))}

      </nav>


      {/* ================= BOTTOM ================= */}

      <div className="sidebar-bottom">

        <div className="demo-label">
          DEMO ENVIRONMENT
        </div>

        <div className="demo-status">
          <span></span>
          Mock Data Connected
        </div>

        <button
          className="sidebar-logout"
          onClick={handleLogout}
        >
          <span>↪</span>
          Logout
        </button>

      </div>

    </aside>
  );
}

export default Sidebar;