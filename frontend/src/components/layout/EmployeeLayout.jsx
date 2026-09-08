import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import "./EmployeeLayout.css";

function EmployeeLayout() {
  return (
    <div className="employee-layout">

      {/* Sidebar */}
      <Sidebar />


      {/* Main Application Area */}

      <div className="employee-main">

        {/* Topbar */}

        <header className="employee-topbar">

          <div className="topbar-left">

            <span className="topbar-label">
              AI-Enabled Learning Platform
            </span>

          </div>


          <div className="topbar-right">

            <button className="topbar-icon-button">
              ?
            </button>

            <button className="topbar-icon-button">
              🔔
              <span className="topbar-notification-dot"></span>
            </button>


            <div className="topbar-profile">

              <div className="topbar-avatar">
                AK
              </div>

              <div className="topbar-user">

                <strong>
                  Arun Kumar
                </strong>

                <span>
                  Statistical Officer
                </span>

              </div>

            </div>

          </div>

        </header>


        {/* Page Content */}

        <main className="employee-content">
          <Outlet />
        </main>

      </div>

    </div>
  );
}

export default EmployeeLayout;