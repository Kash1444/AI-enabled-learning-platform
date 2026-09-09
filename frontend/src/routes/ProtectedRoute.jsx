import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, allowedRole }) {
  const storedUser = localStorage.getItem("authUser");

  // User is not logged in
  if (!storedUser) {
    return <Navigate to="/" replace />;
  }

  const user = JSON.parse(storedUser);

  // User has wrong role
  if (user.role !== allowedRole) {
    return <Navigate to="/" replace />;
  }

  // Authorized
  return children;
}

export default ProtectedRoute;