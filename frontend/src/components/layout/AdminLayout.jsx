import { Outlet } from "react-router-dom";
import AdminSidebar from "./AdminSidebar";
import "./AdminLayout.css";

function AdminLayout() {
  const storedUser = localStorage.getItem("authUser");

  let user = {
    name: "Dr. Rajesh Kumar",
    role: "admin",
  };

  if (storedUser) {
    try {
      user = JSON.parse(storedUser);
    } catch {
      // Keep demo administrator
    }
  }

  return (
    <div className="role-layout admin-layout">
      <AdminSidebar />

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
              <div className="role-avatar admin-avatar">
                RK
              </div>

              <div>
                <strong>
                  {user.name || "Dr. Rajesh Kumar"}
                </strong>

                <small>
                  Administrator
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

export default AdminLayout;