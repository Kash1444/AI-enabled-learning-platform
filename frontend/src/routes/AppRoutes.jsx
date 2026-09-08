import {
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "../pages/Login";
import ProtectedRoute from "./ProtectedRoute";
import SkillGaps from "../pages/employee/SkillGaps";
import EmployeeLayout from "../components/layout/EmployeeLayout";

import EmployeeDashboard from "../pages/employee/EmployeeDashboard";
import Profile from "../pages/employee/Profile";
import Competencies from "../pages/employee/Competencies";
import LearningPath from "../pages/employee/LearningPath";
import IGOTCourses from "../pages/employee/IGOTCourses";
import NSSTAPrograms from "../pages/employee/NSSTAPrograms";
import MyLearning from "../pages/employee/MyLearning";
function AppRoutes() {
  return (
    <Routes>

      {/* =====================================================
          LOGIN
      ===================================================== */}

      <Route
        path="/"
        element={<Login />}
      />

        
      {/* =====================================================
          EMPLOYEE
      ===================================================== */}

      <Route
        path="/employee"
        element={
          <ProtectedRoute allowedRole="employee">
            <EmployeeLayout />
          </ProtectedRoute>
        }
      >

        {/* Default employee route */}

        <Route
          index
          element={
            <Navigate
              to="/employee/dashboard"
              replace
            />
          }
        />


        {/* Dashboard */}

        <Route
            path="dashboard"
            element={<EmployeeDashboard />}
            />
            <Route
                path="profile"
                element={<Profile />}
            />
            <Route
                path="competencies"
                element={<Competencies />}
            />
            <Route
                path="skill-gaps"
                element={<SkillGaps />}
                />
            <Route
                path="learning-path"
                element={<LearningPath />}
                />
            <Route
                path="igot"
                element={<IGOTCourses />}
                />
            <Route
                path="nssta"
                element={<NSSTAPrograms />}
                />
            <Route
                path="learning"
                element={<MyLearning />}
                />


      </Route>


      {/* =====================================================
          TEMPORARY TRAINER
      ===================================================== */}

      <Route
        path="/trainer/dashboard"
        element={
          <ProtectedRoute allowedRole="trainer">
            <div>
              <h1>Trainer Dashboard</h1>
              <p>Trainer dashboard coming next.</p>
            </div>
          </ProtectedRoute>
        }
      />


      {/* =====================================================
          TEMPORARY ADMIN
      ===================================================== */}

      <Route
        path="/admin/dashboard"
        element={
          <ProtectedRoute allowedRole="admin">
            <div>
              <h1>Admin Dashboard</h1>
              <p>Admin dashboard coming next.</p>
            </div>
          </ProtectedRoute>
        }
      />


      {/* =====================================================
          UNKNOWN ROUTES
      ===================================================== */}

      <Route
        path="*"
        element={
          <Navigate
            to="/"
            replace
          />
        }
      />

    </Routes>
  );
}

export default AppRoutes;