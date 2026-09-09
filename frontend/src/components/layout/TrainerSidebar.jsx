import { NavLink, useNavigate } from "react-router-dom";
import "./TrainerLayout.css";

function TrainerSidebar() {
  const navigate = useNavigate();

  const menuItems = [
    {
      section: "MAIN",
      items: [
        {
          name: "Dashboard",
          path: "/trainer/dashboard",
          icon: "⌂",
        },
        {
          name: "Learner Results",
          path: "/trainer/learner-results",
          icon: "📊",
        },
      ],
    },
    {
      section: "CONTENT",
      items: [
        {
          name: "Upload Materials",
          path: "/trainer/upload-materials",
          icon: "📤",
        },
        {
          name: "Generate Assessment",
          path: "/trainer/generate-assessment",
          icon: "✨",
        },
        {
          name: "Assessments",
          path: "/trainer/assessments",
          icon: "✓",
        },
      ],
    },
  ];

  const handleLogout = () => {
    localStorage.removeItem("authUser");
    navigate("/");
  };

  return (
    <aside className="role-sidebar trainer-sidebar">
      <div className="role-sidebar-brand">
        <div className="role-brand-icon">AI</div>

        <div>
          <div className="role-brand-title">
            Skill Intelligence
          </div>

          <div className="role-brand-subtitle">
            Trainer Portal
          </div>
        </div>
      </div>

      <nav className="role-sidebar-navigation">
        {menuItems.map((section) => (
          <div
            className="role-sidebar-section"
            key={section.section}
          >
            <div className="role-sidebar-section-title">
              {section.section}
            </div>

            {section.items.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `role-sidebar-link ${
                    isActive ? "role-sidebar-link-active" : ""
                  }`
                }
              >
                <span className="role-sidebar-icon">
                  {item.icon}
                </span>

                <span>{item.name}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </nav>

      <div className="role-sidebar-bottom">
        <div className="role-demo-label">
          DEMO ENVIRONMENT
        </div>

        <div className="role-demo-status">
          <span></span>
          Mock Data Connected
        </div>

        <button
          className="role-sidebar-logout"
          onClick={handleLogout}
        >
          <span>↪</span>
          Logout
        </button>
      </div>
    </aside>
  );
}

export default TrainerSidebar;