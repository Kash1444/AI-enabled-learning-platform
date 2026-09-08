import {
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "../pages/Login";
import ProtectedRoute from "./ProtectedRoute";


// ================= EMPLOYEE LAYOUT =================

import EmployeeLayout from "../components/layout/EmployeeLayout";


// ================= EMPLOYEE PAGES =================

import EmployeeDashboard from "../pages/employee/EmployeeDashboard";
import Profile from "../pages/employee/Profile";
import Competencies from "../pages/employee/Competencies";
import SkillGaps from "../pages/employee/SkillGaps";
import LearningPath from "../pages/employee/LearningPath";
import IGOTCourses from "../pages/employee/IGOTCourses";
import NSSTAPrograms from "../pages/employee/NSSTAPrograms";
import MyLearning from "../pages/employee/MyLearning";
import Quiz from "../pages/employee/Quiz";
import QuizResult from "../pages/employee/QuizResult";
import AIAssistant from "../pages/employee/AIAssistant";


// ================= TRAINER LAYOUT =================

import TrainerLayout from "../components/layout/TrainerLayout";


// ================= TRAINER PAGES =================

import TrainerDashboard from "../pages/trainer/TrainerDashboard";
import UploadMaterials from "../pages/trainer/UploadMaterials";
import GenerateAssessment from "../pages/trainer/GenerateAssessment";
import Assessments from "../pages/trainer/Assessments";
import LearnerResults from "../pages/trainer/LearnerResults";


// ================= ADMIN LAYOUT =================

import AdminLayout from "../components/layout/AdminLayout";


// ================= ADMIN PAGES =================

import AdminDashboard from "../pages/admin/AdminDashboard";
import WorkforceAnalytics from "../pages/admin/WorkforceAnalytics";
import CompetencyAnalytics from "../pages/admin/CompetencyAnalytics";
import SkillGapAnalytics from "../pages/admin/SkillGapAnalytics";
import TrainingAnalytics from "../pages/admin/TrainingAnalytics";
import FutureSkills from "../pages/admin/FutureSkills";
import Reports from "../pages/admin/Reports";


function AppRoutes() {
  return (
    <Routes>

      {/* ==================================================
          LOGIN
      ================================================== */}

      <Route
        path="/"
        element={<Login />}
      />


      {/* ==================================================
          EMPLOYEE
      ================================================== */}

      <Route
        path="/employee"
        element={
          <ProtectedRoute allowedRole="employee">
            <EmployeeLayout />
          </ProtectedRoute>
        }
      >

        <Route
          index
          element={
            <Navigate
              to="/employee/dashboard"
              replace
            />
          }
        />

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

        <Route
          path="quizzes"
          element={<Quiz />}
        />

        <Route
          path="results"
          element={<QuizResult />}
        />

        <Route
          path="ai-assistant"
          element={<AIAssistant />}
        />

      </Route>


      {/* ==================================================
          TRAINER
      ================================================== */}

      <Route
        path="/trainer"
        element={
          <ProtectedRoute allowedRole="trainer">
            <TrainerLayout />
          </ProtectedRoute>
        }
      >

        <Route
          index
          element={
            <Navigate
              to="/trainer/dashboard"
              replace
            />
          }
        />

        <Route
          path="dashboard"
          element={<TrainerDashboard />}
        />

        <Route
          path="upload-materials"
          element={<UploadMaterials />}
        />

        <Route
          path="generate-assessment"
          element={<GenerateAssessment />}
        />

        <Route
          path="assessments"
          element={<Assessments />}
        />

        <Route
          path="learner-results"
          element={<LearnerResults />}
        />

      </Route>


      {/* ==================================================
          ADMIN
      ================================================== */}

      <Route
        path="/admin"
        element={
          <ProtectedRoute allowedRole="admin">
            <AdminLayout />
          </ProtectedRoute>
        }
      >

        <Route
          index
          element={
            <Navigate
              to="/admin/dashboard"
              replace
            />
          }
        />

        <Route
          path="dashboard"
          element={<AdminDashboard />}
        />

        <Route
          path="workforce"
          element={<WorkforceAnalytics />}
        />

        <Route
          path="competencies"
          element={<CompetencyAnalytics />}
        />

        <Route
          path="skill-gaps"
          element={<SkillGapAnalytics />}
        />

        <Route
          path="training"
          element={<TrainingAnalytics />}
        />

        <Route
          path="future-skills"
          element={<FutureSkills />}
        />

        <Route
          path="reports"
          element={<Reports />}
        />

      </Route>


      {/* ==================================================
          FALLBACK
      ================================================== */}

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