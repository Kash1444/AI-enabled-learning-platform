import { Outlet } from "react-router-dom";
import TrainerSidebar from "./TrainerSidebar";
import "./TrainerLayout.css";

function TrainerLayout() {
  const storedUser = localStorage.getItem("authUser");

  let user = {
    name: "Priya Sharma",
    role: "trainer",
  };

  if (storedUser) {
    try {
      user = JSON.parse(storedUser);
    } catch {
      // Keep demo user
    }
  }

  return (
    <div className="role-layout trainer-layout">
      <TrainerSidebar />

      <div className="role-main">
        <header className="role-topbar">
          <div className="role-topbar-title">
            AI-Enabled Learning Platform
          </div>

          <div className="role-topbar-right">
            <button className="role-topbar-button">
              ?
            </button>

            <button className="role-topbar-button role-notification">
              🔔
              <span></span>
            </button>

            <div className="role-user-profile">
              <div className="role-avatar">
                PS
              </div>

              <div>
                <strong>
                  {user.name || "Priya Sharma"}
                </strong>

                <small>
                  Trainer
                </small>
              </div>
            </div>
          </div>
        </header>

        <main className="role-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default TrainerLayout;